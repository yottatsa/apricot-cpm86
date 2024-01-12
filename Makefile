BDOSFILES = 	bdos.a86  cmdio.c    equates.a86  mem.a86   system.a86 \
		serial.a86 cmdio.h    exe2cmd.c    misc.a86  proctbl.a86 \
		xios.cmd  ccp.cmd    dpgen.c      rtm.a86 \
		cio.a86   entry.a86  sup.a86   bdos33ex.inp \
		ccpldr.a86
BDOSOBJS =	entry.obj sup.obj rtm.obj mem.obj cio.obj misc.obj bdos.obj \
		ccpldr.obj proctbl.obj


BIN2IHEX = ./ihex/bin2ihex
EMU2	= ./emu2/emu2
RUNTIME	= $(EMU2)
RASM86 	= $(RUNTIME) rasm86.exe
LINKCMD	= $(RUNTIME) linkcmd.exe
LINKEXE	= $(RUNTIME) linkexe.exe
DPGEN	= ./dpgen
EXE2CMD = ./exe2cmd
TOOLS	= $(BIN2IHEX) $(EMU2) $(RUNTIME) $(RASM86) $(LINKCMD) $(LINKEXE) $(DPGEN) $(EXE2CMD) cmdio.o dpgen.o

all: loader.cmd new.sys
	@ls -l $^

tags: loader.a86 platform.equ cpm3.equ $(BDOSFILES)
	ctags --languages=+Asm  --map-Asm=+.a86  --map-Asm=+.equ $^

clean:
	rm -f loader.hex loader.cmd loader.obg new.hex new.sys bdos33.exe $(BDOSOBJS) $(BDOSOBJS:.obj=.lst) $(BDOSOBJS:.obj=.sym) $(TOOLS)

pristine: clean
	rm -f $(BDOSFILES)

.PHONY:	all

## generic rules

%.obj %.lst %.sym: %.a86 $(RASM86)
	$(RASM86) $<

%.cmd: %.obj $(LINKCMD)
	$(LINKCMD) $<

## specific rules

loader.hex: loader.cmd $(BIN2IHEX)
	$(BIN2IHEX) -i $< -o $@

new.hex: new.sys $(BIN2IHEX)
	$(BIN2IHEX) -i $< -o $@

new.sys: bdos.cmd ccp.cmd xios.cmd $(DPGEN)
	$(DPGEN) base=F08

bdos.cmd:	bdos33.exe $(EXE2CMD)
	$(EXE2CMD) bdos33.exe bdos.cmd base=F08

bdos33.exe: bdos33ex.inp $(BDOSOBJS) $(LINKEXE)
	$(LINKEXE) bdos33ex[i

exe2cmd.exe:	exe2cmd.c
	pacc -Bs $<

## sources

$(BIN2IHEX): ihex
	git submodule update --init $^
	make -C $^

$(EMU2): emu2
	git submodule update --init $^
	make -C $^

tools86.zip:
	wget -O $@ http://www.cpm.z80.de/download/tools86.zip
	touch $@

bdos33.zip:
	wget -O $@ http://www.cpm.z80.de/download/bdos33.zip
	touch $@

dos86pr2.zip: tools86.zip
	unzip -DD -L $^ $@

rasm86.exe linkcmd.exe linkexe.exe: dos86pr2.zip
	unzip -DD -L $^ $@

$(BDOSFILES): bdos33.zip
	unzip -DD -L $^ $@

## dependencies

loader.obj:	loader.a86 platform.equ cpm3.equ
bdos.obj:	bdos.a86 equates.a86 system.a86
cio.obj:	cio.a86 equates.a86 system.a86
entry.obj:	entry.a86 equates.a86 system.a86
misc.obj:	misc.a86 equates.a86 system.a86 serial.a86
rtm.obj:	rtm.a86 equates.a86 system.a86
ccpldr.obj:	ccpldr.a86 equates.a86
mem.obj:	mem.a86 equates.a86
proctbl.obj:	proctbl.a86 equates.a86
sup.obj:	sup.a86 equates.a86

dpgen.o:	dpgen.c | cmdio.h
cmdio.o:	cmdio.c | cmdio.h
$(DPGEN):	dpgen.o cmdio.o
