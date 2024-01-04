from VMTranslator import add_annotation

def open_vm(source="08\ProgramFlow\FibonacciSeries\FibonacciSeries.vm"):
    with open(source, "r") as fo:
        ins = []
        for line in fo.readlines():
            ins_line = []
            for word in line.split():
                if word[:2] == "//":
                    break
                ins_line.append(word)
            if ins_line:
                ins.append(ins_line)
    return ins

if __name__ == "__main__":
    vm = open_vm()
    asm = []
    for ins in vm:
        ins.insert(0,'//')
        temp = ins
        asm.extend(temp)
    print(asm)