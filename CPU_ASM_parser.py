data_prefixes_global = ["0b", "0d", "0x"]
special_named_registers_global = ["CARRY", "MEMAD"]
register_prefix_global = "R_"

class program():
    def __init__(self, assembly_string_lines):
        """
        This function creates a program object which is a set of parsed assembly blocks by the provided lines of assembly.
        This parser performs some basic validation of the provided lines of assembly.
        For example, it ensures that there is a valid "START" block to begin execution and that a block is not defined multiple times in the assembly.
        The parsing does not garantee a lack of runtime errors however.
        For example, if a block of assembly is completed and there is no terminating "END" or a jump to a valid assembly block, the simulated CPU will crash.
        The parser will NOT provide protections against malformed code that can encounter such a situation for example.
        Note that all the parser does is chunk each block of assembly into their own blocks and ensure that the basic minimum ie that there is a START block is present, all jmps go to valid block identifiers, and that all assembly instructions are correctly formatted.
        No garantees are provided regarding the validity, or well formedness, or proper ordering of the assembly instructions.
        Also note that if there are assembly instructions before any block is declared, those assembly instructions will be parsed but will NOT be part of the program.
        """
        # Contains the actual seperate blocks of assembly
        program_instructions = dict()
        # Used to quickly look up and see what blocks there are
        declared_blocks = list()
        # Used to quickly see what blocks are jumped to(and therefore must be present) and which assembly lines use those implied blocks(for error responses)
        jump_blocks_declared = dict()
        # All valid assembly prefixes that are not comments(ie starts with "#")
        valid_prefixes = ["BLOCK", "END",
                          "JMP", "JNE", "JIE",
                          "CMP", "GT", "LT",
                          "ADD", "MUL",
                          "SHUP", "SHDO",
                          "NOT ", "AND", "OR", "XOR ",
                          "LOAD ", "STORE", "SET", "COPY", "SETMEMAD", "ADDMEMAD"]
        # This reserved block ID ensures that if we start in an assembly input that does not start with a block ID, the assembly will get removed from the final result
        current_block_ID = "NO_BLOCK_ID"
        block_assembly_number = 0
        for line_index in range(len(assembly_string_lines)):
            assembly_line = assembly_string_lines[line_index]
            if assembly_line == "":
                pass
            elif assembly_line[0] == "#":
                pass
            else:
                split_line = assembly_line.split()
                assembly_line_parameters = list()
                # Remove all the empty spaces(which will show up as empty strings in the list)
                for string in split_line:
                    if string != "":
                        assembly_line_parameters.append(string)
                if assembly_line_parameters == []:
                    # Check to see if we end up with an empty set of parameters after stripping out all the spaces from the list of fragments
                    pass
                else:
                    # There is at least 1 item which will be our prefix
                    prefix = assembly_line_parameters[0]
                    if prefix not in valid_prefixes:
                        fmt_string = """Invalid prefix found on assembly line {line_index_value}.  The invalid prefix was: "{faulty_prefix}"."""
                        error_string = fmt_string.format(line_index_value = line_index, faulty_prefix = prefix)
                        raise ValueError(error_string)
                    else:
                        if prefix == "BLOCK":
                        # FORM: BLOCK NAME
                        # Declares a new unique block of assembly
                        # Name must not collide with registers (which start with R_ or are one of the few named registers)
                        # Name may be any string that does not contain spaces or new lines
                        # Do be careful though about the extent which you stretch the above
                        # Verify this is not a previously defined block
                        # Add new block to blocks list
                        # Change current block
                        # Verify that this line has the right amount of parameters
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid block declaration with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 2 arguements. Declaration was: {invalid_block_declaration} ."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index,     invalid_block_declaration = assembly_line)
                                raise ValueError(error_string)
                            else:
                                # Extract the block ID
                                block_ID = assembly_line_parameters[1]
                                # Verify the block ID being in valid form and not colliding
                                block_ID_allowed, reason = validate_block_ID(block_ID)
                                if block_ID_allowed == False:
                                    fmt_string = """Encountered invalid block ID in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                # Verify that this block ID is not already used
                                if block_ID in declared_blocks:
                                    fmt_string = """Encountered invalid block ID in line   {line_index_value}. Reason: block ID already declared. Block ID provided was {invalid_block_id} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, invalid_block_id = block_ID)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                # Alright, this is a valid block ID, we can add it to the list and  configure the state of the parser to handle the new block of assembly
                                current_block_ID = block_ID
                                declared_blocks.append(block_ID)
                                program_instructions[block_ID] = dict()
                                block_assembly_number = 0
                        elif prefix == "END":
                            # FORM: END
                            # Ensure there are no additional components to the instruction
                            if len(assembly_line_parameters) != 1:
                                fmt_string = """Invalid END instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 1 arguement. The line was: {invalid_line} ."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("END",())
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "JMP":
                            # FORM: JMP NAME
                            # Unconditional jump to the indicated block
                            # Verify the fixed amount of arguments
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid JMP instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 2 arguements. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                # Verify the block ID format
                                target_jump_block_ID = assembly_line_parameters[1]
                                block_ID_allowed, reason = validate_block_ID(target_jump_block_ID)
                                if block_ID_allowed == False:
                                    fmt_string = """Encountered invalid block ID in line    {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    # Append the block ID to the list of target block IDs if not    already stored
                                    if target_jump_block_ID not in jump_blocks_declared.keys():
                                        lines_that_use_implied_block = [line_index]
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                    else:
                                        lines_that_use_implied_block = jump_blocks_declared[target_jump_block_ID] 
                                        lines_that_use_implied_block.append(line_index)
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                    # Then add the instruction to the block
                                    program_instructions[current_block_ID][str(block_assembly_number)] = ("JMP",(target_jump_block_ID))
                                    block_assembly_number = block_assembly_number + 1
                        elif prefix == "JNE":
                            # FORM: JNE REG_1 REG_2 NAME
                            # Jump to the indicated block if the contents of the two registers are  different
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid JNE instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                target_jump_block_ID = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line  {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                block_ID_allowed, reason = validate_block_ID(target_jump_block_ID)
                                if block_ID_allowed == False:
                                    fmt_string = """Encountered invalid block ID in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    if target_jump_block_ID not in jump_blocks_declared.keys():
                                        lines_that_use_implied_block = [line_index]
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                    else:
                                        lines_that_use_implied_block = jump_blocks_declared[target_jump_block_ID] 
                                        lines_that_use_implied_block.append(line_index)
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("JNE",(reg_1, reg_2, target_jump_block_ID))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "JIE":
                            # FORM: JIE REG_1 REG_2 NAME
                            # Jump to the indicated block if the contents of the two registers are same
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid JIE instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                target_jump_block_ID = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                block_ID_allowed, reason = validate_block_ID(target_jump_block_ID)
                                if block_ID_allowed == False:
                                    fmt_string = """Encountered invalid block ID in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    if target_jump_block_ID not in jump_blocks_declared.keys():
                                        lines_that_use_implied_block = [line_index]
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                    else:
                                        lines_that_use_implied_block = jump_blocks_declared[target_jump_block_ID] 
                                        lines_that_use_implied_block.append(line_index)
                                        jump_blocks_declared[target_jump_block_ID] = lines_that_use_implied_block
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("JIE",(reg_1, reg_2, target_jump_block_ID))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "CMP":
                            # FORM: CMP REG_1 REG_2 REG_3 REG_4 REG_5
                            # Compare REG_1 and REG_2 contents
                            # If the two match, REG_5 will be set to the contents of REG_3, else it will be set to the contents of REG_4
                            if len(assembly_line_parameters) != 6:
                                fmt_string = """Invalid CMP instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 6 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_4 = assembly_line_parameters[4]
                                reg_5 = assembly_line_parameters[5]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_4_allowed, reason = validate_register(reg_4)
                                if reg_4_allowed == False:
                                    fmt_string = """Encountered invalid REG_4 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_5_allowed, reason = validate_register(reg_5)
                                if reg_5_allowed == False:
                                    fmt_string = """Encountered invalid REG_5 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("CMP",(reg_1, reg_2, reg_3, reg_4, reg_5))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "GT":
                            # FORM: GT REG_1 REG_2 REG_3 REG_4 REG_5
                            # Compare REG_1 and REG_2 contents as unsigned integers
                            # If REG_1 is greater than REG_2, REG_5 will be set to the contents of REG_3, else it will be set to the contents of REG_4
                            if len(assembly_line_parameters) != 6:
                                fmt_string = """Invalid GT instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 6 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_4 = assembly_line_parameters[4]
                                reg_5 = assembly_line_parameters[5]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_4_allowed, reason = validate_register(reg_4)
                                if reg_4_allowed == False:
                                    fmt_string = """Encountered invalid REG_4 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_5_allowed, reason = validate_register(reg_5)
                                if reg_5_allowed == False:
                                    fmt_string = """Encountered invalid REG_5 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("GT",(reg_1, reg_2, reg_3, reg_4, reg_5))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "LT":
                            # FORM: LT REG_1 REG_2 REG_3 REG_4 REG_5
                            # Compare REG_1 and REG_2 contents as unsigned integers
                            # If REG_1 is less than REG_2, REG_5 will be set to the contents of REG_3, else it will be set to the contents of REG_4
                            if len(assembly_line_parameters) != 6:
                                fmt_string = """Invalid LT instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 6 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_4 = assembly_line_parameters[4]
                                reg_5 = assembly_line_parameters[5]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_4_allowed, reason = validate_register(reg_4)
                                if reg_4_allowed == False:
                                    fmt_string = """Encountered invalid REG_4 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_5_allowed, reason = validate_register(reg_5)
                                if reg_5_allowed == False:
                                    fmt_string = """Encountered invalid REG_5 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("LT",(reg_1, reg_2, reg_3, reg_4, reg_5))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "ADD":
                            # FORM: ADD REG_1 REG_2 REG_3
                            # Perform an unsigned addition of REG_1 and REG_2
                            # The results of the addition will be written to REG_3
                            # Any overflow(or no overflow) will be written to the CARRY register
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid ADD instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass                         
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("ADD",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "MUL":
                            # FORM: MUL REG_1 REG_2 REG_3
                            # Perform an unsigned multiplication of REG_1 and REG_2
                            # The results of the multiplication will be written to REG_3
                            # Any overflow will be discarded
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid MUL instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass                             
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("MUL",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "SHUP":
                            # FORM: SHUP REG_1 REG_2 REG_3
                            # Perform a shift of REG_2 bits on REG_1 towards the most significant bit
                            # The results of the shift will be written to REG_3
                            # Any overflow will be discarded
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid SHUP instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass                
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("SHUP",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "SHDO":
                            # FORM: SHDO REG_1 REG_2 REG_3
                            # Perform a shift of REG_2 bits on REG_1 towards the least significant bit
                            # The results of the shift will be written to REG_3
                            # Any underflow will be discarded
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid SHDO instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass                              
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("SHDO",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "NOT":
                            # FORM: NOT REG_1 REG_2
                            # Perform a bitwise NOT (negation) of REG_1
                            # The result will be written to REG_2
                            if len(assembly_line_parameters) != 3:
                                fmt_string = """Invalid MUL instruction with an incorrect amount ({argument_amount}) of arguments on line {line_index_value}. There should be 3 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(argument_amount = len(assembly_line_parameters), line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass                             
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("NOT",(reg_1, reg_2))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "AND":
                            # FORM: AND REG_1 REG_2 REG_3
                            # Perform a bitwise AND of REG_1 and REG_2
                            # The result will be written to REG_3
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid AND instruction with an incorrect amount of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("AND",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "OR":
                            # FORM: OR REG_1 REG_2 REG_3
                            # Perform a bitwise OR of REG_1 and REG_2
                            # The result will be written to REG_3
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid OR instruction with an incorrect amount of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("OR",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "XOR":
                            # FORM: XOR REG_1 REG_2 REG_3
                            # Perform a bitwise XOR of REG_1 and REG_2
                            # The result will be written to REG_3
                            if len(assembly_line_parameters) != 4:
                                fmt_string = """Invalid XOR instruction with an incorrect amount of arguments on line {line_index_value}. There should be 4 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_3 = assembly_line_parameters[3]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_3_allowed, reason = validate_register(reg_3)
                                if reg_3_allowed == False:
                                    fmt_string = """Encountered invalid REG_3 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("XOR",(reg_1, reg_2, reg_3))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "LOAD":
                            # FORM: LOAD REG_1
                            # Takes the current memory address in the special register MEMAD and loads the contents of the memory at said address into REG_1
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid LOAD instruction with an incorrect amount of arguments on line {line_index_value}. There should be 2 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("LOAD",(reg_1))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "STORE":
                            # FORM: STORE REG_1
                            # Stores the contents of REG_1 into the memory address in the special register MEMAD
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid STORE instruction with an incorrect amount of arguments on line {line_index_value}. There should be 2 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("STORE",(reg_1))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "SET":
                            # FORM: SET REG_1 DATA
                            # Sets REG_1 to the specified data
                            if len(assembly_line_parameters) != 3:
                                fmt_string = """Invalid MUL instruction with an incorrect amount of arguments on line {line_index_value}. There should be 3 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                data = assembly_line_parameters[2]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                data_allowed, reason = validate_data(data)
                                if data_allowed == False:
                                    fmt_string = """Encountered invalid DATA in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                data = parse_data(data)
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("SET",(reg_1, data))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "COPY":
                            # FORM: COPY REG_1 REG_2
                            # Copies the contents from REG_1 to REG_2
                            if len(assembly_line_parameters) != 3:
                                fmt_string = """Invalid MUL instruction with an incorrect amount of arguments on line {line_index_value}. There should be 3 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_2 = assembly_line_parameters[2]
                                reg_1_allowed, reason = validate_register(reg_1)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                reg_2_allowed, reason = validate_register(reg_2)
                                if reg_2_allowed == False:
                                    fmt_string = """Encountered invalid REG_2 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("COPY",(reg_1, reg_2))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "SETMEMAD":
                            # FORM: SETMEMAD DATA
                            # Sets the special register MEMAD to data
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid SETMEMAD instruction with an incorrect amount of arguments on line {line_index_value}. There should be 2 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                data = assembly_line_parameters[1]
                                data_allowed, reason = validate_data(data)
                                if data_allowed == False:
                                    fmt_string = """Encountered invalid DATA in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                data = parse_data(data)
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("SETMEMAD",(data))
                                block_assembly_number = block_assembly_number + 1
                        elif prefix == "ADDMEMAD":
                            # FORM: ADDMEMAD REG_1
                            # Adds the contents of REG_1 to the special register MEMAD
                            # NOTE: You can use the MEMAD register in this instruction unlike other instructions
                            # This allows you to double the currently stored memory address
                            if len(assembly_line_parameters) != 2:
                                fmt_string = """Invalid ADDMEMAD instruction with an incorrect amount of arguments on line {line_index_value}. There should be 2 arguments. The line was: {invalid_line}."""
                                error_string = fmt_string.format(line_index_value = line_index, invalid_line = assembly_line)
                                raise ValueError(error_string)
                            else:
                                reg_1 = assembly_line_parameters[1]
                                reg_1_allowed, reason = validate_register(reg_1, no_MEMAD = False)
                                if reg_1_allowed == False:
                                    fmt_string = """Encountered invalid REG_1 in line {line_index_value}. Reason: {reason}. Line was: {invalid_line} ."""
                                    error_string = fmt_string.format(line_index_value = line_index, reason = reason, invalid_line = assembly_line)
                                    raise ValueError(error_string)
                                else:
                                    pass
                                program_instructions[current_block_ID][str(block_assembly_number)] = ("ADDMEMAD",(reg_1))
                                block_assembly_number = block_assembly_number + 1
                        else:
                            # Woops, we have an accepted assembly instruction that we have no idea how to parse
                            # This should never happen but if it does, this case will catch it and allow correction of the problem(likely incomplete code).
                            fmt_string = """Valid but unknown assembly prefix encountered on assembly line {line_index_value}. The unknown assembly prefix was: "{unknown_prefix}"."""
                            error_string = fmt_string.format(line_index_value = line_index, unknown_prefix = prefix)
        # First a quick check that we do have a START block ID
        if "START" not in declared_blocks:
            raise ValueError("""Missing "START" block ID, the program will not run""")
        # Second we check to see if the reserved placeholder block ID is used. If it is used, assembly in that must be deleted
        if "NO_BLOCK_ID" in program_instructions.keys():
            del program_instructions["NO_BLOCK_ID"]
        # Now we check that each block ID needed for the jumps are valid
        implied_jump_block_ID_targets = jump_blocks_declared.keys()
        for key in implied_jump_block_ID_targets:
            if key not in declared_blocks:
                fmt_string = """Encountered implied jump target block IDs that are undefined at lines: {invalid_lines} ."""
                invalid_lines_string = ""
                invalid_lines = jump_blocks_declared[key] 
                # Nicely format all the line numbers up to the last one with a comma
                for line_number in range(len(invalid_lines) - 1):
                    invalid_lines_string = invalid_lines_string + str(line_number) + ", "
                # Append the last line number
                invalid_lines_string = invalid_lines_string + str(invalid_lines[len(invalid_lines)-1])
                error_string = fmt_string.format(invalid_lines = invalid_lines_string)
                raise ValueError(error_string)
        # We managed to get through all the checks and stuff
        # YAY
        self.block_ids = declared_blocks
        self.program_instructions = program_instructions
    def get_instruction(self, block_id, instruction_number, loop_on_block = False):
        """
        Returns the instruction found in the provided block and instruction number
        Instruction number starts at 0 and should be an int
        If the block does not have an instruction at the number provided, it will either loop back around(ie modulo) the block if loop_on_block is True or error out if loop_on_block is False
        Instructions are of the format ("INST", (input1, input2))
        First part is the instruction and the second is a tuple of inputs for the instruction
        """
        if block_id in self.block_ids:
            block = self.program_instructions[block_id]
            instructions_count = len(block)
            if instruction_number >= instructions_count:

                if loop_on_block == True:
                    instruction_number = instruction_number % instructions_count
                else:
                    raise ValueError("The provided instruction number does not exist and looping is not enabled")
            instruction = block[str(instruction_number)]
            return(instruction)
        else:
            raise ValueError("The block ID does not exists")
        
        

def validate_block_ID(block_ID):
    """
    Verifies that the given block ID is not colliding with register or data naming
    It also ensures that the block ID does not collide with the reserved ID "NO_BLOCK_ID"
    Returns: (Bool, "reason"/None)
    """
    # Check to avoid collision with registers
    if block_ID[0:2] == register_prefix_global:
        return(False, "arbitary register collision")
    else:
        pass
    if block_ID in special_named_registers_global:
        return(False, "special register collision")
    else:
        pass
    # Check to avoid collision with data prefixes
    if block_ID[0:2] in data_prefixes_global:
        return(False, "data collision")
    else:
        pass
    if block_ID == "NO_BLOCK_ID":
        return(False, "used reserved placeholder block ID")
    elif block_ID == "END":
        return(False, "used reserved end of execution block ID")
    return(True, None)


def validate_register(register_ID, no_MEMAD = True):
    """
    Verfies that the given register ID is a valid register ID
    no_MEMAD is a flag that disallows the use of MEMAD even though it is an existing register
    This flag is by default set to True and must be overrident to enable the use of MEMAD
    Returns: (Bool, "reason"/None)
    """
    if register_ID[0:2] == register_prefix_global:
        return(True, None)
    elif register_ID in special_named_registers_global:
        if no_MEMAD == True:
            if register_ID == "MEMAD":
                return(False, "MEMAD is not allowed")
            else:
                return(True, None)
    else:
        return(False, "not found in special registers or named appropiately")
    

def validate_data(data_input):
    """
    Verifies that the given data is in valid form
    Note: "0b", "0d", and "0x" are all valid and represent 0
    Returns: (Bool, "reason"/None)
    """
    # Get the first two characters as a prefix
    prefix = data_input[0:2]
    # Verify we at least have 2 characters in the prefix
    if len(prefix) != 2:
        return(False, "prefix missing")
    else:
        pass
    # Verify that the prefix is valid
    if prefix not in data_prefixes_global:
        return(False, "invalid prefix")
    # Now we validate the rest of the data according to the prefix
    remainder = data_input[2:len(data_input)]
    if prefix == "0b":
        # This is a binary representation
        for char in remainder:
            if char not in ["0", "1"]:
                return(False, "nonbinary character detected")
            else:
                pass
    elif prefix == "0d":
        for char in remainder:
            if char not in list("0123456789"):
                return(False, "nondecimal character detected")
            else:
                pass
    elif prefix == "0x":
        for char in remainder:
            # Note, we tolerate both capital and lower case A-F for hexadecimal
            if char not in list("0123456789abcdefABCDEF"):
                return(False, "nonhexadecimal character detected")
            else:
                pass
    else:
        raise NotImplementedError("Missing handler for the prefix: "+str(prefix))
    return(True, None)


def parse_data(data_input):
    """
    Takes a data string and returns the appropiate integer
    """
    prefix = data_input[0:2]
    integers = data_input[2:len(data_input)]
    # Add a padding zero to the front of the number because we may have an empty string like "0b" which will return a string of "" otherwise
    integers = "0" + integers
    if prefix == "0b":
        data = int(integers, 2)
    elif prefix == "0d":
        data = int(integers)
    elif prefix == "0x":
        data = int(integers, 16)
    else:
        raise NotImplemented("Missing handler for data prefix: "+str(prefix))
    return(data)
    