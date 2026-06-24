import os


class CodeWriter:

    def __init__(self, filename, bootstrap=False):

        self.file = open(filename, "w")

        self.label_counter = 0
        self.return_counter = 0

        self.class_name = os.path.basename(filename).replace(".asm", "")
        self.current_function = ""

        if bootstrap:
            self.write_bootstrap()

    def close(self):

        self.file.close()

    def write_line(self, text):

        self.file.write(text + "\n")

    def set_filename(self, filename):

        self.class_name = filename

    def push_d(self):

        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

    def write_bootstrap(self):

        self.write_line("@256")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("M=D")

        self.write_call("Sys.init", 0)
            def write_arithmetic(self, command):

        if command == "add":
            self.binary("M=M+D")

        elif command == "sub":
            self.binary("M=M-D")

        elif command == "and":
            self.binary("M=M&D")

        elif command == "or":
            self.binary("M=M|D")

        elif command == "neg":
            self.unary("M=-M")

        elif command == "not":
            self.unary("M=!M")

        elif command == "eq":
            self.compare("JEQ")

        elif command == "gt":
            self.compare("JGT")

        elif command == "lt":
            self.compare("JLT")

    def unary(self, operation):

        self.write_line("@SP")
        self.write_line("A=M-1")
        self.write_line(operation)

    def binary(self, operation):

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("A=A-1")
        self.write_line(operation)

    def compare(self, jump):

        true_label = f"TRUE_{self.label_counter}"
        end_label = f"END_{self.label_counter}"

        self.label_counter += 1

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("A=A-1")
        self.write_line("D=M-D")
        self.write_line(f"@{true_label}")
        self.write_line(f"D;{jump}")

        self.write_line("@SP")
        self.write_line("A=M-1")
        self.write_line("M=0")

        self.write_line(f"@{end_label}")
        self.write_line("0;JMP")

        self.write_line(f"({true_label})")
        self.write_line("@SP")
        self.write_line("A=M-1")
        self.write_line("M=-1")

        self.write_line(f"({end_label})")
            def write_push(self, segment, index):

        if segment == "constant":

            self.write_line(f"@{index}")
            self.write_line("D=A")

        elif segment in ["local", "argument", "this", "that"]:

            base = {
                "local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"
            }[segment]

            self.write_line(f"@{base}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("A=D+A")
            self.write_line("D=M")

        elif segment == "temp":

            self.write_line(f"@{5 + index}")
            self.write_line("D=M")

        elif segment == "pointer":

            if index == 0:
                self.write_line("@THIS")
            else:
                self.write_line("@THAT")

            self.write_line("D=M")

        elif segment == "static":

            self.write_line(f"@{self.class_name}.{index}")
            self.write_line("D=M")

        self.push_d()

    def write_pop(self, segment, index):

        if segment in ["local", "argument", "this", "that"]:

            base = {
                "local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"
            }[segment]

            self.write_line(f"@{base}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("D=D+A")

        elif segment == "temp":

            self.write_line(f"@{5 + index}")
            self.write_line("D=A")

        elif segment == "pointer":

            if index == 0:
                self.write_line("@THIS")
            else:
                self.write_line("@THAT")

            self.write_line("D=A")

        elif segment == "static":

            self.write_line(f"@{self.class_name}.{index}")
            self.write_line("D=A")

        self.write_line("@R13")
        self.write_line("M=D")

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")

        self.write_line("@R13")
        self.write_line("A=M")
        self.write_line("M=D")
            def make_label(self, label):

        if self.current_function:
            return f"{self.current_function}${label}"

        return label

    def write_label(self, label):

        self.write_line(f"({self.make_label(label)})")

    def write_goto(self, label):

        self.write_line(f"@{self.make_label(label)}")
        self.write_line("0;JMP")

    def write_if(self, label):

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")

        self.write_line(f"@{self.make_label(label)}")
        self.write_line("D;JNE")
            def write_function(self, function_name, nlocals):

        self.current_function = function_name

        self.write_line(f"({function_name})")

        for i in range(nlocals):

            self.write_line("@0")
            self.write_line("D=A")
            self.push_d()

    def write_call(self, function_name, nargs):

        return_label = f"{function_name}$ret.{self.return_counter}"
        self.return_counter += 1

        self.write_line(f"@{return_label}")
        self.write_line("D=A")
        self.push_d()

        for segment in ["LCL", "ARG", "THIS", "THAT"]:

            self.write_line(f"@{segment}")
            self.write_line("D=M")
            self.push_d()

        self.write_line("@SP")
        self.write_line("D=M")
        self.write_line(f"@{5 + nargs}")
        self.write_line("D=D-A")
        self.write_line("@ARG")
        self.write_line("M=D")

        self.write_line("@SP")
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")

        self.write_line(f"@{function_name}")
        self.write_line("0;JMP")

        self.write_line(f"({return_label})")

    def write_return(self):

        self.write_line("@LCL")
        self.write_line("D=M")
        self.write_line("@R13")
        self.write_line("M=D")

        self.write_line("@5")
        self.write_line("A=D-A")
        self.write_line("D=M")
        self.write_line("@R14")
        self.write_line("M=D")

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("A=M")
        self.write_line("M=D")

        self.write_line("@ARG")
        self.write_line("D=M+1")
        self.write_line("@SP")
        self.write_line("M=D")

        self.write_line("@R13")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@THAT")
        self.write_line("M=D")

        self.write_line("@R13")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@THIS")
        self.write_line("M=D")

        self.write_line("@R13")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("M=D")

        self.write_line("@R13")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")

        self.write_line("@R14")
        self.write_line("A=M")
        self.write_line("0;JMP")