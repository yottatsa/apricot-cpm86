all: loader.cmd loader.hex

loader.obj: loader.a86 platform.equ cpm3.equ

%.obj: %.a86
	./emu2/emu2 rasm86.exe $<

%.cmd: %.obj
	./emu2/emu2 linkcmd.exe $<

loader.hex: loader.cmd
	./ihex/bin2ihex -i $< -o $@

.PHONY:	all

