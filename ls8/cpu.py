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
            CALL: self.handle_call,
            HLT: self.handle_hlt,
            LDI: self.handle_ldi,
            MUL: self.handle_mul,
            POP: self.handle_pop,
            PRN: self.handle_prn,
            PUSH: self.handle_push,
            RET: self.handle_ret
        }
        
        
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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    # def run(self):
    #     """Run the CPU."""

    #     running = True

    #     while running:
    #         # instruction register
    #         ir = self.ram[self.pc]
            
    #         # look at op codes
    #         if ir == "LDI":
    #             # arranges data from bucket
    #             # where will you put it in your pocket?
    #             # this is putting it in your pocket
    #             # "where" is the reg_num: it is  the indice of the reg array
    #             reg_num = self.ram[self.pc + 1]
    #             value = self.ram[self.pc + 2]
    #             self.reg[reg_num] = value
    #             self.pc += 3
            
    #         # print instruction
    #         elif ir == "PRN": 
    #             reg_num = self.ram[self.pc + 1]
    #             print(self.reg[reg_num])
    #             self.pc += 2
            
    #         elif ir == "MUL":
    #             self.handle_mul()

    #         elif ir == "HLT":
    #             running = False
    #             self.pc += 1
            
    #         else:
    #             print(f'Unknown instruction{ir} at address {self.pc}')
    #             sys.exit(1)

