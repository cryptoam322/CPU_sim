from CPU_ASM_parser import program

hardcode_file_path = False

def main():
    exit_enable = False
    while exit_enable == False:
        print("----------------------------------------")
        exit_req = input("Exit? ")
        if exit_req.upper() in ["Y","YES","E","EXIT"]:
            exit_enable = True
        else:
            if hardcode_file_path == True:
                file_path = r"""INSERT_HARD_CODED_FILE_PATH"""
            else:
                file_path = input("File path to ASM?")
            with open(file_path, "r") as asm_file:
                file_string = asm_file.read()
            split_asm_lines = file_string.splitlines()
            success = False
            try:
                asm_out = program(split_asm_lines)
                success = True
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
            if success == True:
                instructions = asm_out.program_instructions
                blocks = asm_out.block_ids
                print("Instructions: "+str(instructions))
                print("-----")
                print("Block IDs: "+str(blocks))
                print("-----")
                for key in instructions:
                    print(key)
                    print(str(instructions[key]))
                    print()
    exit()

if __name__ == "__main__":
    main()