# Apricot Personal CP/M-86

to build `BDOS` and `LOADER`

    $ make
    -rw-r--r--  1 yottatsa  staff   1408 11 Jan 23:41 loader.cmd
    -rw-r--r--  1 yottatsa  staff  61184 11 Jan 23:41 new.sys

to build `XIOS` from sources (or rebuild only xios part)

    $ make BUILDXIOS=1 [ clean-xios all ] 

## Sources

* [`bdos33.zip`](http://www.cpm.z80.de/download/bdos33.zip) from [Digital Research Source Code](http://www.cpm.z80.de/source.html)
* `aprixios.a86` in [`dpgen.zip`](http://www.seasip.info/Cpm/software/dpgen.zip) from [DOS Plus v1.x eXtended Input/Output system](http://www.seasip.info/Cpm/dosplus_xios.html)
* [Apricot disks](http://actapricot.org/disks/aprididx.htm)

## TODO

### what FS is needed for this 
~~Currently the system is booting but `dir` doesn't work. Original disk uses FAT12, I'm also trying CP/M filesystem.~~

On Apricot F1, it works with FAT12. However, you need to go to drive `C:`.

### figure out if it's bootable on Xi
Apricot PC/Xi shows Error 99 (disc is not bootable) straight away.
Managed to build somehow bootable disk with the CP/M instead of MS-DOS by patching `apr00013.dsk`, only to find that `int FCh` is not available in ROM BIOS. 

### annotate leftovers
* [`cpm3.equ`](https://github.com/yottatsa/apricot-cpm86/blob/main/cpm3.equ#L14-L16)
* handwaving on memory in [`loader.a86`](https://github.com/yottatsa/apricot-cpm86/blob/main/loader.a86#L111-L300)
