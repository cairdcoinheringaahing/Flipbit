import sys

def to_binary(*args):
	final = []
	for arg in args:
		for element in list(map(int, bin(ord(arg))[2:])):
			final.append(element)
	return final

def from_binary(array):
	total = 0
	for i in range(len(array)):
		mul = 2 ** (len(array) - i - 1)
		total += mul * array[i]
	return chr(total)

def nth_index(string, substring, N):
	if string.count(substring) < N:
		return -1
	found = 0
	for i in range(len(string)):
		char = string[i]
		if substring == char:
			found += 1
		if found == N:
			return i
	return -1

def run(code, inputs, debug, super_debug):
	stream = list(to_binary(*inputs))
	pindex = 0
	iindex = 0
	tindex = 0
	loop_depth = 0
	tape = [0] * 3000
	store = -1
	while pindex < len(code):
		char = code[pindex]
		if char == '^':
			tape[tindex] ^= 1
		if char == '>':
			tindex += 1
		if char == '<':
			tindex -= 1
			if tindex < 0:
				tindex = 0
				tape[tindex] = 0
		if char == ',':
			if iindex < len(stream):
				tape[tindex] = stream[iindex]
				iindex += 1
				tindex += 1
			else:
				tape[tindex] = 0
		if char == '?':
			iindex += 8
			tape[tindex:tindex+8] = stream[iindex-8:iindex]
		if char == '.':
			num = tape[:tindex+1]
			print(end=from_binary(num)+'\n'*super_debug)
		if char == '[':
			loop_depth += 1
			store = pindex
			if not tape[tindex]:
				pindex = nth_index(code, ']', loop_depth)
		if char == ']':
			if tape[tindex]:
				pindex = nth_index(code[store:], '[', loop_depth) + store
			else:
				loop_depth -= 1
		if char == '#' and debug:
			index = ''.join(map(str, tape)).rindex('1') if (''.join(map(str, tape)).rindex('1') + 1) > tindex else tindex
			if debug:
				print('\n', tape[:index+1], sep='')
		pindex += 1
		if super_debug:
			print(('%s %s %-{}s %-2s %s').format(len(str(len(code)))) % (char, loop_depth, pindex, tindex, tape[:tindex+1]))

	index = ''.join(map(str, tape)).rindex('1') if (''.join(map(str, tape)).rindex('1') + 1) > tindex else tindex
	if debug:
		print('\n' * ('.' in code), tape[:index+1], sep='')

if __name__ == '__main__':
	run(sys.argv[1], sys.stdin.read(), '-d' in sys.argv[2:], '--debug' in sys.argv[2:])
