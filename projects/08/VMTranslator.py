import argparse, os


#def source():
    #""" GUI: python VTranslator.py SOURCE """
    #parser = argparse.ArgumentParser(description="SOURCE")
    #parser.add_argument("source", type=str, help="Source File")
    #args = parser.parse_args()
    #return args.source

test = 'D:\\OneDrive\Documents\\nand2tetris\projects\\08\ProgramFlow\FibonacciSeries\FibonacciSeries.vm'
def open_vm(source = test): # return splited ins
    with open(source, "r") as fo:
        vm_ins = []
        for line in fo.readlines():
            ins_line = []
            for word in line.split():
                if word[:2] == "//":
                    break
                ins_line.append(word)
            if ins_line:
                vm_ins.append(ins_line)
    return vm_ins


def save_asm(asm_ins: list, address=test):
    target = address.replace(".vm", ".asm")
    with open(target, "w") as fw:
        fw.write("\n".join(asm_ins))  # auto newline


def branching(ins, vm_ins, count):
    length = len(line)
    if length == 1:
        return len_1(ins[0], vm_ins, count)
    elif length == 2:
        return len_2(ins)
    else:
        return len_3(ins)


def len_1(ins, vm_ins, count) -> list:  # arithmetic/boolean
    actions = {
        "add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M+D"],
        "sub": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"],
        "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
        "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
        "not": ["@SP", "A=M-1", "M=!M"],
        "neg": ["@SP", "A=M-1", "M=-M"],
    }
    jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
    if ins in actions.keys():
        return actions[ins]
    else:
        asm_ins = ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1"]
        location = str(len(vm_ins) + 10 - count)
        asm_ins.extend(["@" + location, "D;" + jump[ins], "@SP", "A=M-1", "M=0"])
        return asm_ins


def len_2(ins) -> list:     # branching command
    if ins[0] == 'label':
        return ["(" + ins[1] + ')']
    elif ins[0] == 'if-goto':
        return ['@SP','AM=M-1',"D=M",'@'+ ins[1], 'D;JGE']
    elif ins[0] ==  'goto':
        return ['@'+ins[1],'0;JMP']
    else:
        return False

def len_3(ins) -> list:     # pop/push/function
    if ins[0] == "pop":
        return pop(ins)
    elif ins[0] == 'push':
        return push(ins)
    elif ins[0] == 'function':
        return function_call(ins)
    else:
        return False


mapping = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "static": "16",
    "temp": "5",
    "pointer": "3",
}


def pop(ins) -> list:
    asm_ins = ["@" + ins[2], "D=A", "@" + mapping[ins[1]]]
    if ins[1] == "pointer" or ins[1] == "temp":
        asm_ins.extend(["D=D+A"])
    else:
        asm_ins.extend(["D=D+M"])
    pop_code = ["@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
    asm_ins.extend(pop_code)
    return asm_ins


def push(ins) -> list:
    asm_ins = ["@" + ins[2], "D=A"]
    if ins[1] == "constant":
        pass
    elif ins[1] == "pointer" or ins[1] == "temp":
        asm_ins.extend(["@" + mapping[ins[1]], "A=A+D", "D=M"])
    else:
        asm_ins.extend(["@" + mapping[ins[1]], "A=M+D", "D=M"])
    asm_ins.extend(["@SP", "A=M", "M=D", "@SP", "M=M+1"])
    return asm_ins

def function_call(ins) -> list:
    pass


if __name__ == "__main__":
    vm_ins = open_vm()
    count = 0
    asm_ins = []
    for line in vm_ins:
        print(line)
        asm_ins.extend(['//'+ " ".join(line)])     #add annotations
        asm_ins.extend(branching(line, asm_ins, count))
        count += 1
        print(asm_ins)
    print("Translation Succeed!\n")
    save_asm(asm_ins)
