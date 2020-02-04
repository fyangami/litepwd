#include "__input.h"


int __input(char * prompt, char * ipt)
{
    printf(COLOR_LIGHT_GREEN);
    printf("%s", prompt);
    printf(COLOR_CYAN);
    char ch;
    int len = 0;
    printf(CURSOR_OFF);
    system(ECHO_OFF);
    while ((ch = getche()) != '\n')
    {
        if ((int) ch == KEYBOARD_INTERRUPT) break;
        if ((int) ch < ASCII_IGNORED) continue;  // 32一下ascii忽略
        if ((int) ch == ASCII_DEL) // 删除字符
        {
            if (len == 0) continue;
            printf(BACKSPACE);
            printf(DELETE_CHAR);
            ipt--;
            len--;
        }
        else
        {
            *ipt++ = ch;
            printf("*");
            len++;
        }
    }
    system(ECHO_ON);
    printf(CURSOR_ON);
    printf(COLOR_RESET);
    putchar('\n');
    *ipt++ = STRING_TAIL;
    return len;
}


static inline char getche()
{
    char ch;
    system(ICANON_OFF);
    ch = getchar();
    system(ICANON_ON);
    return ch;
}
