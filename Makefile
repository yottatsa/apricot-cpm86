all: loader.cmd loader.hex

loader.obj: loader.a86 platform.equ cpm3.equ

%.obj: %.a86 emu2/emu2 rasm86.exe
	./emu2/emu2 rasm86.exe $<

%.cmd: %.obj emu2/emu2 linkcmd.exe
	./emu2/emu2 linkcmd.exe $<

loader.hex: loader.cmd ihex/bin2ihex
	./ihex/bin2ihex -i $< -o $@

ihex/bin2ihex: ihex
	git submodule update --init $^
	make -C $^

emu2/emu2: emu2
	git submodule update --init $^
	make -C $^

tools86.zip:
	wget -O $@ http://www.cpm.z80.de/download/tools86.zip
	touch $@

dos86pr2.zip: tools86.zip
	unzip -L $^ $@
	touch $@

rasm86.exe linkcmd.exe: dos86pr2.zip
	unzip -L $^ $@
	touch $@


.PHONY:	all

