%include "sys.equ"
global sys_base
global ram_top
SECTION .data
sys_base:
	dw seg_cpmcode
ram_top:
	dw seg_cpmdata

