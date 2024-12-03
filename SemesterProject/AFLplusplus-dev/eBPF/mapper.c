#include <stdio.h>
#include <stdlib.h>

int main() {
    // Path to the Python script
    const char *pythonScriptPath = "SemesterProject/hello.py";

    // Command to execute the Python script
    char command[256];
    snprintf(command, sizeof(command), "python3 %s", pythonScriptPath);

    // Execute the command
    int result = system(command);

    // Check if the command was executed successfully
    if (result == -1) {
        perror("system");
        return 1;
    }

    printf("Python script executed successfully\n");
    return 0;
}