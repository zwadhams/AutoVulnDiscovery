#!/bin/bash

message1="Setting up folders"
echo "Making directory" $(mkdir SecretDependentStuff)
echo "And a file" $(touch SecretDependentStuff/secret1.txt)
$(echo "I'm here" >> SecretDependentStuff/secret1.txt)
echo "Or two" $(touch SecretDependentStuff/secret2.txt)
