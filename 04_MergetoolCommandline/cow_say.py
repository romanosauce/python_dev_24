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
        """
        List all available cows in given directory (or default)

        :param cow_path=PATH/TO/FILE
        """

        print(cowsay.list_cows())

    def do_make_bubble(self, arg):
        """
        Wrap text in bubble

        :param text=TEXT
        :param width=WIDTH
        """

        print(cowsay.make_bubble(arg))

    def do_cowsay(self, arg):
        """
        Make cow say the text

        :param text=TEXT
        :param cow=COW_NAME
        :param eyes=EYE_STRING
        :param tongue=TONGUE_STRING
        """

        print(cowsay.cowsay(arg))

    def do_cowthink(self, arg):
        """
        Make cow say the text

        :param text=TEXT
        :param cow=COW_NAME
        :param eyes=EYE_STRING
        :param tongue=TONGUE_STRING
        """

        print(cowsay.cowthink(arg))


if __name__ == '__main__':
    CowsayCmd().cmdloop()
