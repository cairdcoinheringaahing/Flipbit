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

def nth_index(string, substring, N, reverse):
	if string.count(substring) < N:
		return -1
	string = string[::reverse]
	found = 0
	for i in range(len(string)):
		char = string[i]
		if substring == char:
			found += 1
		if found == N:
			if reverse < 0:
				return len(string) - i
			else:
				return i
	return -1

def run(code, inputs, debug):
	stream = list(to_binary(*inputs))
	pindex = 0
	iindex = 0
	tindex = 0
	loop_depth = 0
	tape = [0] * 3000
	while pindex < len(code):
		char = code[pindex]
		if char == '^':
			tape[tindex] ^= 1
		if char == '>':
			tindex += 1
		if char == '<':
			tindex -= 1
			tindex %= 3000
		if char == ',':
			if iindex < len(stream):
				tape[tindex] = stream[iindex]
				iindex += 1
			else:
				tape[tindex] = 0
		if char == '.':
			num = tape[:tindex+1]
			print(end=from_binary(num))
		if char == '[':
			loop_depth += 1
			if tape[tindex]:
				pindex = nth_index(code, ']', loop_depth, -1)
		if char == ']':
			if not tape[tindex]:
				pindex = nth_index(code, '[', loop_depth, 1)
			else:
				loop_depth -= 1
		pindex += 1

	index = ''.join(map(str, tape)).rindex('1') if (''.join(map(str, tape)).rindex('1') + 1) > tindex else tindex
	if debug:
		print('\n', tape[:index+1], sep='')

if __name__ == '__main__':
	run(sys.argv[1], sys.stdin.read(), '-d' in sys.argv[2:])
