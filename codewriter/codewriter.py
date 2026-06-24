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

        # inicia a pilha em 256

        self.write_line("@256")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("M=D")

        # chama Sys.init

        self.write_call("Sys.init", 0)

    def write_call(self, function_name, nargs):
        pass