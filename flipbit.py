import sys
from collections import defaultdict

def run(code, inputs, debug, super_debug):
    print('')
    inputs = list(map(lambda x:str(bin(ord(x))[2:]).zfill(8), inputs))

    pindex = 0
    tindex = 0
    iindex = 0
    ibit = 0

    loop_starts = []

    tape = defaultdict(int)

    while pindex < len(code):
        char = code[pindex]
        if char == '^': # flip the bit
            tape[tindex] ^= 1
        elif char == '>': # move right
            tindex += 1
            tape[tindex] = tape[tindex] # initialize any new tape cells
        elif char == '<': # move left
            tindex -= 1
            if tindex < 0:
                tindex = 0
                tape[tindex] = 0
        elif char == ',': # bitwise input
            try:
                tape[tindex] = int(inputs[iindex][ibit]) # get the next bit of the current input char
                ibit += 1
                tindex += 1
            except IndexError: # if no more bits, go to the next input char
                try:
                    tape[tindex] = int(inputs[iindex+1][0])
                    iindex += 1
                    ibit = 1
                    tindex += 1
                except IndexError: # if no more chars, return 0
                    tape[tindex] = 0
        elif char == '?': # charwise input
            try:
                if ibit < len(inputs[iindex]): # get the remaining bits of the current input char
                    for i in range(len(inputs[iindex][ibit:])):
                        tape[tindex+i] = int(inputs[iindex][ibit])
                        ibit += 1
                    iindex += 1
                    ibit = 0
                else: # if no more bits, get the next input char
                    iindex += 1
                    ibit = 0
                    for i in range(len(inputs[iindex])):
                        tape[tindex+i] = int(inputs[iindex][ibit])
                        ibit += 1
                    iindex += 1
                    ibit = 0
            except IndexError: # if no more chars, return 8 0s
                for i in range(8):
                    tape[tindex+i] = 0
        elif char == '.':
            print(end=chr(int(''.join(map(str, list(tape.values())[:tindex+1])), 2))+'\n'*super_debug)
        elif char == '[':
            loop_starts.append(pindex)
            if not tape[tindex]: # skip to matching bracket if current bit is 0
                depth = 1
                while depth and pindex < len(code):
                    if code[pindex+1] == '[':
                        depth += 1
                    elif code[pindex+1] == ']':
                        depth -= 1
                    pindex += 1
        elif char == ']':
            pindex = loop_starts.pop()-1
        elif char == '#' and debug:
            try:
                if (''.join(map(str, tape.values())).rindex('1') + 1) > tindex:
                    index = ''.join(map(str, tape.values())).rindex('1')
                else: index = tindex
            except:
                index = tindex
            print('\n', tape[:index+1], sep='')
        pindex += 1
        if super_debug:
            print(('%s %s %-{}s %-2s %s').format(len(str(len(code)))) % (char, len(loop_starts), pindex, tindex, list(tape.values())[:tindex+1]))
    try:
        if (''.join(map(str, tape.values())).rindex('1') + 1) > tindex:
            index = ''.join(map(str, tape.values())).rindex('1')
        else:
            index = tindex
    except:
        index = tindex
    if debug:
        print('\n' * ('.' in code), list(tape.values())[:index+1], sep='')

if __name__=='__main__':
    run(sys.argv[1], sys.stdin.read(), '-d' in sys.argv[2:], '--debug' in sys.argv[2:])
