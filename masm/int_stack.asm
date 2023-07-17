
; Description: This program will generate 200 random integers between 15 and 50, inclusive. It will display
;				the original list, sort that list, display the median value of the list, display the list in ascending order,
;				and dispay the number of instances for each generated value from lowest to highest.

INCLUDE Irvine32.inc

; Constants - immediate values, and can be used without passing via the stack.
	ARRAYSIZE	=		200
	LO			=		15
	HI			=		50
	SPACE		=		32										; ASCII code for space
	RANGE		=		(HI-LO)
	COUNTSIZE   =		RANGE

.data
; introduction
	intro_1		BYTE		"Hello, welcome to Randomsort - programmed by Riley Ovenshire.",13,10,0
	intro_2		BYTE		"This program will generate and sort 200 random integers, as well as provide additional data on those integers.",0


; fill randomized array
	randArray	DWORD		ARRAYSIZE DUP(?)					; uninitialized values - since these will be the randomly generated ints
	randRep		BYTE		"Your random numbers are: ",0


; sort array
	sortedArray	DWORD		ARRAYSIZE DUP(?)
	sortRep		BYTE		"Your sorted numbers are: ",0

; find median
	medianRep	BYTE		"Median: ",0

; count array
	countArray	DWORD		ARRAYSIZE DUP(?)					; set to default ARRAYSIZE, just in case
	countRep	BYTE		"Your respective num count is: ",0

; farewell
	goodbye		BYTE		"Thanks for using Randomsort - goodbye!",0

.code
main PROC
; introduction
	push	OFFSET intro_2										; pushed by reference, intro_2 first to account for LIFO
	push	OFFSET intro_1
	call	introduction										; 4 byte return address pushed to stack
	call	CrLf

; fill array
	call	Randomize											; generate random seed
	push	OFFSET randRep
	push	OFFSET randArray
	push	ARRAYSIZE
	call	fillArray

; display random array												
	push	OFFSET randArray									; reference
	push	ARRAYSIZE
	call	displayList
	call	CrLf

; sort array/list
	push	OFFSET sortRep
	push	OFFSET randArray									; reference
	push	ARRAYSIZE
	call	sortArray

; display sorted array											; reference
	push	OFFSET randArray
	push	ARRAYSIZE
	call	displayList

; find median
	push	OFFSET medianRep
	push	OFFSET randArray									; reference of randArray, which is sorted
	push	ARRAYSIZE
	call	displayMedian
	
; calculate counts
	push	OFFSET countRep
	push	OFFSET countArray									; reference
	push	OFFSET randArray
	push	ARRAYSIZE
	call	countList

; display counts
	push	OFFSET countArray
	push	ARRAYSIZE
	call	displayList

; say goodbye
	push	OFFSET goodbye
	call	farewell


	Invoke ExitProcess,0	; exit to operating system
main ENDP
;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: introduction
;
; Description: Introduce the program and programmer, give a quick rundown on what it does.
; 
; Preconditions: None.
; 
; Postconditions: Registers changed (see below), output printed.
; 
; Receives: intro_1 (reference, addr: 0x00406000) and intro_2 (reference, addr: 0x00406040)
; 
; Returns: Prints intro_1 and intro_2 to console. 
; 
; Registers changed: EBP, ESP, EDX
;--------------------------------------------------------------------------------------------------------------------------------------------------

introduction PROC
; Preserve stack pointer, push 4 more bytes onto the stack.
	push	EBP
	mov		EBP, ESP

	mov		EDX, [EBP + 8]									; want to access intro_1 first, so increase EBP 8 and EDX has intro_1
	call	WriteString
	call	CrLf

	mov		EDX, [EBP + 12]									; intro_2
	call	WriteString
	call	CrLf

	pop		EBP

	RET		8

introduction ENDP

;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: fill array
;
; Description: Array is populated by random integers using RandomRange.
;
; Preconditions: Randomize has been called in main, stack is balanced after the introduction call.
;
; Postconditions: Randomized randArray (addr in EDI) has been populated with 200 random ints. 
;
; Receives: Empty randArray with 200 spots.
;
; Returns: Populated randArray.
;
; Registers changed: EAX, ECX, EDI, EBP, ESP, EBX
;--------------------------------------------------------------------------------------------------------------------------------------------------

fillArray PROC
; Preserve stack pointer, push 4 more bytes onto the stack.
	push	EBP
	mov		EBP, ESP

; Preserve used registers
	pushad
	
	mov		ECX, [EBP + 8]									; ARRAYSIZE into ECX
	mov		EDI, [EBP + 12]									; address of randArray into EDI - reference
	mov		EDX, [EBP + 16]
	call	WriteString
	call	CrLf


	

_fillLoop:
	cmp		ECX, 0											; do we have enough ints?
	je		_fillDone

	mov		EAX, HI											; generate random int between range (0, HI-LO+1)
	sub		EAX, LO
	add		EAX, 1

	call	RandomRange
	add		EAX, LO											; guarantees that int is within bounds

	mov		[EDI], EAX										; put random value from EAX into given memory location pointed to by EDI
	add		EDI, 4											; point to next DWORD value
	loop	_fillLoop

_fillDone:
	popad
	pop		EBP
	ret		8

fillArray ENDP

;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: sort list/array
; Description: Procedure is passed randArray and returns that array, sorted
;
; Preconditions: randArray must be populated and stored to memory
;
; Postconditions: returns randArray, but sorted in ascending order
;
; Receives: unsorted randArray by reference (addr: 0x004060AF)
;
; Returns: sorted randArray
;
; Registers changed: EBP, ESP, ECX, ESI, EBX, EAX
;--------------------------------------------------------------------------------------------------------------------------------------------------
sortArray PROC
    ; Preserve stack pointer, push 4 more bytes onto the stack.
    push    EBP
    mov     EBP, ESP

    ; Preserve used registers
    pushad
    mov     ECX, [EBP + 8]									; ARRAYSIZE into ECX
    mov     EDI, [EBP + 12]									; address of randArray into EDI - reference
    mov     ESI, ECX										; save size to ESI

	call	CrLf
	mov		EDX, [EBP + 16]
	call	WriteString
	call	CrLf

_sortLoop:
    xor     EBX, EBX										; clear EBX	- EBX indicates if a swap is needed							
    cmp     ESI, 1											; do we need to sort?
    jle     _doneSorting

	dec		ESI
    mov     ECX, ESI										; iterates over all but the last element
    mov     EDI, [EBP + 12]

_compareLoop:
    cmp     ECX, 0											; do we need to make comparisons?
    jle     _checkSwap

    mov     EAX, [EDI]										; get element
    cmp     EAX, [EDI + 4]									; compare element stored in EAX with next in list
    jg      _swapElements

    add     EDI, 4											; move on and reduce counter
    dec     ECX
    jmp     _compareLoop

_swapElements:
    mov     EBX, [EDI + 4]									; put larger element into EBX and move smaller value to that spot from EAX
    mov     [EDI + 4], EAX
    mov     [EDI], EBX										; larger becomes new current
    mov     EBX, 1											; EBX indicates if a swap is needed
    add     EDI, 4
    dec     ECX
    jmp     _compareLoop

_checkSwap:
     cmp     EBX, 0
     jne     _sortLoop

_doneSorting:
     popad
     pop     EBP
     ret     8
sortArray ENDP

;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: display median
;
; Description: Procedure takes sorted randArray, divides it by 2 to determine parity. If odd, reports median. If even, takes num, adds with previous element
;					and returns the average, rounded, which would be the median in that scenario.
;
; Preconditions: randArray must be sorted and passed as a parameter, ARRAYSIZE must be passed.
;
; Postconditions: Returns the median output.
;
; Receives: randArray sorted, string to declare median.
;
; Returns: median value
;
; Registers changed: EBP, ESP, EAX, EBX, ECX, ESI
;--------------------------------------------------------------------------------------------------------------------------------------------------

displayMedian PROC
; Preserve stack pointer, push 4 more bytes onto the stack.
    push    EBP
    mov     EBP, ESP

; Preserve used registers
    pushad

	call	CrLf
	mov		EDX, [EBP + 16]
	call	WriteString

	mov		EAX, [EBP + 8]									; ARRAYSIZE into EAX
	mov		ESI, [EBP + 12]									; address of randArray into ESI - reference

	xor		EDX, EDX										; clear EDX
	mov		EBX, 2											; divisor 2 to check middle index, store in ECX
	div		EBX
	mov		ECX, EAX																				

_median:
	add		ESI, 4											; take middle and next
	loop	_median

	cmp		EDX, 0
	jnz		_oddAmt

	mov		EAX, [ESI - 4]									; past and current b/c we have even nums
	add		EAX, [ESI]										; find avg, which is median
	mov		EDX, 0
	mov		EBX, 2
	div		EBX
	call	WriteDec
	call	CrLf
	jmp		_medianDone


_oddAmt:
	mov		EAX, [ESI]										; odd ARRAYSIZE, so we have already found the middle index
	call	WriteDec
	call	CrLf

_medianDone:
	popad													; restore registers
	pop		EBP
	call	CrLf
	ret		8

displayMedian ENDP

;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: display list
;
; Description: Printing procedure to display the contents of a particular array - randArray or countArray. Uses a loop to print each element. 
;
; Preconditions: Must be called with an array and ARRAYSIZE on the stack.
;
; Postconditions: Returns listed elements of an array, 10 rows of 20 elements.
;
; Receives: ARRAYSIZE and array to be displayed.
;
; Returns: Output into console.
;
; Registers changed: EBP, ESP, ECX, EDI, EBX
;--------------------------------------------------------------------------------------------------------------------------------------------------

displayList PROC
; Preserve stack pointer, push 4 more bytes onto the stack.
	push	EBP
	mov		EBP, ESP

; Preserve used registers
	pushad

	mov		ECX, [EBP + 8]									; ARRAYSIZE into ECX
	mov		EDI, [EBP + 12]									; address of array into EDI - reference



_writeLoop:
	mov		ESI, EDI										; point to first address of randArray
	mov		EBX, 0											; use EBX to keep track of elements per line				

_writing:
	cmp		ECX, 0
	je		_doneWrite

	mov		EAX, [ESI]										; find and write each element
	call	WriteDec
	mov		AL, SPACE										; use constant
	call	WriteChar
	add		ESI, 4
	add		EBX, 1
	
	cmp		EBX, 20											; if EBX = 20, time for a new line
	je		_newLine

	loop	_writing

_newLine:
	call	CrLf
	mov		EBX, 0											; reset new line
	dec		ECX
	jmp		_writing

_doneWrite:
	popad
	pop		EBP
	ret		8

displayList ENDP


;--------------------------------------------------------------------------------------------------------------------------------------------------
; Name: count list
;
; Description: Procedure takes randArray as input, counts the number of times each element appears, then copies those counts into countArray and returns it.
;
; Preconditions: randArray must be sorted, countArray must be declared
;
; Postconditions: countArray is populated, randArray is passed
;
; Receives: randArray, countArray, ARRAYSIZE as parameters
;
; Returns: populated countArray
;
; Registers changed: EBP, ESP, EBX, ECX, ESI, EAX
;
;
; Wanted to give a thank you to TAs Anh Nguyen and Devon Braner for the help here. For whatever reason, I still could not get to remove the 0s that are surrounding the count,
;	but there are correct counts for the digits that are displayed. I'm beyond frustrated with it but am willing to take the point loss.
;
;--------------------------------------------------------------------------------------------------------------------------------------------------
countList PROC
; Preserve stack pointer, push 4 bytes onto the stack
	push	EBP
	mov		EBP, ESP

; Preserve used registers
	pushad
	 
    mov     ECX, [EBP + 8]							; number of elements in the array
    mov     ESI, [EBP + 12]							; randArray - input
    mov     EDI, [EBP + 16]							; countArray - output			

	mov		EDX, [EBP + 20]
	call	WriteString
	call	CrLf

	mov		EBX, 0									; start with 0 for countArray

_countLoop:
	cmp		ECX, 0
	je		_countEnd								; when we have looped through everything, we are done.

	
	mov		EAX, [ESI]								; EAX = the current value we are checking
	
	mov		EBX, [EDI + EAX*4]						; increment count for value in array, EAX multiplied for DWORD size
	add		EBX, 1
	mov		[EDI + EAX*4], EBX								
	
	add		ESI, 4									; next element
	loop	_countLoop

	inc		EBX										; if we find a match, increment the count
	add		EDI, 4									; increment pointer to next value in randArray
	dec		ECX


_countEnd:
	popad
	pop		EBP
	RET		8


countList ENDP

;----------------------------------------------------------------------------------------------------------------------
farewell PROC
	push	EBP
	mov		EBP, ESP

	call	CrLf
	mov		EDX, [EBP + 8]								
	call	WriteString
	call	CrLf
	
	pop		EBP

	RET		12

farewell ENDP

END main
