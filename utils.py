# utils.py by fyang

from ctypes import cdll, c_int, c_char_p
from binascii import hexlify
from hashlib import pbkdf2_hmac
from random import choice
from sys import stdin
from os import system
from time import localtime, strftime


UP_CODE = b"\x1b[A"
DOWN_CODE = b"\x1b[B"
RIGHT_CODE = b"\x1b[C"
LEFT_CODE = b"\x1b[D"
TERMINAL_COLORS = {
    "RESET": '\033[0m',
    "RED": '\033[31m',
    "GREEN": '\033[32m',
    "CYAN": '\033[36m',
    "LIGHT_GREEN": '\033[1;32m',
}
ERROR_MSG = f"{TERMINAL_COLORS['RED']}incorrect argument! please using --help and try again!{TERMINAL_COLORS['RESET']}"

SYMBOL = ['~', '`', '!', '@', '#', '$', '%', '^',
          '&', '*', '(', ')', '-', '_', '=', '+',
          '[', '{', '}', ']', '\\', '"',':', ';',
          ',', '<', '.', '>', '/', '?']
CHARACTERS = [chr(ch) for ch in range(65, 91)] + [chr(ch) for ch in range(97, 123)]
DIGITS = [str(_) for _ in range(10)]

DATE_FMT = "%Y-%m-%d %H:%M:%S"


def print_green(msg: str, end='\n'):
    __print_color("GREEN", msg, end)


def print_red(msg: str, end='\n'):
    __print_color("RED", msg, end)


def print_cyan(msg: str, end='\n'):
    __print_color('CYAN', msg, end)


def __print_color(color, msg, end):
    print(TERMINAL_COLORS[color], msg, TERMINAL_COLORS['RESET'], end=end)


def __pwd_input(prompt: str) -> str:
    __input = cdll.LoadLibrary("./lib/__input.so").__input
    __input.restype = c_int
    __input.argtypes = [c_char_p, c_char_p]
    __pwd = bytes(b"0"*10)
    __input(bytes(prompt.encode("utf8")), __pwd)
    pwd = ""
    for ch in __pwd:
        if ch == 0x00:
            break
        pwd += chr(ch)
    return pwd


def __user_choose(choose_list: list) -> int:
    try:
        user_choose = cdll.LoadLibrary("./lib/__input.so").__user_choose
        user_choose.restype = c_int
        c_str_arr = c_char_p * len(choose_list)
        user_choose.argtypes = [c_str_arr, c_int]
        arr = c_str_arr()
        for i in range(len(choose_list)):
            arr[i] = choose_list[i].encode()
        select = user_choose(arr, len(choose_list))
        print(f"\033[{len(choose_list) - select}B\r", end="")  # reset failed int c.... fix it!
        return select
    except KeyboardInterrupt:
        exit(0)
    finally:
        print("\033[?25h", end="")


def gen_hash(user: str, password: str) -> str:
    bs = pbkdf2_hmac("sha256", password.encode("utf8"), user.encode("utf8"), 1000)
    return hexlify(bs).decode("utf8")


def gen_password(length=16) -> str:
    if length < 16:
        error_exit("length too short!")
    password = ["*" for _ in range(length)]
    seq = [i for i in range(length)]
    a = choice(seq)
    seq.remove(a)
    b = choice(seq)
    seq.remove(b)
    c = choice(seq)
    seq.remove(c)
    password[a] = choice(SYMBOL)
    password[b] = choice(DIGITS)
    password[c] = choice(CHARACTERS)
    for index in seq:
        password[index] = choice(SYMBOL + DIGITS + CHARACTERS)
    return "".join(password)


def format_print_store(stores: list, hidden=True):
    print("{:^20}  |  {:^20}  |  {:^20}  |  {:^16}".format("store_name", "group", "    create_time    ", "password"))
    print("#"*90)
    for store in stores:
        print("{:^20}  |  {:^20}  |  {:^20}  |  {:^16}".format(
            store['name'],
            store['_group'],
            strftime(
                DATE_FMT,
                localtime(int(store['create_time']))
            ),
            "?" if hidden else store['password']
        ))
    if not len(stores):
        print("{:^20}  |  {:^20}  |  {:^20}  |  {:^16}".format("-", "-", "-", "?"))
    print("#"*90)


def error_exit(msg='Unknown error! please try again.'):
    print_red(msg)
    exit(0)
