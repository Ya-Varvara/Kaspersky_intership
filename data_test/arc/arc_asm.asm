;���������� �� ����� STK500: SW0-PD2, SW1-PD3, LED0-PB0
;*********************************************************************
.include "m8515def.inc" ;���� ����������� ��� ATmega8515

.def temp = r16 ;��������� �������
.equ led = 0 ;0-� ��� ����� PB
.equ sw0 = 2 ;2-� ��� ����� PD
.equ sw1 = 3 ;3-� ��� ����� PD
.org $000

;***������� �������� ����������, ������� � ������ $000***
rjmp INIT 		;��������� ������
rjmp led_on1 	;�� ��������� ������� INT0
rjmp led_on2 	;�� ��������� ������� INT1

;***������������� SP, ������, �������� �����***
INIT: 
	ldi temp,$5F 		;���������
	out SPL,temp 		; ��������� �����
	ldi temp,$02 		; �� ���������
	out SPH,temp 		; ������ ���
	ser temp 			;������������� �������
	out DDRB,temp 		; ����� PB �� �����
	out PORTB,temp 		;�������� ��
	clr temp 			;�������������
	out DDRD,temp 		; ����� PD �� ����
	ldi temp,0b00001100 ;��������� ���������������
	out PORTD,temp 		; ���������� ����� PD

	ldi temp,((1<<INT0)|(1<<INT1))	;���������� ����������
	out GICR,temp 					; � 6,7 ����� �������� ����� GICR
	ldi temp,0 						;��������� ����������
	out MCUCR,temp 					; �� ������� ������
	sei 							;���������� ���������� ����������

loop: 
	nop 		;����� �������� ����������
	rjmp loop

led_on1:
	cbi PORTB,led
	rcall delay1
	sbi PORTB,led

wait_0: 
	sbis pind,sw0
	rjmp wait_0
	reti

led_on2:
	cbi PORTB,led
	rcall delay2
	sbi PORTB,led

wait_1: 
	sbis pind,sw1
	rjmp wait_1
	reti

delay1: 	;��� ������������ �������� 1 c
	ldi r17,255
d0:	ldi r18,255
d1: ldi r19,20
d2: dec r19
	brne d2
	dec r18
	brne d1
	dec r17
	brne d0
	ret

delay2:	 	;������������ �������� 2 c
	rcall delay1
	rcall delay1
	ret
