The description of this functionality is in the Project Report. Please refer to it.<br>

Allow core dumps to come to the working directory:
```
sudo sh -c 'echo core >/proc/sys/kernel/core_pattern'
```
Note: we redirect the core dump to the output directory. <br><br>
Fuzzing command:
```
AFL_DEBUG=1 AFL_FRIDA_JS_SCRIPT=./afl.js ./afl-fuzz -O -G 6 -i input -o output -- ./fuzz
```
