import os
import sys

from parser.parser import Parser
from codewriter.codewriter import CodeWriter


def get_output_file(input_path):

    if os.path.isdir(input_path):

        folder_name = os.path.basename(os.path.normpath(input_path))

        return os.path.join(input_path, folder_name + ".asm")

    return input_path.replace(".vm", ".asm")


def get_vm_files(input_path):

    if os.path.isdir(input_path):

        files = []

        for file in os.listdir(input_path):

            if file.endswith(".vm"):

                files.append(os.path.join(input_path, file))

        return sorted(files)

    return [input_path]


def need_bootstrap(input_path):

    # no project 8, quando tem Sys.vm precisa iniciar com bootstrap

    if os.path.isdir(input_path):

        for file in os.listdir(input_path):

            if file == "Sys.vm":
                return True

    return False


def translate(input_path):

    output_file = get_output_file(input_path)

    vm_files = get_vm_files(input_path)

    bootstrap = need_bootstrap(input_path)

    writer = CodeWriter(output_file, bootstrap)

    for vm_file in vm_files:

        file_name = os.path.basename(vm_file).replace(".vm", "")

        writer.set_filename(file_name)

        parser = Parser(vm_file)

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

            elif cmd_type == "C_LABEL":

                writer.write_label(parser.arg1())

            elif cmd_type == "C_GOTO":

                writer.write_goto(parser.arg1())

            elif cmd_type == "C_IF":

                writer.write_if(parser.arg1())

            elif cmd_type == "C_FUNCTION":

                writer.write_function(
                    parser.arg1(),
                    parser.arg2()
                )

            elif cmd_type == "C_CALL":

                writer.write_call(
                    parser.arg1(),
                    parser.arg2()
                )

            elif cmd_type == "C_RETURN":

                writer.write_return()

    writer.close()

    print("Arquivo gerado:", output_file)


def main():

    if len(sys.argv) != 2:

        print("Uso:")
        print("python main.py arquivo.vm")
        print("python main.py pasta")
        return

    input_path = sys.argv[1]

    translate(input_path)


if __name__ == "__main__":
    main()