def mapping1(s: str):  # locate mapping locations
    map = {'local': 'LCL', 'arguement': 'ARG', 'this': 'THIS', 'that': 'THAT',
            'static': 16, 'temp': 5, 'pointer': 3}
    if s == 'constant':
        pass
    else:
        return '@'+map[s]+'\nD=M+D\n@5'+'\nM=D\n'

def mapping2():
    return '@5\nA=M\nM=D\n'

def push(str):
    code='@'+str[2]+'\nD=A\n'
    if str[1] != 'constant':
        code += mapping1(str[1]) + changeSP('+') + mapping2()
    else:
        code += changeSP('+') 
    return code

def add_note(line):
    return '//' + line


def changeSP(sign):
    return '@SP\nA=M\nD=M\n@SP\nM=M'+sign+'1\n'





address = '07\StackArithmetic\SimpleAdd\SimpleAdd.vm'
with open(address) as f:
    # use line.strip() to filter empty line (return false when empty)
    # remove all empty lines, \n and notes
    file = [line.strip('\n') for line in f.readlines()
            if line.strip() and line[:2] != '//']

instructions = ''
for line in file:
    instructions += '// ' + line +'\n' # automatically add notes
    print(instructions)
    line = line.split()
    instructions += changeSP('+')
