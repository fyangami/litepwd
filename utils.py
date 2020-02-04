# utils.py by fyang

from ctypes import cdll, c_int, c_char_p
from binascii import hexlify
from hashlib import pbkdf2_hmac
from random import seed, randint


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
          '[', '{', '}', ']', '\\', '\'', '"',
          ':', ';', ',', '<', '.', '>', '/', '?']
CHARACTERS = [chr(ch) for ch in range(65, 91)] + [chr(ch) for ch in range(97, 123)]
DIGITS = [_ for _ in range(10)]


def print_green(msg: str):
    __print_color("GREEN", msg)


def print_red(msg: str):
    __print_color("RED", msg)


def print_cyan(msg: str):
    __print_color('CYAN', msg)


def __print_color(color, msg):
    print(TERMINAL_COLORS[color], msg, TERMINAL_COLORS['RESET'])


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


def gen_hash(user: str, password: str) -> str:
    _salt = __random(user)
    bs = pbkdf2_hmac("sha256", password.encode("utf8"), _salt.encode("utf8"), 1000)
    return hexlify(bs).decode("utf8")


def __random(s: str) -> str:
    bs = s.encode("utf8")
    _seed = 0
    for b in bs:
        _seed += b
    seed(_seed)
    return str(randint(1000000, 9999999))
