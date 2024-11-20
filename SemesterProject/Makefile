# Compiler and flags
CC = gcc
CFLAGS = -g -O0
TARGET = main
SRC = main.c

# Default target: Build and execute
all: $(TARGET) run_uprobe

# Compile the target
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

# Clean up generated files and processes
clean:
	rm -f $(TARGET)



