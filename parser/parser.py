class Parser:

    def __init__(self, filename):

        self.commands = []

        with open(filename, "r") as file:

            for line in file:

                line = line.split("//")[0].strip()

                if line:
                    self.commands.append(line)

        self.index = 0
        self.current_command = None

    def has_more_commands(self):
        return self.index < len(self.commands)

    def advance(self):

        self.current_command = self.commands[self.index]
        self.index += 1
            def command_type(self):

        cmd = self.current_command.split()[0]

        if cmd == "push":
            return "C_PUSH"

        if cmd == "pop":
            return "C_POP"

        if cmd == "label":
            return "C_LABEL"

        if cmd == "goto":
            return "C_GOTO"

        if cmd == "if-goto":
            return "C_IF"

        if cmd == "function":
            return "C_FUNCTION"

        if cmd == "call":
            return "C_CALL"

        if cmd == "return":
            return "C_RETURN"

        return "C_ARITHMETIC"