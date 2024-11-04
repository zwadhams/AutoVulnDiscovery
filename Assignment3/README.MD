# Steps to run
## 1. Download `Symbolic_Ex.py` and `test_program.c`
## 2. Run `Symbolic_Ex.py` with `test_program.c` as an argument
Ex: `python3 Symbolic_Ex.py test_program.c`

TODO




DELETE EVERYTHING BELOW UPON TURNIN
#### Parser to use: https://tree-sitter.github.io/tree-sitter/  
Check out this playground to see what tree-sitter turns C code into: https://tree-sitter.github.io/tree-sitter/playground

#### SMT solver to use: https://github.com/z3prover/z3

TODO: \
-[ ] Make description of parsed output\
-[ ] make note of what to ignore and what to keep (ex, ignore imports)
-[x] Function to traverse tree.\
Functionality for each statement below:\
-[x] variable declaration (int x;)\
-[x] variable assignment (int x = y;)\
-[x] if- and if-else-statements (if (x == 0) { ... }, if (x == 0) { ... } else { ... })\
-[ ] while loops (while (x < 10) { ... })\
-[ ] return statements (return x;)\
Functionality for each expression below:\
-[ ] integer literals (41)\
-[ ] integer variables (x)\
-[x] addition (x + y)\
-[x] subtraction (x - y)\
-[x] multiplication (x * y)\
-[x] division (x / y)\
-[ ] negation (-x)\
-[ ] pre- and post-increment (++x, x++)\
-[ ] pre- and post-decrement (--x, x--)\
-[ ] boolean expressions\
-[ ] equality (x == y)\
-[ ] inequality (x < y, x <= y, x > y, x >= y)\
\
-[ ] Ability to check feasability of states
