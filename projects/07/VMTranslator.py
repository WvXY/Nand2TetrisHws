import argparse


def source():
    """ GUI: python VMtranslator.py SOURCE """
    parser = argparse.ArgumentParser(description="SOURCE")
    parser.add_argument("source", type=str, help="Source File")
    args = parser.parse_args()
    return args.source


def open_vm(source=source()):
    with open(source, "r") as fo:
        # use line.strip() to filter empty line (return false when empty)
        # remove all empty lines, \n and notes
        file = [
            line.strip("\n")
            for line in fo.readlines()
            if line.strip() and line[:2] != "//"
        ]
    return file


def save_asm(asm_ins: list, address=source()):
    target = address.replace(".vm", ".asm")
    with open(target, "w") as fw:
        fw.write("\n".join(asm_ins))  # auto newline


def branching(ins, asm_ins, count):
    ins = ins.split()
    length = len(ins)
    if length == 1:
        return len_1(ins[0], asm_ins, count)
    elif length == 2:
        return len_2(ins)
    else:
        return len_3(ins)


def len_1(action, vm_ins, count):  # arithmetic/boolean
    actions = {
        "add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M+D"],
        "sub": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"],
        "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
        "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
        "not": ["@SP", "A=M-1", "M=!M"],
        "neg": ["@SP", "A=M-1", "M=-M"],
    }
    jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
    if action in actions.keys():
        return actions[action]
    else:
        asm_ins = ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1"]
        location = str(len(vm_ins) + 10 - count)
        asm_ins.extend(
            ["@" + location, "D;" + jump[action], "@SP", "A=M-1", "M=0"]
        )
        return asm_ins


def len_2(ins):  # lables
    pass


def len_3(ins):  # pop/push
    if ins[0] == "pop":
        return pop(ins)
    else:
        return push(ins)


mapping = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "static": "16",
    "temp": "5",
    "pointer": "3",
}


def pop(ins):
    asm_ins = ["@" + ins[2], "D=A", "@" + mapping[ins[1]]]
    if ins[1] == "pointer" or ins[1] == "temp":
        asm_ins.extend(["D=D+A"])
    else:
        asm_ins.extend(["D=D+M"])
    pop_code = ["@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
    asm_ins.extend(pop_code)
    return asm_ins


def push(ins):
    asm_ins = ["@" + ins[2], "D=A"]
    if ins[1] == "constant":
        pass
    elif ins[1] == "pointer" or ins[1] == "temp":
        asm_ins.extend(["@" + mapping[ins[1]], "A=A+D", "D=M"])
    else:
        asm_ins.extend(["@" + mapping[ins[1]], "A=M+D", "D=M"])
    asm_ins.extend(["@SP", "A=M", "M=D", "@SP", "M=M+1"])
    return asm_ins


def add_annotation(line: str):
    return ["//" + line]


if __name__ == "__main__":
    vm_ins = open_vm()
    count = 0
    asm_ins = []
    for line in vm_ins:
        asm_ins.extend(add_annotation(line))
        asm_ins.extend(branching(line, asm_ins, count))
        count += 1
    print('Translation Succeed!\n')
    save_asm(asm_ins)
