import sys
from collections import defaultdict as defdict

def run(code, inputs, debug = False, super_debug = False):

    inputs = list(map(lambda x:str(bin(ord(x))[2:]).zfill(8), inputs))
    print("")

    prog_index = 0
    tape_index = 0
    inpt_index = 0
    inpt_bit = 0

    loops = []

    tape = defdict(int)
    tape[0] = 0

    while prog_index < len(code):
        command = code[prog_index]

        if command == "<":  # Move left
            tape_index -= 1 if tape_index > 0 else 0

        elif command == ">":  # Move right
            tape_index += 1
            tape[tape_index] = tape[tape_index]  # initialize new cells to 0

        elif command == "^":  # Flip bit
            tape[tape_index] ^= 1

        elif command == "[":  # Start loop
            if tape[tape_index]:
                loops.append(prog_index)
            else:
                depth = 0
                while True:  # scan to matching bracket
                    if code[prog_index] == "[":
                        depth += 1
                    elif code[prog_index] == "]":
                        depth -= 1
                    prog_index += 1
                    if not depth:
                        break

        elif command == "]":  # End loop
            if tape[tape_index]:
                prog_index = loops[-1]  # jump to matching bracket
            else:
                loops.pop()

        elif command == ".":  # Print
            print(end=chr(int("".join(map(str, list(tape.values())[:tape_index+1])), 2)))

        elif command == ",":  # Bitwise input
            try:
                tape[tape_index] = int(inputs[inpt_index][inpt_bit])
                inpt_bit += 1
                tape_index += 1

            except IndexError:  # if no bits left in the char:
                try:
                    tape[tape_index] = int(inputs[inpt_index+1][0])
                    inpt_index += 1
                    inpt_bit = 1
                    tape_index += 1

                except IndexError:  # if no chars left in the input:
                    tape[tape_index] = 0

        elif command == "?":  # Charwise input
            try:
                if inpt_bit < len(inputs[inpt_index]):  # if bits left in the char:
                    for i in range(len(inputs[inpt_index][inpt_bit:])):
                        tape[tape_index+i] = int(inputs[inpt_index][inpt_bit])
                        inpt_bit += 1

                else:  # if no bits left in the char:
                    inpt_index += 1
                    inpt_bit = 0
                    for i in range(len(inputs[inpt_index])):
                        tape[tape_index+i] = int(inputs[inpt_index][inpt_bit])
                        inpt_bit += 1
                inpt_index += 1
                inpt_bit = 0

            except IndexError:  # if no chars left in the input
                for i in range(8):
                    tape[tape_index+i] = 0

        prog_index += 1

    try:
        if ("".join(map(str, tape.values())).rindex("1") + 1) > tape_index:
            index = "".join(map(str, tape.values())).rindex("1")
        else:
            index = tape_index
    except:
        index = tape_index
    if debug:
        print("\n" * ("." in code), list(tape.values())[:index+1], sep="")


if __name__ == "__main__":
    sys.stdout.write("> ")
    sys.stdout.flush()
    run(sys.argv[1], sys.stdin.read(), "-d" in sys.argv[2:], "--debug" in sys.argv[2:])
    print("")
