// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(END)
@KBD
D=M

@WHITE
D;JEQ
@BLACK
D;JNE

(WHITE)
@SCREEN
D=A
(LOOP1)
A=D
M=0
@j
D=D+1
M=D

@KBD
D=A-D
@END
D;JLE

@j
D=M
@LOOP1
0;JMP


(BLACK)
@SCREEN
D=A
(LOOP2)
A=D
M=-1
@i
D=D+1
M=D

@KBD
D=A-D
@END
D;JLE

@i
D=M
@LOOP2
0;JMP