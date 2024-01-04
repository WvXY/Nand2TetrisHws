// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@sum    //reset
M=0

@R2
M=0

@R1
D=M

@25     //R1=0: R2=0
D;JEQ

@12     //if R1<0: keep i positive
D;JGT

@i
M=-D

@i
M=D

@sum
D=M

@R0
D=D+M

@sum
M=D

@i
M=M-1
D=M

@14     //Loop
D;JGT

@sum
D=M

@R2
M=D

@29
0;JMP