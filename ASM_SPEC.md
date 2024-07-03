ASM SPEC 

Memory Model:
There are two read/writable sets of memory: Registers and RAM. Registers are defined by either the program(in which case they will take the form of R_NAME) or are special named registers that are used by the CPU itself. RAM is characterized by being only accessible through special instructions and requiring the preloading of the target numeric address in the RAM by special instructions as well.

In this model of CPU, there are an infinite(or at least until the simulator breaks) amount of registers. All registers are labeled by the prefix of "R_". The section after that serves as a unique identifier for the register. All registers are of the bit width of the CPU.

As of right now there are only 2 special named registers. These registers are CARRY and MEMAD. CARRY at the start of execution is set to 0. It can be overwritten by either intentional register operations or by executing the ADD instruction. After the ADD instruction is executed, CARRY will contain any overflowing carries until the next overwrite happens due to either register operations or another ADD instruction.

MEMAD is the MEMory ADdress register. It is an integer of arbitary length(or at least until the simulator hits it's limit). At the start of execution is is set to 0. It can only be set by the SETMEMAD instruction (which will change it to a static value) and modified by the ADDMEMAD instruction(which can be used to dynamically change the MEMAD value). When the LOAD instruction is executed, it will use the address in MEMAD to select the appropiate RAM word to copy into the target register. MEMAD can not be interacted with by instructions unless otherwise specified.

Instructions:
BLOCK
Usage: BLOCK NAME
Each block of assembly must be preceeded by a BLOCK instruction. Each block declares the start of a uniquely named set of assembly instructions. If the assembly input starts with assembly instructions that are not under a block, they will be removed. Each block declares a label called the Block ID. A Block ID must be globally unique as it will be used to resolve jumps. The Block ID has minimal limitations on it's format. However, certain rules apply:
- The Block ID can not be labeled NO_BLOCK_ID or END as that block ID is reserved internally for use and can not be used in the program.
- The Block ID can not start with the register prefix or be a named register.
- The Block ID can not start with a data prefix
- The block must be parsable(ie please don't shove special characters into the name and make it easy to read)

END
Usage: END
In order to cleanly end program execution, the program must signal it's end by using the END instruction. Once the END instruction is executed, further execution is halted permanently.

JMP
Usage: JMP NAME
The JMP(Jump) instruction is used to perform an unconditional jump into the start of a block of assembly by referring to it's Block ID. This Block ID must exist otherwise processing will fail.

JNE
Usage: JNE REG_1 REG_2 NAME
The JNE(Jump if Not Equal) instruction is used to perform an conditional jump into the start of a block of assembly by comparing the two defined registers and then if the contents of the two registers are not equal execute a jump to the specified Block ID.

JIE
Usage: JIE REG_1 REG_2 NAME
The JNE(Jump If Equal) instruction is used to perform an conditional jump into the start of a block of assembly by comparing the two defined registers and then if the contents of the two registers are  equal execute a jump to the specified Block ID.

CMP
Usage: CMP REG_1 REG_2 REG_3 REG_4 REG_5
The CMP(Compare) instruction is used to detect if two registers(REG_1 and REG_2) are equal. If they are equal, the value in REG_3 is copied to REG_5. Otherwise the value in REG_4 is copied to REG_5.

GT
Usage: GT REG_1 REG_2 REG_3 REG_4 REG_5
The GT(Greater Than) instruction is used to detect if one of the registers is greater than the other(REG_1 > REG_2). If REG_1 is greater than REG_2, the value in REG_3 is copied to REG_5. Otherwise the value in REG_4 is copied to REG_5. 

LT
Usage: LT REG_1 REG_2 REG_3 REG_4 REG_5
The LT(Less Than) instruction is used to detect if one of the registers is greater than the other(REG_1 <> REG_2). If REG_1 is less than REG_2, the value in REG_3 is copied to REG_5. Otherwise the value in REG_4 is copied to REG_5. 

ADD
Usage: ADD REG_1 REG_2 REG_3
The ADD instruction adds the two registers REG_1 and REG_2 as unsigned integers. The portion that fits within the word size of the processor being emulated will be stored into REG_3. Meanwhile, the any carries that propagate out of the word size will be placed into the CARRY special register.
NOTE: This instruction will first write the truncated output to REG_3, and then write the overflow to CARRY. This means that if REG_3 is CARRY, the output will be ignored and only the overflow will be written to CARRY.

MUL
Usage: MUL REG_1 REG_2 REG_3
The MUL(MULtiply) instruction multiplies the two registers REG_1 and REG_2 as unsigned integers. The lower portion that fits into the wordsize will be stored into REG_3. Any overflow will be silently discarded.

SHUP
Usage: SHUP REG_1 REG_2 REG_3
The SHUP(SHift UPwards) instruction bitshifts the value of REG_1 by the amount in REG_2 towards the most significant bit. This is equivalent to a multiplication of REG_1 by a power of 2 defined in REG_2. For example, if REG_2 == 0, REG_1 would be multiplied by 1, if REG_2 == 1, REG_1 would be multiplied by 2, and if REG_2 == 2, REG_1 would be multiplied by 4. Any overflow is silently discarded. The result of this operation is stored into REG_3.

SHDO
Usage: SHDO REG_1 REG_2 REG_3
The SHDO(SHift DOwnwards) instruction bitshifts the value of REG_1 by the amount in REG_2 towards the least significant bit. This is equivalent to a division of REG_1 by a power of 2 defined in REG_2. For example, if REG_2 == 0, REG_1 would be divided by 1, if REG_2 == 1, REG_1 would be divided by 2, and if REG_2 == 2, REG_1 would be divided by 4. Any underflow(ie fractional values) is silently discarded. The result of this operation is stored into REG_3.

NOT 
Usage: NOT REG_1 REG_2
The NOT instruction performs bitwise negation on the value in REG_1 and then stores the result of the operation into REG_2.

AND
Usage: AND REG_1 REG_2 REG_3
The AND instruction performs bitwise AND on the value in REG_1 and REG_2 and then stores the result of the operation into REG_3.

OR
Usage: AND REG_1 REG_2 REG_3
The OR instruction performs bitwise OR on the value in REG_1 and REG_2 and then stores the result of the operation into REG_3.

XOR 
Usage: XOR REG_1 REG_2 REG_3
The XOR instruction performs bitwise XOR on the value in REG_1 and REG_2 and then stores the result of the operation into REG_3.

LOAD 
Usage: LOAD REG_1
The LOAD instruction retrieves the value in RAM at the location indicated by the MEMAD special register and then puts it into REG_1.

STORE
Usage: STORE REG_1
The STORE instruction retrieves the value in REG_1 and then stores it in RAM at the location indicated by the MEMAD special register.

SET
Usage: SET REG_1 DATA
The SET instruction takes the DATA specified in it's line and attempts to set REG_1 to that value. Please note that if the value represented in the DATA field is larger than REG_1 that data loss can occur as the CPU will truncate any overflow.

COPY
Usage: COPY REG_1 REG_2
The COPY instruction takes the value in REG_1 and copies it to REG_2, overwriting whatever data may be present in REG_2.

SETMEMAD
Usage: SETMEMAD DATA
The SETMEMAD(SET MEMory ADdress) instruction directly sets the value stored in the MEMAD special register. This allows the program to access a static memory address in RAM.

ADDMEMAD
Usage: ADDMEMAD REG_1
The ADDMEMAD(ADD MEMory ADdress) instruction allows modification of the MEMAD special register's value. The modification is the addition of the specified register's contents on top of the MEMAD register's current value. Notably, this is currently the ONLY instruction that can use MEMAD as a valid register. If this is done the result is equivalent to multiplying the MEMAD's value by 2, doubling it.

Writing:
- All extraneous spaces are ignored 
Example:
ADD R_1 R_2 R_3
ADD    R_1 R_2    R_3
    ADD R_1 R_2 R_3     
  ADD  R_1   R_2   R_3     
Are all equivalent
- All valid assembly instructions must start with a valid prefix
Example:
BLOCK STEAD
ADD R_1 R_2 R_3
SET R_4 0x00
COPY R_5 R_6
JMP REG_ADD
Are all valid

CPY R_M R_N
SUB R_1 R_2 R_3
DIV R_4 R_5 R_6
INC R_7
Are all invalid
- Registers must either be a special named register or start with R_
Example:
R_1
R_2
R_123
R_09AS
R_qwe
R_6T
R_ZXCV
R_!@#$
R_}{P7
R_R_poi
MEMAD
CARRY
Are all valid and a singular register

register_1
G_7
R1
reg2
Are all invalid custom registers
- Any line that starts with # is a comment and will be ignored
Example:
# MUL R_1 R_2 R_3
#ADD R_0 R_9 R_8
#JIE R_7 JMP_TARGET
Will all be ignored

XOR R_4 R_5 R_6
COPY R_B R_H
Are not comments and will be treated as instructions
- All data must start with 0x, 0d, or 0b prefixes
0x means treat the trailing characters as a hexadecimal integer
0d means treat the trailing characters as a decimal integer
0b means treat the trailing characters as a binary integer
If there are no digits after the prefix, the value is 0
Examples:
0x = 0
0xF = 15
0xf = 15
0x000f = 15
0x01001 = 4097
0xd = 0
0x1 = 1
0x55 = 55
0x0123 = 123
0b = 0
0b111 = 7
0b001101 = 13