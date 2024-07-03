class CPU():
    def __init__(self, bit_width, autoloop_block = True):
        self.bit_width = bit_width
        self.registers = memory()
        self.registers.update("CARRY", 0)
        self.registers.update("MEMAD", 0)
        if autoloop_block == True:
            self.autoloop_block = True
        else:
            self.autoloop_block = False
        self.memory = memory()
        self.program = None
        self.execution_point = None
        self.execution_log = None
    def load_program(self, program):
        self.program = program
        self.execution_log = []
        self.execution_point = ("START", 0)
    def get_execution_log(self):
        """
        Returns the full execution log as a list
        The execution log looks like:
        ((True/False(Did instructions get executed), (instruction(prefix), involved_parameters(dict), changed_parameters(dict), starting_execution_point(block_id, num), new_execution_point(block_id, num)))
        """
        return(self.execution_log)
    def get_execution_point(self):
        """
        Returns the current execution point(will be used upon next execution step)
        Format: (block_id, num)
        """
        return(self.execution_point)
    def step_single_instruction(self, return_info = True):
        if self.program == None:
            AttributeError("Program has not been loaded")
        else:
            pass
        if self.execution_point == ("END", 0):
            return(False)
        else:
            starting_execution_point = self.execution_point
            block_id = starting_execution_point[0]
            instruction_number = starting_execution_point[1]
            try:
                instruction, parameters = self.program.get_instruction(block_id, instruction_number, self.autoloop_block)
            except ValueError as e:
                raise ValueError("Unable to get instruction at execution point "+str(self.execution_point)+" because of reason: "+str(e))
            if instruction == "END":
                involved_parameters = ()
                changed_parameters = {}
                # Reserved block ID for halting execution
                new_execution_point = ("END", 0)
            elif instruction == "JMP":
                # Note that for single parameter instructions the ASM parser will only output the relevant string and NOT a tuple!!!
                jump_block_ID = parameters
                involved_parameters = {}
                involved_parameters["Jump target"] = ("Block ID", jump_block_ID)
                new_execution_point = (jump_block_ID, 0)
                self.execution_point = new_execution_point
                changed_parameters = {}
            elif instruction == "JNE":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                jump_block_ID = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Jump target"] = ("Block ID", jump_block_ID)
                if reg_1_content != reg_2_content:
                    new_execution_point = (jump_block_ID, 0)
                else:
                    new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
                changed_parameters = {}
            elif instruction == "JIE":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                jump_block_ID = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Jump target"] = ("Block ID", jump_block_ID)
                if reg_1_content == reg_2_content:
                    new_execution_point = (jump_block_ID, 0)
                else:
                    new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
                changed_parameters = {}
            elif instruction == "CMP":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_4 = parameters[3]
                reg_5 = parameters[4]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                reg_4_content = self.registers.get(reg_4)
                reg_5_content = self.registers.get(reg_5)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                involved_parameters["Reg_4"] = (reg_4, reg_4_content)
                involved_parameters["Reg_5"] = (reg_5, reg_5_content)
                if reg_1_content == reg_2_content:
                    reg_5_content = reg_3_content
                else:
                    reg_5_content = reg_4_content
                self.registers.update(reg_5, reg_5_content)
                changed_parameters = {}
                changed_parameters["Reg_5"] = (reg_5, reg_5_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "GT":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_4 = parameters[3]
                reg_5 = parameters[4]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                reg_4_content = self.registers.get(reg_4)
                reg_5_content = self.registers.get(reg_5)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                involved_parameters["Reg_4"] = (reg_4, reg_4_content)
                involved_parameters["Reg_5"] = (reg_5, reg_5_content)
                if reg_1_content > reg_2_content:
                    reg_5_content = reg_3_content
                else:
                    reg_5_content = reg_4_content
                self.registers.update(reg_5, reg_5_content)
                changed_parameters = {}
                changed_parameters["Reg_5"] = (reg_5, reg_5_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "LT":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_4 = parameters[3]
                reg_5 = parameters[4]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                reg_4_content = self.registers.get(reg_4)
                reg_5_content = self.registers.get(reg_5)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                involved_parameters["Reg_4"] = (reg_4, reg_4_content)
                involved_parameters["Reg_5"] = (reg_5, reg_5_content)
                if reg_1_content < reg_2_content:
                    reg_5_content = reg_3_content
                else:
                    reg_5_content = reg_4_content
                self.registers.update(reg_5, reg_5_content)
                changed_parameters = {}
                changed_parameters["Reg_5"] = (reg_5, reg_5_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "ADD":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                carry = self.registers.get("CARRY")
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                involved_parameters["CARRY"] = ("CARRY", carry)
                result = reg_1_content + reg_2_content
                # Remember to extract the overflow first before truncating the result
                carry = result//(2**self.bit_width)
                result = result % (2**self.bit_width)
                reg_3_content = result
                # Note that this operation overrides any attempt to use REG_3 to overwrite the overflow in CARRY
                if reg_3 == "CARRY":
                    reg_3_content = carry
                else:
                    pass
                self.registers.update(reg_3, reg_3_content)
                self.registers.update("CARRY", carry)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                changed_parameters["CARRY"] = ("CARRY", carry)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "MUL":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                result = reg_1_content * reg_2_content
                result = result % (2**self.bit_width)
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "SHUP":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                result = reg_1_content << reg_2_content
                result = result % (2**self.bit_width)
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "SHDO":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                result = reg_1_content >> reg_2_content
                result = result % (2**self.bit_width)
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "NOT":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                result = bitwise_negate(reg_1_content, self.bit_width)
                reg_2_content = result
                self.registers.update(reg_2, reg_2_content)
                changed_parameters = {}
                changed_parameters["Reg_2"] =(reg_2,  reg_2_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "AND":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                result = reg_1_content & reg_2_content
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "OR":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                result = reg_1_content | reg_2_content
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "XOR":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_3 = parameters[2]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                reg_3_content = self.registers.get(reg_3)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                involved_parameters["Reg_3"] = (reg_3, reg_3_content)
                # A XOR is equal to (X & ~Y) | (~X & Y)
                first_term = reg_1_content & bitwise_negate(reg_2_content, self.bit_width)
                second_term = bitwise_negate(reg_1_content, self.bit_width) & reg_2_content
                result = first_term | second_term
                reg_3_content = result
                self.registers.update(reg_3, reg_3_content)
                changed_parameters = {}
                changed_parameters["Reg_3"] = (reg_3, reg_3_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "LOAD":
                reg_1 = parameters
                memory_address = self.registers.get("MEMAD")
                memory_content = self.memory.get(str(memory_address))
                reg_1_content = self.registers.get(reg_1)
                involved_parameters = {}
                involved_parameters["MEMAD"] = ("MEMAD", memory_address)
                involved_parameters["Memory"] = memory_content
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                reg_1_content = memory_content
                self.registers.update(reg_1, reg_1_content)
                changed_parameters = {}
                changed_parameters["Reg_1"] = (reg_1, reg_1_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "STORE":
                reg_1 = parameters
                memory_address = self.registers.get("MEMAD")
                memory_content = self.memory.get(memory_address)
                reg_1_content = self.registers.get(reg_1)
                involved_parameters = {}
                involved_parameters["MEMAD"] = ("MEMAD", memory_address)
                involved_parameters["Memory"] = memory_content
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                self.memory.update(str(memory_address), reg_1_content)
                changed_parameters = {}
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "SET":
                reg_1 = parameters[0]
                data = parameters[1]
                reg_1_content = self.registers.get(reg_1)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Data"] = data
                result = data % (2**self.bit_width)
                reg_1_content = result
                self.registers.update(reg_1, reg_1_content)
                changed_parameters = {}
                changed_parameters["Reg_1"] = (reg_1, reg_1_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "COPY":
                reg_1 = parameters[0]
                reg_2 = parameters[1]
                reg_1_content = self.registers.get(reg_1)
                reg_2_content = self.registers.get(reg_2)
                involved_parameters = {}
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                involved_parameters["Reg_2"] = (reg_2, reg_2_content)
                reg_2_content = reg_1_content
                self.registers.update(reg_2, reg_2_content)
                changed_parameters = {}
                changed_parameters["Reg_2"] =(reg_2,  reg_2_content)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "SETMEMAD":
                data = parameters
                memory_address = self.registers.get("MEMAD")
                involved_parameters = {}
                involved_parameters["Data"] = data
                involved_parameters["MEMAD"] = ("MEMAD", memory_address)
                memory_address = data
                self.registers.update("MEMAD", memory_address)
                changed_parameters = {}
                changed_parameters["MEMAD"] = ("MEMAD", memory_address)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            elif instruction == "ADDMEMAD":
                reg_1 = parameters
                memory_address = self.registers.get("MEMAD")
                reg_1_content = self.registers.get(reg_1)
                involved_parameters = {}
                involved_parameters["MEMAD"] = ("MEMAD", memory_address)
                involved_parameters["Reg_1"] = (reg_1, reg_1_content)
                result = memory_address + reg_1_content
                memory_address = result
                self.registers.update("MEMAD", memory_address)
                changed_parameters = {}
                changed_parameters["MEMAD"] = ("MEMAD", memory_address)
                new_execution_point = (starting_execution_point[0], starting_execution_point[1]+1)
            else:
                #TODO
                #NOTE:involved parameters has the following format "input type/label":registry_name/data/blockid, raw data(registry content/data/bloc_id)
                # changed parameters has the same format
                # Example: "Reg_1": "R_123", 13
                fmt_string = "The instruction "+instruction+" has not been implemented yet."
                error_string = fmt_string.format(instruction = instruction)
                raise NotImplementedError(error_string)
            self.execution_point = new_execution_point
            execution_info = (instruction, involved_parameters, changed_parameters, starting_execution_point, new_execution_point)
            self.execution_log.append(execution_info)
            if return_info == True:
                result = (True, execution_info)
                return(result)
            else:
                return(True)
    def step_multiple_instruction(self, instructions, return_info = True):
        returned_info = []
        for i in range(instructions):
            info = self.step_single_instruction(return_info)
            returned_info.append(info)
        return(returned_info)
    def get_registers(self):
        """
        Returns the current state of the registers as a dictionary
        """
        reg = self.registers.dump()
        return(reg)
    def get_memory(self):
        """
        Returns the current state of the memory as a dictionary
        """
        mem = self.memory.dump()
        return(mem)
            
def bitwise_negate(number, bit_width):
    """Given a number and a bit width, this function will calculate the negated version(bit wise NOT) for said binary string"""
    bin_string = bin(number)[2:len(bin(number))]
    bin_string = bin_string.zfill(bit_width)
    negated_bit_string = ""
    for bit in bin_string:
        if bit == "0":
            negated_bit_string = negated_bit_string + "1"
        else:
            negated_bit_string = negated_bit_string + "0"
    result = int(negated_bit_string, 2)
    return(result)


class memory():
    def __init__(self) -> None:
        self.data = {}
    def update(self, target, content):
        """
        Updates the target's content, creating a new key:value pair if needed
        """
        data = self.data
        data[target] = content
        self.data = data
    def get(self, target):
        """
        Attempts to retrieve the given target's contents
        If the target is not present, a 0 is returned
        """
        if target in self.data.keys():
            return(self.data[target])
        else:
            return(0)
    def dump(self):
        """
        Returns a raw dict of the contents
        """
        return(self.data)
    