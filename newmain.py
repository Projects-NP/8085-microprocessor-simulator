from newfunctions import *


class Simulator:
    def __init__(self):
        self.pc = 0
        self.opcode = None
        self.operand1 = None
        self.operand2 = None
        self.register1 = None
        self.register2 = None
        self.value = None
        self.address = None
        self.label = None
        self.function_dict = {
            'mov': mov,
            'mvi': mvi,
            'lxi': lxi,
            'lda': lda,
            'sta': sta,
            'lhld': lhld,
            'shld': shld,
            'stax': stax,
            'xchg': xchg,
            'add': add,
            'adi': adi,
            'sub': sub,
            'inr': inr,
            'dcr': dcr,
            'inx': inx,
            'dcx': dcx,
            'dad': dad,
            'sui': sui,
            'cma': cma,
            'cmp': cmp,
            # 'set': set,
            # 'out': out,
        }
        self.register_pairs = {'B': ('B', 'C'), 'D': ('D', 'E'), 'H': ('H', 'L')}

    def decode(self, instruction):
        code_list = instruction.upper().split()
        if len(code_list) == 1:
            self.opcode = code_list[0]
        elif len(code_list) == 2:
            self.opcode = code_list[0].upper()
            if self.opcode in ['LXI', 'INX', 'DCX', 'DAD', 'STAX']:
                if code_list[1] in self.register_pairs:
                    self.register1, self.register2 = self.register_pairs[code_list[1]]
            self.operand1 = code_list[1] if code_list[1].isalpha() else None
            self.value = code_list[1] if code_list[1].isdigit() and len(code_list[1]) == 2 else None
            self.address = code_list[1] if len(code_list[1]) == 4 else None
        elif len(code_list) == 3:
            self.opcode = code_list[0]
            if code_list[1] == ':':
                self.address = code_list[2]
                self.label = self.address
            elif code_list[1].isdigit() and len(code_list[1]) == 4:
                self.address = code_list[1]
                self.value = code_list[2]
            elif code_list[2].isdigit() and len(code_list[2]) == 2:
                self.operand1, self.value = code_list[1][:-1], code_list[2]
            elif code_list[2].isdigit() and len(code_list[2]) == 4:
                self.operand1, self.address = code_list[1][:-1], code_list[2]
                if self.operand1 in self.register_pairs:
                    self.register1, self.register2 = self.register_pairs[self.operand1]

            elif code_list[2].isalpha():
                self.operand1, self.operand2 = code_list[1][:-1], code_list[2]

        data = {
            'opcode': self.opcode,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'register1': self.register1,
            'register2': self.register2,
            'value': int(self.value) if self.value else None,
            'address': int(self.address) if self.address else None,
            'label': int(self.label) if self.label else None,
        }
        self.run_instruction(data)
        self.reset_values()

    def reset_values(self):
        self.opcode = None
        self.operand1 = None
        self.operand2 = None
        self.register1 = None
        self.register2 = None
        self.value = None
        self.address = None
        self.label = None

    def run_instruction(self, data):
        opcode = data['opcode'].lower()
        if opcode in self.function_dict:
            if opcode not in ['jc', 'jnc', 'jz', 'jnz', 'jmp']:
                self.function_dict[opcode](data)
            elif opcode in ['jc', 'jnc', 'jz', 'jnz', 'jmp']:
                if flags['carry'] and opcode == 'jc':
                    self.pc = data['address']

        else:
            print("Invalid Instruction")

    def execute(self, start_address, last_address):
        print(start_address, last_address)
        while start_address <= last_address:
            # self.decode(memory[self.pc])
            self.decode(memory[start_address])
            start_address += count_bytes(memory[start_address])

    # read_code_lines -> execute -> decode -> run_instruction
    def read_code_lines(self):
        self.set_memory()
        self.pc = 2000
        global  last_address
        initial_address = self.pc
        last_address = self.pc
        with open("code.txt", 'r') as file:
            for instruction in file:
                opcode = instruction.split()[0]
                # store the instruction in memory
                memory[self.pc] = instruction[:-1].upper() if instruction[
                                                                  -1] == '\n' else instruction.upper()
                last_address = self.pc
                self.pc += count_bytes(opcode)
        self.execute(initial_address, last_address)
        print_values()

    def set_memory(self):
        with open("setmemory.txt", 'r') as file:
            for instruction in file:
                address = instruction.split()[0]
                value = instruction.split()[1]
                memory[int(address)] = value


if __name__ == "__main__":
    simulator = Simulator()
    simulator.read_code_lines()

# updated