"""CPU functionality."""

import sys

#TODO: use 
op_LDI = 0b10000010
op_PRN = 0b01000111
op_HLT = 0b00000001
op_MUL = 0b10100010
op_ADD = 0b10100000
op_PUSH = 0b01000101
op_POP = 0b01000110
op_CALL = 0b01010000
op_RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self): #TODO
        """Construct a new CPU."""
        self.pc = None #PROGRAM COUNTER
        ir = None
        self.ram = [None] * 256
        self.reg = [None] * 8
        IM = 5
        IS = 6
        self.SP = 7
        self.reg[self.SP] = 0xF4 #Initialie SP
        self.running = None #TODO refactor
        self.branchtable = {}
        self.branchtable[op_LDI] = self.ldi
        self.branchtable[op_PRN] = self.prn
        self.branchtable[op_HLT] = self.hlt
        self.branchtable[op_ADD] = self.add
        self.branchtable[op_MUL] = self.mul
        self.branchtable[op_PUSH] = self.push
        self.branchtable[op_POP] = self.pop
        self.branchtable[op_CALL] = self.call
        self.branchtable[op_RET] = self.ret
        

    def load_hardcoded(self):
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    
    def load(self, load_file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:


        # if len(sys.argv) != 2:
        #     print('usage: compy.py filename')
        #     sys.exit(1)

        try:
            address = 0

            # with open(sys.argv[1]) as f:
            with open(load_file) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n,2)
                    except ValueError:
                        print(f"Invalid number '{n}''")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: '{load_file}'")
            sys.exit(2)

        # breakpoint()

    def call(self):
        # goto line in current step minus 2

        # store pc + 2 in stack to return later
        self.ram_write(self.reg[self.SP],self.pc+2)

        # get addy from register corresponding to PC+1
        self.pc = self.reg[self.ram_read(self.pc+1)]

        
    def ret(self):
        # pop and goto addy from stack, setting pc to that addy 
        # return_addy = self.ram_read(self.reg[self.SP])
        # breakpoint()
        self.pc = self.ram_read(self.reg[self.SP])

        #incremeent stack pointer
        self.reg[self.SP] += 1

    

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self):
        self.reg[self.ram_read(address = self.pc + 1)] = self.ram_read(address=self.pc+2)
        self.pc += 3

    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def hlt(self):
        self.running = False

    def mul(self):
        # self.reg[self.ram_read(self.pc + 1)] = self.reg[self.ram_read(self.pc+1)]*self.reg[self.ram_read(self.pc+2)]
        # self.pc += 3

        self.alu('MUL',self.ram.read(self.pc+1),self.ram.read(self.pc+2))
        self.pc += 3

    def add(self):
        # self.reg[self.ram_read(self.pc + 1)] = self.reg[self.ram_read(self.pc+1)]*self.reg[self.ram_read(self.pc+2)]
        # self.pc += 3
        # print('hey')
        # breakpoint()
        self.alu('ADD',self.ram_read(self.pc+1),self.ram_read(self.pc+2))
        self.pc += 3

    def push(self):
        # decrement SP
        # breakpoint()
        self.reg[self.SP] -= 1
        #value to push
        value = self.reg[self.ram[self.pc+1]]
        #push value to slot
        self.ram_write(address = self.reg[self.SP], value=value )
        self.pc += 2

    def pop(self):
        # pop value from top of stack / @SP
        value = self.ram[self.reg[self.SP]]
        # assign value to register at PC+1
        self.reg[self.ram[self.pc + 1]] = value

        # increment SP and PC
        self.reg[self.SP] += 1
        self.pc += 2

    def run(self): #TODO
        """Run the CPU."""
        self.running = True
        self.pc = 0

        while self.running:
            ir = self.ram[self.pc]

            try:
                self.branchtable[ir]()
                # breakpoint()
            except Exception:
                print(f"Unknown instruction")
                breakpoint()



    def ram_read(self, address): #TODO
        """ 
        should accept the address to read and return the value stored there.
        """
        if  0 <= address <= 255:
            return self.ram[address]
        else:
            print('Invalid address')
            return None

    def ram_write(self, address,value): #TODO
        self.ram[address] = value
