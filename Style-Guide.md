Style Guide for ENGI E1006
======

**Note:** This style guide borrows heavily from the PEP-8 guidelines, but
focuses on aspects of the guidelines that are most relevant to the course.
Students are _encouraged_ to view the original PEP-8 guidelines at
https://www.python.org/dev/peps/pep-0008/, and familarize themselves with it.

##Why Style?##

Style is often considered secondary to functional code. However, as you will
realize, while debugging code, programmers often spend more time reading code
than writing it. Thus, having well written code that follows specific style
conventions simplifies the task of reading one's own code, as well as code
written by teammates or coworkers. Let's take a look at two pieces of code to
see how style improves the readability of code:

_Sample 1_
```python
def euclid(a, b):

    if a < b:
        t = a
        a = b
        b = t
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

def main():
    print "(i,j) -> GCD"
    for i in range(1, 10):
        for j in range(i, 10):
            print "(" + str(i) + "," + str(j) + ") ->", euclid(i,j)

main()
```

_Sample 2_
```python
##########################
# Name : Amar Dhingra
# UNI  : asd2157
#
# File contains function that computes the GCD of two numbers and tester
##########################

def euclid(a, b):
    ''' Function that computes the greatest common divisor of two numbers using
    the Euclidean algorithm'''
    # determine which of the two numbers is larger
    if a > b:
        larger = a
        smaller = b
    else:
        larger = b
        smaller = a

    # running euclids algorithm to determine the gcd
    while not smaller == 0:
        remainder = larger % smaller
        larger = smaller
        smaller = remainder

    # returning the gcd
    return larger


def main():
    ''' Tester for euclidean algorithm'''

    # printing out the gcd for all pairs of numbers from 1 to 9
    print "(i,j) -> GCD"
    for i in range(1, 10):
        for j in range(i, 10):
            print "(" + str(i) + "," + str(j) + ") ->", euclid(i,j)

main()
```

Both of these pieces calculate the greatest common divisor of two numbers using
the Euclidean algorithm (http://en.wikipedia.org/wiki/Euclidean_algorithm) and
then prints the divisor out.

However, Sample 2 is clear to read and easy to follow in such a manner that
even the most inexperienced programmers can follow and understand what the
program is doing. Sample 1 is probably unreadable to most people, except for
the author, and it would even take experienced programmers a few minutes to
understand it.

Below, we will examine what coding practices and conventions make the code from
_Sample 1_ easier to read, as well as the style guidelines you will be expected
to follow for this class.

##1. Header##
A header is the first thing someone sees when they open a Python file
(disregarding the shebang line). As such, the header should provide the user
with information about the author of the file, as well as a short overview of
what the functions are in the file.

If the whole file is one program, the header should have a summary of what the
program does. If the file holds helper functions for some other external
program (not contained in the file), it should state what program the helper
functions belong to and an overview of what the functions do.

###For This Class###
Your header should contain at least three things:

1. Your Name

2. Your UNI, and

3. 1 - 2 line overview describing what the functions in the file do

##2. Import Statements##
Programmers (both amateur and professional) very rarely work on projects that
do not require the use of built-in libraries. Python allows a programmer to use
functions from external files by importing the file using an `import`
statement. Functions from an external file can be used anywhere within the
scope of an import statement, so it is often convenient to call an import
statement within a funciton. **HOWEVER**, this should be avoided as much as
possible. It is poor style to import external modules in a function; it is
good style to have all import statements at the top of the file, directly
under the header. This allows the imports to be global and affect the whole
program, rather than one specific function.

###For This Class###
You will be expected to have all your `import` statements declared globally;
that is, at the top of the file, directly under the header.

##3. Whitespace##
Adding whitespace to code is the easiest way to make unreadable code readable.
There are three areas in which whitespace should be used to maximize
readability:

1. single line operations

2. within functions, and

3. between functions

###Single Line Operations###
Single line operations (such as varaible assignments or algebraic operations)
can be made more readable by adding appropriate amounts of whitespace. By
convention, binary operators such as `=`, `+`, `-`, `*`, `/`, and `%` should
have a single space around one side. Unary operators such as `-` should only
have one space, in order to distinguish them from other types.

####Example####
```python
test=(a*2+-4)/6
```

can be more easily read as
```python
test = (a * 2 + -4) / 6
```

###Within Functions###
Within functions, whitespace should be used to break code into logical blocks;
thus, making it easier to follow what the function is doing. This
sectionalization has the added benefit of making debuggign easier, as the
astute programmer can now locate bugs in one logical block of a (sometimes)
larger function.

In Sample 2, we broke the Euclidean algorithm into three sections: Determine
which number is larger, apply the algorithm, and return the appropriate value.

###Between Functions###
As per Sample 2, whitespace should be used to clearly demarcate functions by
adding two lines between each function.

###For This Class###
You are expected to include space inbetween assignment and algebraic operations
within single lines of code. Similarly, you should include one line of
whitespace between logical blocks of code in functions, and two whitespaces
between different functions.

