# Pylint

- If the import did show `resolvedPylancereportMissingImports` or something about not being able to resolve the import, and you have a virtual env. You might be able to solve it in VSCode by opening the Command Palette (`Ctrl+Shift+P`) and changing the python version. So type "Python: Select Interpreter".

## Generate a New `.pylintrc` File

```bash
pylint --generate-rcfile > .pylintrc
```

## `.pylintrc` Config File

```txt
[MAIN]

[BASIC]

# Naming style matching correct argument names.
argument-naming-style=snake_case

# Naming style matching correct attribute names.
attr-naming-style=snake_case

# Bad variable names which should always be refused, separated by a comma.
bad-names=foo,
          bar,
          baz,
          toto,
          tutu,
          tata

# Naming style matching correct class attribute names.
class-attribute-naming-style=snake_case

# Naming style matching correct class constant names.
class-const-naming-style=UPPER_CASE

# Naming style matching correct class names.
class-naming-style=PascalCase

# Naming style matching correct constant names.
const-naming-style=UPPER_CASE

# Minimum line length for functions/classes that require docstrings, shorter
# ones are exempt.
docstring-min-length=-1
missing-module-docstring

# Naming style matching correct function names.
function-naming-style=snake_case

# Good variable names which should always be accepted, separated by a comma.
good-names=i,
           j,
           k,
           ex,
           Run,
           _

# Include a hint for the correct naming format with invalid-name.
include-naming-hint=no

# Naming style matching correct method names.
method-naming-style=snake_case

# Naming style matching correct module names.
module-naming-style=snake_case

# Naming style matching correct variable names.
variable-naming-style=snake_case

[CLASSES]

[DESIGN]

[EXCEPTIONS]

# Exceptions that will emit a warning when caught.
overgeneral-exceptions=builtins.BaseException,builtins.Exception

[FORMAT]

[IMPORTS]

[LOGGING]

[MESSAGES CONTROL]

[METHOD_ARGS]

[MISCELLANEOUS]

# List of note tags to take in consideration, separated by a comma.
notes=FIXME,
      XXX,
      TODO

[REFACTORING]

# Maximum number of nested blocks for function / method body
max-nested-blocks=3

[REPORTS]

[SIMILARITIES]

# Comments are removed from the similarity computation
ignore-comments=yes

# Docstrings are removed from the similarity computation
ignore-docstrings=yes

# Imports are removed from the similarity computation
ignore-imports=yes

# Signatures are removed from the similarity computation
ignore-signatures=yes

# Minimum lines number of a similarity.
min-similarity-lines=4

[SPELLING]

[STRING]

# This flag controls whether inconsistent-quotes generates a warning when the
# character used as a quote delimiter is used inconsistently within a module.
check-quote-consistency=no

[TYPECHECK]

[VARIABLES]
```
