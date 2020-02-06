#include<stdio.h>
#ifndef __INPUT_HEAD
#define __INPUT_HEAD
#define KEYBOARD_INTERRUPT -1
#define ASCII_IGNORED 32
#define ECHO_OFF "stty -echo"
#define ECHO_ON "stty echo"
#define ICANON_OFF "stty -icanon"
#define ICANON_ON "stty icanon"
#define STRING_TAIL '\0'
#define COLOR_CYAN "\033[36m"
#define COLOR_LIGHT_GREEN "\033[1;32m"
#define COLOR_RESET "\033[0m"
#define CURSOR_OFF "\033[?25l"
#define CURSOR_ON "\033[?25h"
#define BACKSPACE "\033[1D"
#define DELETE_CHAR "\033[1X"
#define ASCII_DEL 127
#define UP_FLAG 1
#define DOWN_FLAG 2
#define ENTER 10

int system(char *command);
static inline char getche();
static inline char getch();
static inline void print_green(char *);
static int user_choose_get_key();
int __input(char *, char *);
int __user_choose(char *lines[], int);
#endif
