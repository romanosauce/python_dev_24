import cmd
import cowsay
import shlex
import readline


class CowsayCmd(cmd.Cmd):
    prompt = "cowsay>> "
    intro = """
Welcome to the cowsay CLI. It is fun, I promise
"""

    def do_list_cows(self, arg):
        print(cowsay.list_cows())

    def make_bubble(self, arg):
        print(cowsay.make_bubble(arg))

    def cowsay(self, arg):
        print(cowsay.cowsay(arg))

    def cowthink(self, arg):
        print(cowsay.cowthink(arg))


if __name__ == '__main__':
    CowsayCmd().cmdloop()
