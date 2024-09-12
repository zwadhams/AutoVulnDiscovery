#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

// This program combines the functions of stat and cat for streamiled file identification

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    char *command;
    size_t commandLength;

    // Calculate the total length required for the full command
    commandLength = strlen("stat ") + strlen(argv[1]) + strlen("; cat ") + strlen(argv[1]) + 1;

    // Allocate memory for the full command
    command = (char *) malloc(commandLength);

    // Construct the vulnerable command: "stat <filename>; cat <filename>"
    // Will execute injected code twice
    snprintf(command, commandLength, "stat %s; cat %s", argv[1], argv[1]);

    // Execute the command using system() with the unsanitized user input
    system(command);

    free(command);

    return 0;
}
