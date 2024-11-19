Allow core dump:
```
sudo sh -c 'echo core >/proc/sys/kernel/core_pattern'
```

Fuzzing command:
```
AFL_DEBUG=1 AFL_FRIDA_JS_SCRIPT=./afl.js ./afl-fuzz -O -G 6 -i input -o output -- ./fuzz
```

