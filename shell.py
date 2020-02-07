# command.py by fyang

from litepwd import __config

__PROMPT = f"\033[1;32mlitepwd@{__config['user']}:\033[0m"


def get_shell(sqlcipher):
    while True:
        print(__PROMPT, end="")



