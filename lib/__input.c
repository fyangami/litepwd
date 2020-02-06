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


int __user_choose(char *lines[], int len)
{
    printf("\033[?25l"); // cursor hidden.
    for (int i = 0; i < len; ++i) // forEach item
    {
        printf("   ");
        printf("%s\n", lines[i]);
    }
    int selected = 0;
    printf("\033[%dA\r", len);  // Move the cursor to the begining of the line.
    print_green(" > ");  // selected line.
    print_green(lines[0]);
    // init finished.
    while (1)
    {
        int choose = user_choose_get_key(); // get input key
        if (choose == UP_FLAG)   //  arrow up
        {
            if (selected > 0)
            {
                // reset
                printf("\r   %s", lines[selected--]);
                // print select
                printf("\033[1A\r");
                print_green(" > ");
                print_green(lines[selected]);
            }
        } 
        else if (choose == DOWN_FLAG) // arrow down
        {
            if (selected < len - 1)
            {
                // reset
                printf("\r   %s", lines[selected++]);
                // print select
                printf("\033[1B\r");
                print_green(" > ");
                print_green(lines[selected]);
            }
        }
        else if (choose == ENTER)  // to select
        {
            printf("\033[?25h\033[%dB\r", len - selected); // after output.
            return selected;  // return the index of lines.
        }
        else if (choose == KEYBOARD_INTERRUPT)
        {
            printf("\033[?25h\033[%dB\r", len - selected); // after output.
            return KEYBOARD_INTERRUPT;  // return the index of lines.
        }
    }
}

static inline void print_green(char * msg)
{
    printf(COLOR_LIGHT_GREEN);
    printf("%s", msg);
    printf(COLOR_RESET);
}

static int user_choose_get_key()
{
    int ch = (int)getch();
    if (ch == 27)
    {   
        getch();
        char c = getch();
        if (c == 'A') return UP_FLAG;
        if (c == 'B') return DOWN_FLAG;
    }
    if (ch == KEYBOARD_INTERRUPT) 
    {
        printf("\033[?25h");
        return KEYBOARD_INTERRUPT;
    }
    if (ch == 10) return ENTER;
    if (ch == KEYBOARD_INTERRUPT) return KEYBOARD_INTERRUPT;
    return -2;
}


static inline char getch()
{
    system(ECHO_OFF);
    char ch = getche();
    system(ECHO_ON);
    return ch;
}


static inline char getche()
{
    char ch;
    system(ICANON_OFF);
    ch = getchar();
    system(ICANON_ON);
    return ch;
}
