#### Parser to use: https://tree-sitter.github.io/tree-sitter/  
Check out this playground to see what tree-sitter turns C code into: https://tree-sitter.github.io/tree-sitter/playground

#### SMT solver to use: https://github.com/z3prover/z3

TODO: \
-[ ] Make description of parsed output\
-[ ] make note of what to ignore and what to keep (ex, ignore imports)
-[ ] Function to traverse tree.\
Functionality for each statement below:\
-[ ] variable declaration (int x;)\
-[ ] variable assignment (int x = y;)\
-[ ] if- and if-else-statements (if (x == 0) { ... }, if (x == 0) { ... } else { ... })\
-[ ] while loops (while (x < 10) { ... })\
-[ ] return statements (return x;)\
Functionality for each expression below:\
-[ ] integer literals (41)\
-[ ] integer variables (x)\
-[ ] addition (x + y)\
-[ ] subtraction (x - y)\
-[ ] multiplication (x * y)\
-[ ] division (x / y)\
-[ ] negation (-x)\
-[ ] pre- and post-increment (++x, x++)\
-[ ] pre- and post-decrement (--x, x--)\
-[ ] boolean expressions\
-[ ] equality (x == y)\
-[ ] inequality (x < y, x <= y, x > y, x >= y)\
\
-[ ] Ability to check feasability of states
