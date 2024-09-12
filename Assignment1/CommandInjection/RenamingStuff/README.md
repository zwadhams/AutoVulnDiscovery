How to use:

1. Make sure that the commandinjection exploit generally works.
2. run ```bash setup.sh``` to create file structure
3. run ```dependentScript.sh```. This script requires one of the files created in the prior setup to accomplish its task.
4. now run the exploit and chain "bash movingExploit.sh" to the main exploit. Ex: ```./build/final_program "input.txt; bash movingExploit.sh"```
5. run ```bash dependentScript.sh``` again. The script should give an error because the file is no in its known location and therefore the script cannot read it. 
