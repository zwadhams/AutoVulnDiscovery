To install angr on Ubuntu 24.01 LTS, follow these steps:
```
sudo apt-get update
sudo apt-get install python3-dev build-essential
sudo apt install python3.10-venv
python3 -m venv angr-env
source angr-env/bin/activate
pip install --upgrade pip
pip install angr
pip install angr-management
pip install angr-utils
sudo apt update
sudo apt install graphviz
```
Verify the Installation: To confirm that angr is installed correctly, run:
```
python -c "import angr; print(angr.__version__)"
```

Note: the afl-fuzz and afl-frida-trace.so files in this directory were compiled with less optimizations in order to visualize more function names. The executables in the Frida Example directory should run faster.

angr-management is run with:
```
angr-management
```
And then you can select the afl-fuzz binary and run the tool with the default configuration. Just hit ok.
