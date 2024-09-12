## Example: 
https://owasp.org/www-community/attacks/Command_Injection <br />

Before this will work you will need to find yourself a gcc compiler for the Makefile.

## Commands: <br />
Compile the program:
```
make
```
Now let's make the file execuatable. Run:
```
chmod +x /path/to/statcat
```
There is now an executable file called `statcat` in the `build` folder and a prebuilt input string `input.txt` in the main folder. Run the program with the input file using:
```
./build/statcat input.txt
```
You should see `If you're seeing more than file data and this message command injection may have occurred...`. Now let's exploit our code. Run:
```
./build/statcat "input.txt; ls"
```
Here we are command injecting the command `ls` to see what else is in our current directory. If done correctly you should see the contents of the folder you are in. It will do this twice as both `stat` and `cat are called in our `statcat` program. 

Now lets make `statcat` a real linux command! Run the following command to place a symlink to this program in `/usr/local/bin`

```
sudo ln -s /path/to/my_script /usr/local/bin
```
Now you can run `statcat` anywhere in your filesystem to return file data and contents. Be careful though, this new fun linux command is still injectable!
```
./build/statcat "input.txt; ./set_background.sh"
```
For a more fun example try the command above (only on Linux)
