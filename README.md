# Apricot Personal CP/M-86

to build `BDOS` and `LOADER`

    $ make
    -rw-r--r--  1 yottatsa  staff   1408 11 Jan 23:41 loader.cmd
    -rw-r--r--  1 yottatsa  staff  61184 11 Jan 23:41 new.sys

to build DOS Plus 1.2 (CP/M-86 v4.1) modified `XIOS` from sources (or rebuild only xios part) instead of bundled 3.3:

    $ make BUILDXIOS=1 [ clean-xios all ] 

## Sources

* [`bdos33.zip`](http://www.cpm.z80.de/download/bdos33.zip) from [Digital Research Source Code](http://www.cpm.z80.de/source.html)
* `aprixios.a86` in [`dpgen.zip`](http://www.seasip.info/Cpm/software/dpgen.zip) from [DOS Plus v1.x eXtended Input/Output system](http://www.seasip.info/Cpm/dosplus_xios.html)
* [Apricot disks](http://actapricot.org/disks/aprididx.htm)
  - [Apricot F1E Dr.Logo](http://actapricot.org/disks/aprid5ks.htm#apr00301.dsk)

## TODO

### what FS is needed for this 
~~Currently the system is booting but `dir` doesn't work. Original disk uses FAT12, I'm also trying CP/M filesystem.~~

On Apricot F1, it works with FAT12. However, you need to go to drive `C:`.
Version for Apricot Xi uses CP/M disk format.

### how does it boot
Apricot F-series has `int FCh` provided in ROM BIOS, therefore, `xios.cmd` (`aprixios.a86`) can be run as-is.

Apricot Xi requires RAM BIOS to provide with high-level API. Original distribution has it embedded in `cpm3.sys`, another option would be using a parts of [_RAM BIOS VR2.6 APRICOT PC/XI_ sources](http://actapricot.org/disks/aprid5ks.htm#apr00203.dsk).

### annotate leftovers
* [`cpm3.equ`](https://github.com/yottatsa/apricot-cpm86/blob/main/cpm3.equ#L14-L16)
* handwaving on memory in [`loader.a86`](https://github.com/yottatsa/apricot-cpm86/blob/main/loader.a86#L111-L300)
