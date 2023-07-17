TITLE Project 4 - Nested Loops and Procedures  (Proj3_ovenshir.asm)

; Author: Riley Ovenshire
; Last Modified: 2/26/2023
; OSU email address: ovenshir@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:  4               Due Date: 2/26/2023 @ 12:00 AM
; Description: Program takes a number from a user between [1, 200] and shows them that amount of prime numbers. 

INCLUDE Irvine32.inc

UPPERLIMIT = 200
LOWERLIMIT = 1
RESETDIV = 2

;_________________________________________________________________________________________________________________________________________________________________

.data
; introduction - names and rules
	intro		BYTE    "Hello, welcome to PrimeCalc by Riley Ovenshire.",0
	rules		BYTE	"You will soon enter the amount of primes you would like to see. Just keep it from 1 to 200 - don't overwork me here.",0
	
; getUserData
	prompt		BYTE	"Please enter the amount of prime integers that you would like to see: ",0
	userAmt		DWORD	?					; amount of primes to be entered by user

; validate
	oor			BYTE	"Slow down champ, you're out of range. Keep it between 1 and 200. ",0

; display nums
	testnum		DWORD	1					; number to be tested as a prime
	stornum		DWORD	?					; tested number to be stored
	divnum		DWORD	1					; number that acts as a divisor
	space		DWORD	"   ",0				; each space is word 12 bytes (I think?) b/c they're counted by char
	primeAmt	DWORD	0					; count of primes found/arrayCount integer to keep track


; farewell
	goodbye		BYTE	"Congratulations, you have been blessed with the knowledge of primes. Farewell.",0
;_________________________________________________________________________________________________________________________________________________________________

.code
main PROC

	call	introduction
	call	getUserData
	call	showPrimes
	call	farewell
	

	Invoke ExitProcess,0	; exit to operating system
main ENDP

;____________________________________________________________________

introduction PROC

; procedure description: Procedure to introduce program and programmer.
; preconditions: intro and prompt are strings that introduce program and the number prompt
; postconditions: EDX changed
; receives: n/a
; returns: Intro message to output.

	mov		EDX, OFFSET intro
	call	WriteString
	call	CrLf

	mov		EDX, OFFSET rules
	call	WriteString
	call	CrLf

	ret

introduction ENDP

;____________________________________________________________________

getUserData PROC
; procedure description: Takes an integer amount from the user, shows that amount of primes. 
; preconditions: introduction needs to successfully execute.
; postconditions: EAX, EDX changed and userAmt global variable is assigned
; receives: n/a
; returns: user input values for global variable userAmt

; Prompt the user to enter the amount of prime numbers that they would like to see.
	mov		EDX, OFFSET prompt
	call	WriteString

_getNums:
; User enters numbers, saved to global variable userAmt
	call	ReadDec
	mov		userAmt, EAX

	call validate					; immediately call validate subproc to check input

	ret


getUserData ENDP


validate PROC							; subprocedure for validation
; procedure description: Validates that user input is within range [1, 200].
; preconditions: 1 <= userAmt <= 200
; postconditions: If userAmt is validated, the program continues to showPrimes.
; receives: userAmt, UPPERLIMIT, LOWERLIMIT
; returns: Valid primes.
		
	cmp		userAmt, LOWERLIMIT				; is userAmt less than 1?
	jl		_outOfRange

	cmp		userAmt, UPPERLIMIT				; is userAmt greater than 200?
	jg		_outOfRange

	ret

_outOfRange:								; range error
	mov		EDX, OFFSET oor
	call	WriteString
	call	CrLf
	jmp		getUserData

	ret

validate ENDP

;____________________________________________________________________

showPrimes PROC
; procedure description: Procedure displays given amount of primes.
; preconditions: given amount of primes have been collected in variable userAmt
; postconditions: list of primes is written to output, EAX is changed, EDX is changed
; receives: Number values from nested loop.
; returns: Prime to output.
	
	mov		ECX, userAmt					; start by setting the loop counter to be userAmt

_userAmtLoop:
	inc		testnum							; generate next prime candidate
	mov		EAX, testnum					; put num in EAX
	mov		stornum, EAX					; preserve it in failsafe variable
	mov		EBX, divnum

	xor		EDX, EDX						; EDX must be set to 0
	call	isPrime

	cmp		EDX, 0							; did isPrime return a zero? do it again.
	jz		_userAmtLoop

	mov		EDX, OFFSET testnum
	call	WriteDec
	mov		EDX, OFFSET space
	call	WriteString						; write the prime and space

	loop	_userAmtLoop

_breakLoop:
	ret

showPrimes ENDP


isPrime PROC							; subprocedure for adding primes
; procedure description: Check numbers to see if they're prime.
; preconditions: Must be called by _userAmtLoop.
; postconditions: Adds valid prime values to list.
; receives: candidate value (testnum) from showPrimes
; returns: Prime numbers - prints them as an array.

	cmp		EAX, 2							; special case for 2, since it is the first prime
	je		_twoOrThree
	cmp		EAX, 3							; special case for 3, since we were told we could hardcode first two primes
	je		_twoOrThree

	
_divisorLoop:
	mov		EDX, 0							; clear EDX for every operation
	inc		divnum
	mov		EAX, testnum
	mov		EBX, divnum						; divisor in EBX
	div		EBX								; divide EAX by divnum

	cmp		EDX, 0							; if there is not a remainder, break loop
	jz		_break
	
	cmp		EAX, divnum						; if the result in EAX is less than any other factor than 2, we know the number is prime (do not have to check factors greater than half)
	jle		_isPrime

							
	
	jmp		_divisorLoop					; there could still be a factor other than divnum's default(2), so check again


_twoOrThree:
	mov		EDX, 1							; manually setting EDX for exceptions
	ret

_isPrime:
	mov		EAX, stornum	
	mov		EBX, 1							; reset divisor
	mov		divnum, EBX
	ret

_break:
	mov		EBX, 1							; reset divisor
	mov		divnum, EBX
	ret

isPrime ENDP

;____________________________________________________________________

farewell PROC
; procedure description: Displays a goodbye message to the user. 
; preconditions: Program executed correctly by showing all primes for userAmt.
; postconditions: EDX changed
; receives: n/a
; returns: n/a

	call	CrLf
	mov		EDX, OFFSET goodbye
	call	WriteString
	ret

farewell ENDP

END main
