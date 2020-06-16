"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter
        # register is where you store what you retrieved from ram(memory)
        self.register = [0] * 8 # variable R0-R7
        # ram is running memory
        self.ram = [0] * 256 # ram is memory

    def ram_read(self, address):
        # Memory_Address_Register = MAR
        # MAR

        # takes address and returns the value at the address
        return self.ram[address]
    
    def ram_write(self, value, address):
        # Memory_Data_Register = MDR
        
        # takes an address and a value to write to it
        self.ram[address] = value



    def load(self):
        """Load a program into memory."""

        # sets up a way to read the program being passed in by a user
        filename = sys.argv[1]
        print("filename", filename)


        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split("#")
            
                try:
                    value = int(line[0], 2)
                
                except ValueError:
                    continue

                self.ram[address] = value



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
        running = True

        while running:
            # instruction register
            ir = self.ram[self.pc]
            
            if ir == self.ram[0]:
                # arranges data from bucket
                # where will you put it in your pocket?
                # this is putting it in your pocket
                # "where" is the reg_num: it is  the indice of the reg array
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.register[reg_num] = value
                self.pc += 3
            
            # print instruction
            elif ir == self.ram[3]: 
                reg_num = self.ram[self.pc + 1]
                print(self.register[reg_num])
                self.pc += 2
            
            elif ir == self.ram[5]:
                running = False
                self.pc += 1
            
            else:
                print(f'Unknown instruction{ir} at address {self.pc}')
                sys.exit(1)

