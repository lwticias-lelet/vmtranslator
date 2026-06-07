import sys

from parser.parser import Parser
from codewriter.codewriter import CodeWriter


def main():

    if len(sys.argv) != 2:

        print("Uso: python main.py arquivo.vm")
        return

    input_file = sys.argv[1]

    output_file = input_file.replace(".vm", ".asm")

    parser = Parser(input_file)
    writer = CodeWriter(output_file)

    while parser.has_more_commands():

        parser.advance()

        cmd_type = parser.command_type()

        if cmd_type == "C_ARITHMETIC":
            writer.write_arithmetic(parser.arg1())

        elif cmd_type == "C_PUSH":
            writer.write_push(
                parser.arg1(),
                parser.arg2()
            )

        elif cmd_type == "C_POP":
            writer.write_pop(
                parser.arg1(),
                parser.arg2()
            )

    writer.close()

    print(f"Arquivo gerado: {output_file}")


if __name__ == "__main__":
    main()