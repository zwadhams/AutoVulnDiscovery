#!/bin/bash

# Check if the binary is provided as an argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <binary>"
    exit 1
fi

BINARY="$1"

# Ensure the binary exists
if [ ! -f "$BINARY" ]; then
    echo "Error: File '$BINARY' not found."
    exit 1
fi

# Extract function names using objdump
echo "Extracting functions from '$BINARY'..."
FUNCTIONS=$(objdump -t "$BINARY" | awk '/F .text/ {print $6}' | sort | uniq)

# Check if any functions are found
if [ -z "$FUNCTIONS" ]; then
    echo "No functions found in '$BINARY'."
    exit 1
fi

# Display the functions and let the user select
echo "Please select a function number to trace. Available functions:"
select FUNCTION in $FUNCTIONS; do
    if [ -n "$FUNCTION" ]; then
        echo "Selected function: $FUNCTION"
        break
    else
        echo "Invalid selection. Please try again."
    fi
done

# Trace the selected function using the uprobe script
echo "Tracing function '$FUNCTION' using uprobe script..."
sudo python3 uprobe.py ./"$BINARY" "$FUNCTION"

# End of script
