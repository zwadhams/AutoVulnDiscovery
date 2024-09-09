## Example: 
https://owasp.org/www-community/attacks/Command_Injection <br />

Before this will work you will need to find yourself a gcc compiler for the Makefile.

## Commands: <br />
Compile the program:
```
make
```
There is now an executable file called `final_program` in the `build` folder and a prebuilt input string `input.txt` in the main folder. Run the program with the input file using:
```
./build/final_program input.txt
```
You should see `If you're seeing more than this message command injection may have occurred...`. Now let's exploit our code. Run:
```
./build/final_program "input.txt; ls"
```
Here we are command injecting the command `ls` to see what else is in our current directory. If done correctly you should see the contents of the folder you are in.

```
./build/final_program "input.txt; ./set_background.sh"
```
For a more fun example try the command above
