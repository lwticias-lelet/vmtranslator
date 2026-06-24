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