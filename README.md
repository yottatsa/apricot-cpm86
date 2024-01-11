# Apricot Personal CP/M-86

to build `BDOS` and `LOADER`

    $ make
    -rw-r--r--  1 yottatsa  staff   1408 11 Jan 23:41 loader.cmd
    -rw-r--r--  1 yottatsa  staff  61184 11 Jan 23:41 new.sys

## TODO

### what FS is needed for this 
Currently the system is booting but `dir` doesn't work. Original disk uses FAT12, I'm also trying CP/M filesystem.

### figure out if it's bootable on Xi
Apricot PC/Xi shows Error 99 (disc is not bootable) straight away.

### annotate leftovers
* [`cpm3.equ`](https://github.com/yottatsa/apricot-cpm86/blob/main/cpm3.equ#L14-L16)
* handwaving on memory in [`loader.a86`](https://github.com/yottatsa/apricot-cpm86/blob/main/loader.a86#L111-L300)
