Python 3.11 Release Notes

## Major New Features
Python 3.11 is between 10-60% faster than Python 3.10. On average, we measured a 1.25x speedup on the standard benchmark suite. The Faster CPython Project has been focused on improving the performance of the interpreter, and many of the changes in 3.11 are the result of this work.

### Exception Groups and except*
PEP 654 introduces Exception Groups and the new except* syntax for handling multiple exceptions. This feature is particularly useful for concurrent code where multiple tasks may fail independently with different exceptions.

### Improved Error Messages
The error messages in Python 3.11 have been significantly improved. The interpreter now provides more precise information about where errors occur, including pointing to the exact column of the error in the source line.

## Typing Features

### Self Type
PEP 673 introduces the Self type, which can be used to annotate methods that return an instance of their class. This is particularly useful for builder patterns and fluent interfaces.

### Variadic Generics
PEP 646 introduces Variadic Generics, allowing generic types to be parameterized by an arbitrary number of types. This is a advanced feature primarily used by libraries that work with tensors and arrays.

## Standard Library Changes

### tomllib
A new module tomllib has been added to the standard library for parsing TOML files. This provides built-in support for reading TOML configuration files without the need for third-party libraries.

### asyncio Improvements
The asyncio module has received several improvements, including the addition of TaskGroup which provides a more structured way to manage concurrent tasks, similar to the trio library.

## Deprecations and Removals
Several deprecated features have been removed in Python 3.11, including the smtpd module, the distutils package, and several legacy modules. The deprecated C APIs have also been cleaned up.

The Python community continues to work on improving the language while maintaining backward compatibility. Python 3.11 represents a significant step forward in terms of performance, developer experience, and language features.