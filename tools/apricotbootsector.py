#!/usr/bin/env python3
import sys
import struct
import io
import math

from typing import NamedTuple, OrderedDict
from enum import Enum

from pyfat12 import FloppyImage, FAT12 as FAT12Base

class ApricotOS(Enum):
    invalid = 0
    msdos2 = 1
    psystem = 2
    cpm86 = 3
    ccpm = 4
    bos = 5
    unix = 6

    @classmethod
    def to_byte(self):
        return bytes((self.value,))

class ApricotBootType(Enum):
    nonbootable = 0
    genericrom = 1  # might be other way around
    pcxiram = 2     # with it
    pcxirom = 3
    portablerom = 4
    f1rom = 5

class ApricotDiskType(Enum):
    unknown = -1
    ss70 = 0
    ss80 = 1
    ds80 = 2
    hdd5 = 3
    hdd10 = 4
    hdd20 = 5

def s2o(i: int) -> int:
    return (i >> 12) + (i & 0xffff)

class ApricotConfiguration(NamedTuple):
    sctl_sz: int = 512
    clu_sz: int = 1
    rsvd_sct: int = 1
    n_fats: int = 2
    dir_ent: int = 128
    n_sec: int = 630
    media_id: int = 0x0fc
    n_fat_s: int = 2
    disk_type: ApricotDiskType = ApricotDiskType.unknown
    start_sct: int = 0
    font_name: bytes = b""
    keys_name: bytes = b""

    @classmethod
    def from_bytes(cls, label: bytes) -> "ApricotConfiguration":
        (sctl_sz, clu_sz, rsvd_sct, n_fats, dir_ent, n_sec, media_id, n_fats, unused1, unused2, font_name, keys_name) = struct.unpack("<HBHBHHBHBH16s16s", label[0x50:0x80])
        return cls(sctl_sz, clu_sz, rsvd_sct, n_fats, dir_ent, n_sec, media_id, n_fats, unused1, unused2, font_name, keys_name)

class ApricotLabel(NamedTuple):
    form_vers: bytes = b""
    op_sys: ApricotOS = ApricotOS.invalid
    sw_prot: bool = False
    copy_prot: bool = False
    boot_disk: ApricotBootType = ApricotBootType.nonbootable
    multi_region: int = 0
    winchester: bool = False
    sec_size: int = 512
    sec_track: int = 9
    tracks_side: int = 70
    sides: int = 2
    interleave: int = 1
    skew: int = 1
    boot_locn: int = 29
    boot_size: int = 112
    boot_addr: int = 0x0d800000
    boot_start: int = 0x0e000029
    data_locn: int = 13
    generation: int = 0
    copy_count: int = 0
    copy_max: int = 0xffff
    serial_id: bytes = b""
    part_id: bytes = b""
    copyrite: bytes = b""

    @classmethod
    def from_bytes(cls, label: bytes) -> "ApricotLabel":
        (form_vers, op_sys, sw_prot, copy_prot, boot_disk, multi_region, winchester) = struct.unpack("<8sBBBBBB", label[0:0xe])
        (sec_size, sec_track, tracks_side, sides, interleave, skew) = struct.unpack("<HHIBBH", label[0xe:0x1a])
        (boot_locn, boot_size, boot_addr, boot_start, data_locn) = struct.unpack("<IHIII",label[0x1a:0x2c])
        (generation, copy_count, copy_max, serial_id, part_id) = struct.unpack("<HHH8s8s", label[0x2c:0x42])
        copyrite = label[0x42:0x50]
        return cls(form_vers, ApricotOS(op_sys), bool(sw_prot), bool(copy_prot), ApricotBootType(boot_disk), multi_region, bool(winchester), sec_size, sec_track, tracks_side, sides, interleave, skew, boot_locn, boot_size, boot_addr, boot_start, data_locn, generation, copy_count, copy_max, serial_id, part_id, copyrite.split(b"\x00", 1)[0])
    
class Apridisk(FloppyImage):

    def __init__(self, capacity):
        self.size = 3.5
        self.capacity = capacity
        self.bytes_per_sector = 512

    @classmethod
    def from_file(cls, f: io.IOBase):
        data = bytearray(f.read())
        capacity = len(data)
        self = cls(capacity)
        self._data = data
        return self

    @property
    def label(self) -> ApricotLabel:
        return ApricotLabel.from_bytes(self.read_sector(0))

    @property
    def config(self) -> ApricotConfiguration:
        return ApricotConfiguration.from_bytes(self.read_sector(0))

    def verify_label(self):
        label = self.label
        assert self.bytes_per_sector == label.sec_size
        total_secs = label.sec_track * label.tracks_side * label.sides
        total_size = label.sec_size * total_secs
        assert self.capacity == total_size
        config = self.config
        assert self.bytes_per_sector == config.sctl_sz
        assert total_secs == config.n_sec

    def __str__(self) -> str:
        label = self.label
        return f"{label.form_vers.decode()} {hex(s2o(label.boot_addr))}:{hex(s2o(label.boot_start))}@{label.boot_locn}-{label.boot_size+label.boot_locn}s, {label.data_locn}"

class FAT12(FAT12Base):
    def _readfs(self):
        self._readapricotlabel()
        self._readfat()
        self._readlabel()
        self._chdirroot()
        self._readfiles()

    def _readapricotlabel(self):
        label = self._image.label
        self.bytes_per_sector = label.sec_size
        self.sectors_per_track = label.sec_track
        self.number_of_heads = label.sides

        config = self._image.config
        self.sectors_per_cluster = config.clu_sz
        self.fat_start_sector = 1
        self.fat_count = 2
        self.sectors_per_fat = config.n_fat_s
        self.root_entries = config.dir_ent
        self.logical_sectors = config.n_sec
        self.descriptor = config.media_id
        self.hidden_sectors = config.rsvd_sct
        self.large_total_logical_sectors = 0
        self.drive_number = 0
        self.ebpb_flags = 0
        self.has_ebpb = False
        self.serial = None
        self.bpb_label = b" " * 11
        self.fs_type = None

    def _readfiles(self):
        files = list(self.listfiles("/", hidden=True))
        label = self._image.label
        if label.boot_disk != ApricotBootType.nonbootable:
            assert len(files) >=4
            assert self._cluster_index(files[0].starting_cluster) == label.data_locn
            assert self._cluster_index(files[2].starting_cluster) == label.boot_locn
            assert math.ceil(files[2].size/512) >= label.boot_size
            assert s2o(label.boot_start) - s2o(label.boot_addr) < files[2].size
        self.files = files

if __name__ == "__main__":
    for fname in sys.argv[1:]:
        with open(fname, "rb") as f:
            a = Apridisk.from_file(f)
        a.verify_label()
        print(a.label)
        print(a.config)
        fs = FAT12(a)
        print(f"{fname}: {a}")
        print(fs.files)
