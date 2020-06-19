"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        # register is where you store what you retrieved from ram(memory)
        self.reg = [0] * 8 # variable R0-R7
        # ram is running memory
        self.ram = [0] * 256 # ram is memory
        # Set up branch table
        self.branch_table = {
            ADD: self.handle_add,
            AND: self.handle_and,
            CALL: self.handle_call,
            CMP: self.handle_cmp,
            HLT: self.handle_hlt,
            JEQ: self.handle_jeq,
            JMP: self.handle_jmp,
            JNE: self.handle_jne,
            LDI: self.handle_ldi,
            MUL: self.handle_mul,
            NOT: self.handle_not,
            OR: self.handle_or,
            POP: self.handle_pop,
            PRN: self.handle_prn,
            PUSH: self.handle_push,
            RET: self.handle_ret,
            SHL: self.handle_shl,
            XOR: self.handle_xor
        }
        self.fl = 0b00000000
        
        # stack pointer is in register 7
        self.SP = 7
        self.reg[self.SP] = 0xf4

    def ram_read(self, address):
        # Memory_Address_Register = MAR
        # MAR

        # takes address and returns the value at the address
        return self.ram[address]
    
    def ram_write(self, value, address):
        # Memory_Data_Register = MDR
        
        # takes an address and a value to write to it
        self.ram[address] = value

    def handle_call(self):
        # set the address to return to
        return_addy = self.pc + 2

        # push onto the stack
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = return_addy

        # get the address to call
        reg_num = self.ram[self.pc + 1]
        sub_addy = self.reg[reg_num]

        # call it
        self.pc = sub_addy

    def handle_ret(self):
        # get the address of the thing to remove
        return_index = self.ram[self.pc + 1]

        # sets the value to the top of the stack with the pointer
        self.reg[return_index] = self.ram[self.reg[self.SP]]

        # increment the pointer
        self.reg[self.SP] += 1

        # return the counter to where we were before the call(after the call instruction)
        self.pc = self.reg[return_index]

    def handle_add(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("ADD", reg_1, reg_2)
        self.pc += 3

    def handle_push(self):
        # decrement the SP
        self.reg[self.SP] -= 1

        # get the value we want to store from the register
        reg_num = self.ram_read(self.pc + 1)
        # print('Register', reg_num)
        value = self.reg[reg_num]

        # get the place to store it
        top_of_stack = self.reg[self.SP]

        # store it
        # self.ram_write(value, top_of_stack) same as below
        self.ram[top_of_stack] = value

        # increment the PC
        self.pc += 2

    def handle_pop(self):
        # check if stack is empty
        if self.reg[self.SP] == 0xf4:
            return print('The stack is empty')
        
        # get the location of the value to pop
        value_index = self.ram_read(self.pc + 1)

        # sets the value to the top of the stack with the pointer
        self.reg[value_index] = self.ram[self.reg[self.SP]]

        # increment the pointer
        self.reg[self.SP] += 1

        # increment the PC
        self.pc += 2


    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3

    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def handle_mul(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("MUL", reg_1, reg_2)
        self.pc += 3

    def handle_hlt(self):
        self.pc += 1
        self.running = False
        return self.running
    
    def load(self):
        """Load a program into memory."""

        # sets up a way to read the program being passed in by a user
        filename = sys.argv[1]
        print("filename", filename)

        address = 0
        with open(filename) as f:
            for line in f:
                line = line.split("#")
            
                try:
                    value = int(line[0], 2)
                
                except ValueError:
                    continue

                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        register_a = self.reg[reg_a]
        register_b = self.reg[reg_b]
        if op == "ADD":
            register_a += register_b
        #elif op == "SUB": etc
        elif op == "MUL":
            register_a *= register_b
        elif op == "CMP":
            if register_a > register_b:
                # 100
                self.fl = 0b00000100
            elif register_a < register_b:
                # 010
                self.fl = 0b00000010
            elif register_a == register_b:
                # 001
                self.fl = 0b00000001
            else:
                # 000
                self.fl = 0b00000000
        elif op == "AND":
            for i in range(len(register_a) - 1):
                register_a[i] = register_a[i] * register_b[i]
        elif op == "NOT":
            for each in register_a:
                if each == 0:
                    each = 1
                else:
                    each = 0
        elif op == "OR":
            for i in range(len(register_a) - 1):
                if register_a[i] and register_b[i] == 0:
                    register_a[i] = 0
                else:
                    register_a[i] = 1
        elif op == "XOR":
            for i in range(len(register_a) - 1):
                if register_a[i] == register_b[i]:
                    register_a[i] = 0
                else:
                    register_a[i] = 1
        elif op == "SHL":
            

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # instrution register
        self.running = True
        while self.running:
            # grab the current instruction
            ir = self.ram[self.pc]
            # if we have an instruction that matches run it
            if ir in self.branch_table:
                self.branch_table[ir]()
            # if not print error
            else:
                print(f'Unknown instruction: {ir}, at address PC: {self.pc}')
                sys.exit(1)

### Sprint Challenge ###


    def handle_cmp(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("CMP", reg_1, reg_2)
        self.pc += 3
        
    def handle_jeq(self):
        if self.fl == 0b00000001:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else: 
            self.pc += 2

    def handle_jmp(self):
            self.pc = self.reg[self.ram[self.pc + 1]]

    def handle_jne(self):
        if self.fl != 0b00000001:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else: 
            self.pc += 2
### STRETCH ###
    def handle_and(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("AND", reg_1, reg_2)
        self.pc += 3
    
    def handle_not(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("NOT", reg_1, reg_2)
        self.pc += 2

    def handle_or(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("OR", reg_1, reg_2)
        self.pc += 3

    def handle_xor(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)

        self.alu("XOR", reg_1, reg_2)
        self.pc += 3