POR - Poorly Written Parallel Language in Python

Code requirements:

All Python code should be in column format, with each column representing a thread.
	Code should be flush against pipes - no whitespace.
	Modules must be imported per-thread, and shared variables must be declared using the 'global' keyword, in the first line (before all imports).

Sample code (sample.por):

global x		|				|global x
import random		|import multiprocessing		|import antigravity
x = random.random()	|print('from thread 2')		|x = x + 5
			|				|# expected: ~5.5
			|				|print(x)

Run `parser.py <POR file>` - this will generate a list of threaded files. Note that these files are dumped into the CWD, so please invoke the parser from an empty directory.
Run `compiler.py -d <directory> > <file>` - this outputs the final Python code to be run. There is a wrapper file, `por.sh <directory>`, which will run the output immediately.

See `compiler.py --help` for more information.

- Minke Zhang, Shir Yehoshua, Kevin Zhang
- v. 0.8.0, 17 Dec. 2012

Examples:

`blocks.py` - Demonstrates how both sequential and concurrent For loops can be instantiated using the base architecture - this has yet to be 
	implemented at the parser level.
`variables.py` - Demonstrates simple variable sharing.
