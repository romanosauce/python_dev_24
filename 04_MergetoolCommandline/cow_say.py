import cmd
import cowsay
import shlex
import readline
import sys


class CowsayCmd(cmd.Cmd):
    prompt = "cowsay>> "
    intro = """
        Welcome to the cowsay CLI. It is fun, I promise
        """
    eyes_preset = {'OO', 'xx', '$$', '**', '--', '@@', '__', '^^'}
    tongue_preset = {'U ', ' U', '||', '| ', 'J ', 'LT'}

    def get_option_value(self, opt, arg, cmd_name, val_type=str):
        if opt in arg:
            idx = arg.index(opt)
            try:
                val = val_type(arg[idx+1])
            except Exception:
                print("Wrong usage!")
                self.do_help(cmd_name)
                raise
            return val
        else:
            return None

    def do_list_cows(self, arg):
        """
        List all available cows in given directory (or default)

        :param -f PATH/TO/FILE
        """

        arg = shlex.split(arg)
        try:
            val_path = self.get_option_value('-f', arg, 'list_cows')
        except Exception:
            return
        cow_path = val_path if val_path else cowsay.COW_PEN

        print(cowsay.list_cows(cow_path=cow_path))

    def do_make_bubble(self, arg):
        """
        Wrap text in bubble

        :param -t TEXT
        :param -w WIDTH
        """

        arg = shlex.split(arg)
        try:
            val_width = self.get_option_value('-w', arg, 'make_bubble', int)
            val_text = self.get_option_value('-t', arg, 'make_bubble')
        except Exception:
            return
        width = val_width if val_width else 40
        text = val_text if val_text else sys.stdin.read()

        print(cowsay.make_bubble(text=text, width=width))

    def do_cowsay(self, arg, func=cowsay.cowsay):
        """
        Make cow say the text

        :param -t TEXT
        :param -c COW_NAME
        :param -e EYE_STRING
        :param -T TONGUE_STRING
        """

        arg = shlex.split(arg)
        try:
            val_text = self.get_option_value('-t', arg, 'cowsay')
            val_eyes = self.get_option_value('-e', arg, 'cowsay')
            val_tongue = self.get_option_value('-T', arg, 'cowsay')
            val_cow = self.get_option_value('-c', arg, 'cowsay')
        except Exception:
            return
        text = val_text if val_text else sys.stdin.read()
        eyes = val_eyes if val_eyes else cowsay.Option.eyes
        tongue = val_tongue if val_tongue else cowsay.Option.tongue
        cow = val_cow if val_cow else 'default'

        print(func(text, cow=cow, eyes=eyes, tongue=tongue))

    def do_cowthink(self, arg):
        """
        Make cow think the text

        :param -t TEXT
        :param -c COW_NAME
        :param -e EYE_STRING
        :param -T TONGUE_STRING
        """

        self.do_cowsay(arg, func=cowsay.cowthink)

    def complete_list_cows(self, text, line, begidx, endidx):
        return ["""Sorry, friend. I can't autocomplete filepaths yet.
I hope my lack of skills didn’t slow you down
and you managed to do all the planned things.""", ""]

    def complete_cowsay(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        if len(words) != 1:
            match words[-2]:
                case '-t':
                    return ["Sorry, I can't complete text for you", ""]
                case '-c':
                    return [cow for cow in cowsay.list_cows() if cow.startswith(text)]
                case '-e':
                    return list(self.eyes_preset)
                case '-T':
                    return list(self.tongue_preset)

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.complete_cowsay(text, line, begidx, endidx)


if __name__ == '__main__':
    CowsayCmd().cmdloop()
