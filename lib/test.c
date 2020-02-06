#include<stdio.h>
#include "__input.c"

int main()
{
    // get_key();
    char* arr[] = {
        "fyangami.com.cn",
        "www.baidu.com",
        "www.github.com",
        "www.google.com",
        "fyangami.org"
    };
    printf("%d\n", __user_choose(arr, 5));
    return 0;
}