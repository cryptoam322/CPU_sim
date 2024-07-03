import CPU_core
import CPU_ASM_parser

hardcode_file_path = False
hardcode_iterations = False
fallback_iterations = 100
fallback_bit_width = 8

def main():
    exit_enable = False
    while exit_enable == False:
        print("----------------------------------------")
        exit_req = input("Exit? ")
        if exit_req.upper() in ["Y","YES","E","EXIT"]:
            exit_enable = True
        else:
            if hardcode_file_path == True:
                print("Using hard coded file path")
                file_path = r"""INSERT_HARD_CODED_FILE_PATH"""
                print("File path is: "+file_path)
            else:
                file_path = input("File path to ASM? ")
            file_path_success = False
            try:
                with open(file_path, "r") as asm_file:
                    file_string = asm_file.read()
                    split_asm_lines = file_string.splitlines()
                    file_path_success = True
            except Exception as e:
                print("!!!Failed to get file contents!!!")
                print("Error below")
                print(str(type(e)))
                print(e)
                throw_error = input("Intentionally throw error for debugging? ")
                throw_error = throw_error.upper()
                if throw_error in ["Y", "YES"]:
                    raise Exception("Intentionally threw error for debugging")
                else: 
                    pass
            if file_path_success == True:
                ASM_parse_sucess = False
                try:
                    asm_out = CPU_ASM_parser.program(split_asm_lines)
                    ASM_parse_sucess = True
                except Exception as e:
                    print("!!!Failed parsing!!!")
                    print("Error below")
                    print(type(e))
                    print(e)
                    throw_error = input("Intentionally throw error for debugging? ")
                    throw_error = throw_error.upper()
                    if throw_error in ["Y", "YES"]:
                        raise Exception("Intentionally threw error for debugging")
                    else:
                        pass
                if ASM_parse_sucess == True:
                    instructions = asm_out.program_instructions
                    blocks = asm_out.block_ids
                    print("-----")
                    print("Instructions")
                    print(str(instructions))
                    input()
                    print("-----")
                    print("Block IDs")
                    print(str(blocks))
                    input()
                    print("-----")
                    for key in instructions:
                        print(key)
                        print(str(instructions[key]))
                        print()
                    print("Assembly sucessfully parsed")
                    input()
                    print("-----")
                    try:
                        iterations = int(input("How many iterations? "))
                        if iterations < 1:
                            print("Invalid iterations(<1 or not an integer), using fallback iterations count of "+str(fallback_iterations))
                            iterations = fallback_iterations
                        else:
                            pass
                    except Exception:
                        iterations = fallback_iterations
                        print("Invalid iterations count, falling back to "+str(fallback_iterations))
                    input()
                    try:
                        bit_width = int(input("Bit width of CPU? "))
                        if bit_width < 1:
                            print("Invalid bit width(<1 or not an integer), using fallback bit width of "+str(fallback_bit_width))
                            bit_width = fallback_bit_width
                        else:
                            pass
                    except Exception:
                        bit_width = fallback_bit_width
                        print("Invalid iterations count, falling back to "+str(fallback_iterations))
                    CPU_obj = CPU_core.CPU(bit_width, False)
                    CPU_obj.load_program(asm_out)
                    execution_success = False
                    try:
                        print("Executing now...")
                        CPU_obj.step_multiple_instruction(iterations)
                        log = CPU_obj.get_execution_log()
                        memory = CPU_obj.get_memory()
                        registers = CPU_obj.get_registers()
                        execution_success = True
                    except Exception as e:
                        print("!!!Failed execution!!!")
                        print("Error below")
                        print(str(type(e)))
                        print(e)
                        throw_error = input("Intentionally throw error for debugging? ")
                        throw_error = throw_error.upper()
                        if throw_error in ["Y", "YES"]:
                            raise Exception("Intentionally threw error for debugging")
                        else:
                            pass
                    if execution_success == True:
                        print("-----")
                        print("Output")
                        print("LOG: "+str(log))
                        input()
                        print("Memory: "+str(memory))
                        input()
                        print("Registers: "+str(registers))
                        input()
                        print("-----")
                        print("Log")
                        for i in range(len(log)):
                            print(str(i)+": "+str(log[i]))
                        input()
                        print("-----")
                        print("Memory")
                        for i in memory.keys():
                            print(str(i)+":"+str(memory[i]))
                        print("-----")
                        input()
                        print("Registers")
                        for i in registers.keys():
                            print(str(i)+":"+str(registers[i]))
                    else:
                        pass
        input()     
    exit()

if __name__ == "__main__":
    main()