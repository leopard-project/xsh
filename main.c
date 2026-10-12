#include "xtuiapi.h"   /* xapi_* + libsys.h(enter_syscall/XAPI_INPUT) + krlibc.h(字符串) */

#define LINE_CAP  256
#define MAX_ARGS  16

int main(int argc, char *argv[], char *envp[])
{
    (void)argc;
    (void)argv;
    (void)envp;

    for (;;) {
        xapi_Printf("xj380$ ");

        char line[LINE_CAP] = {0};
        enter_syscall(XAPI_INPUT, (uint64_t)line, sizeof(line), 0, 0, 0, 0);
        if (line[0] == '\0')
            continue;

        if (strcmp(line, "exit") == 0)
            return 0;
        if (strcmp(line, "clear") == 0) {
            xapi_Printf("\033[2J\033[H");
            continue;
        }

        char *args[MAX_ARGS];
        int   n = 0;
        for (char *tok = strtok(line, " \t"); tok && n < MAX_ARGS - 1;
             tok = strtok(NULL, " \t"))
            args[n++] = tok;
        args[n] = NULL;
        if (n == 0)
            continue;

        char path[LINE_CAP];
        snprintf(path, sizeof(path), "/apps/%s", args[0]);

        int64_t result = (int64_t)xapi_RunArgs((WSTR)path, (WSTR *)args);
        if (result < 0)
            xapi_Printf("command not found\n");
    }
}

