

; Description: Program introduces programmer, gets the user's name, asks them to enter a number (which is asked until an invalid num is given),
;	Calculates the average of provided nums. Displays numbers given, the sum of nums, the max num, the min num, the average and a parting message.

INCLUDE Irvine32.inc

upperlimit_1 = -200
lowerlimit_1 = -100

upperlimit_2 = -50
lowerlimit_2 = -1

;_________________________________________________________________________________________________________________________________________________________________

.data
; introduction
	; greeting and name
	intro_1     BYTE    "Hello, welcome to the Integer Collector 3000 by Riley Ovenshire.",0
	intro_2		BYTE	"We will be collecting negative integers between specific bounds, entered by you.",0
	intro_3		BYTE	"Then, we will display statistics such as minimum, maximum, average, total sum, and total number of valid inputs.",0 
	prompt_1	BYTE	"What is your name? ",0
	userName	BYTE	33 DUP(0)							; to be entered by user
	intro_4		BYTE	"Nice to meet you, ",0
	
; getting the data
	; displaying the instructions for the user
	instr_1		BYTE	"Please enter numbers in [-200, -100] or [-50, -1].",0
	instr_2		BYTE	"Enter a non-negative number when you are finished, then we will display the statistics for your given numbers.",0
	numprmt		BYTE	"Enter a number: ",0
	userNum		DWORD	?									; to be entered by user
	outofrange	BYTE	"Number is out of range. ",0							

; calculating and displaying the data
	amtrep1	BYTE	"You entered ",0
	amtrep2	BYTE	" valid numbers.",0						; amount of valid nums entered by user
	numamt	DWORD	0

	novals	BYTE	"Hmmm, you didn't enter any valid numbers.",0				; special message for user who entered no valid numbers

	sumrep	BYTE	"The sum of your valid numbers is ",0
	sum		DWORD	?			; sum of all valid numbers

	maxrep	BYTE	"Your maximum valid number is ",0
	maxnum	DWORD	-201			; maximum num (closest to 0)
	minrep	BYTE	"Your minimum valid number is ",0
	minnum	DWORD	0			; minimum num (furthest from 0)

	avgrep	BYTE	"The rounded average of your valid numbers is ",0
	avgnum	DWORD	?			; average, rounded to nearest int

; saying goodbye
	gbye	BYTE	"Thanks for playing. Bye, ",0

;_________________________________________________________________________________________________________________________________________________________________

.code
main PROC

;--------------------------------------------------------
; introduction
;--------------------------------------------------------
; introduce program and programmer
	mov		EDX, OFFSET intro_1
	call	WriteString
	call	CrLf

	mov		EDX, OFFSET intro_2
	call	WriteString
	call	CrLf

	mov		EDX, OFFSET intro_3
	call	WriteString
	call	CrLf

; get user's name, greet user
	mov		EDX, OFFSET prompt_1
	call	WriteString
	mov		EDX, OFFSET userName
	mov		ECX, 32
	call	ReadString

	mov		EDX, OFFSET intro_4
	call	WriteString
	mov		EDX, OFFSET userName
	call	WriteString
	call	CrLf
	call	CrLf

;--------------------------------------------------------
; getting the data
;--------------------------------------------------------
; display instructions for user
	mov		EDX, OFFSET instr_1
	call	WriteString
	call	CrLf
	mov		EDX, OFFSET instr_2
	call	WriteString
	call	CrLf


; repeating prompts for user to enter numbers
_startLoop:
	mov		EDX, OFFSET numprmt
	call	WriteString
	call	ReadInt
	mov		userNum, EAX
	jns		_positiveInt									; checks sign flag to see if user indicated they are done by entering an unsigned int

	cmp		userNum, upperlimit_1							; is user input less than -200?
	jl		_outOfRange
	cmp		userNum, lowerlimit_1							; user input has to be greater than -200, but is it less than -100?
	jl		_validNum
	
	cmp		userNum, lowerlimit_1							; is user input greater than -100?
	cmp		userNum, upperlimit_2							; ... and is it less than -50?
	jl		_outOfRange									; then it's in no man's land

	cmp		userNum, upperlimit_2							; well maybe it is greater than -50!
	cmp		userNum, lowerlimit_2							; but is it less than -1?
	jl		_validNum									; if so, great! it's valid
	jg		_outofRange									; if not, L


;--------------------------------------------------------
; calculate validNum, with given data
;--------------------------------------------------------
	
_validNum:
; adds userNum to the sum
	mov		EDX, OFFSET sum
	mov		EAX, sum
	add		EAX, userNum
	mov		sum, EAX
	
; determines if num is greater than max	
	mov		EDX, OFFSET maxnum
	mov		EAX, maxnum
	cmp		EAX, userNum
	jl		_setNewMax
	jmp		_checkMin

_setNewMax:
	mov		EDX, OFFSET maxnum
	mov		EAX, userNum
	mov		maxnum, EAX
	jmp		_checkMin

_checkMin:
	; determines if num is less that min
	mov		EDX, OFFSET minnum
	mov		EAX, minnum
	cmp		EAX, userNum
	jg		_setNewMin
	jmp		_countLoop

_setNewMin:
	mov		EDX, OFFSET minnum
	mov		EAX, usernum
	mov		minnum, EAX
	jmp		_countLoop
	
_countLoop:
	; adds a successful loop count to numamt counter
	mov		EDX, OFFSET numamt							
	add		numamt, 1

; restarts the loop
	jmp		_startLoop


;--------------------------------------------------------
; throws exceptions for out of range nums or positive num
;--------------------------------------------------------

_outOfRange:
	mov		EDX, OFFSET outofrange
	call	WriteString
	jmp		_startLoop

_positiveInt:											; if SF = 1, it is assumed that the user is done entering numbers, so the loop is broken.
	jmp		_showResults

;--------------------------------------------------------
; display results/statistics
;--------------------------------------------------------

_showResults:
; they entered valid numbers, right?
	mov		EDX, OFFSET numamt
	mov		EAX, numamt
	cmp		EAX, 0										; didn't enter any valid nums? jmp to special message (_noValidNums)
	je		_noValidNums

; amount of numbers entered
	mov		EDX, OFFSET amtrep1
	call	WriteString
	mov		EDX, OFFSET numamt
	mov		EAX, numamt
	call	WriteDec
	mov		EDX, OFFSET amtrep2
	call	WriteString
	call	CrLf

; sum of all valid numbers
	mov		EDX, OFFSET sumrep
	call	WriteString
	mov		EDX, OFFSET sum
	mov		EAX, sum
	call	WriteInt
	call	CrLf


; max number (closest to 0)
	mov		EDX, OFFSET maxrep
	call	WriteString
	mov		EDX, OFFSET maxnum
	mov		EAX, maxnum
	call	WriteInt
	call	CrLf


; min number (furthest from 0)
	mov		EDX, OFFSET minrep
	call	WriteString
	mov		EDX, OFFSET minnum
	mov		EAX, minnum
	call	WriteInt
	call	CrLf
	jmp		_average


_average:
; results shown, now show average
	finit
	fild	sum
	fild	numamt
	fdiv												; div st(1) :sum, by st(0),numamt
	fistp	avgnum										; pop avgnum off stack as int

	mov		EDX, OFFSET avgrep
	call	WriteString
	mov		EDX, OFFSET avgnum
	mov		EAX, avgnum
	call	WriteInt
	call	CrLf

	jmp		_goodbye
;--------------------------------------------------------
; saying goodbye, with user's name
;--------------------------------------------------------
_noValidNums:
	call	CrLf
	mov		EDX, OFFSET novals
	mov		AL, novals
	call	WriteString
	call	CrLf
	jmp		_goodbye
	
_goodbye:
	call	CrLf
	mov		EDX, OFFSET gbye
	mov		AL, gbye
	call	WriteString
	mov		EDX, OFFSET userName
	mov		AL, userName
	call	WriteString
	call	CrLf
	call	CrLf

main ENDP
END MAIN
	Invoke ExitProcess,0	; exit to operating system
main ENDP

; (insert additional procedures here)

END main
