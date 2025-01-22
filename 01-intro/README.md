# Installing Python Interpreter

## What is an Interpreter?

You might wanna ask what is interpreter, in the layman's terms (tell me like i am 5), it is a software that:

1. Takes your python code.
2. Read the first line.
3. Translate it to what computers understand.
4. Execute the translated result.
5. Computer act upon it.
6. It goes to the next line.
7. If there is more code, it repeats steps 3 to 6 until it finishes executing your python code.

![Interpreter as translator](./assets/interpreter-translator.png)

> [!NOTE]
>
> Number systems: binary, octal, decimal, hexadecimal
>
> ![Number systems](./assets/number-systems.png)

## Windows

![Downloading Python for Windows](./assets/win-download-process.png)

After it finished downloading, open the downloaded file.

![Opening file](./assets/open-python-file.png)

Then you must check the option to add python to your path:

![First page of python installer](./assets/first-page-of-python.png)

Allow python installer make changes on your device:

![allow installer to install python](./assets/allow-installer-to-install-python.png)

Confirm python installation:

![Open run](./assets/open-run.png)

Open CMD:

![Open CMD](./assets/open-cmd.png)

Type `python --version` and hit enter:

![Printed python version in terminal](./assets/python-version-in-terminal.png)

# IDE -- VSCode

There might be others who use things like [PyCharm](https://www.jetbrains.com/pycharm/), [Intellij IDEA](https://www.jetbrains.com/idea/). BTW Python wiki also has somethings to say about this. So if you're interested in their recommendations please read [this](https://wiki.python.org/moin/IntegratedDevelopmentEnvironments).

> [!NOTE]
>
> IDE stands for **I**ntegrated **D**evelopment **E**nvironment.

## Download & installation

1. Download it from [here](https://code.visualstudio.com/).
2. Open it and accept terms of service:

   ![accepting terms of service](./assets/install-vscode-terms-of-service.png)

3. Pick a location on your hard drive if you like, but like I've already suggested in the folowing screenshot, do not change if you do not have any reason to do so and just click on "Next":

   ![VSCode install location](./assets/vscode-install-location.png)

4. ![Click next](./assets/start-menu-vscode.png).
5. Create its icon on desktop if you like, but those two other options will make your life much much easier:

   ![Add some actions to your right click](./assets/add-vscode-to-desktop.png)

6. ![CLick on Install](./assets/install-vscode-page.png)
7. ![alt text](./assets/finished-vscode-installation-page.png)

## Configurations

1.  Choose a theme:

    ![Choose a theme](./assets/vscode-initial-page-choose-theme.png)

2.  Install ["Python"](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension for VSCode. This will give you stuff like:

    - Intellisense.
    - Debugging.
    - Formatting, linting, code navigation, refactoring, variable explorer, test explorer, and other convenience you might need while coding.

    Learn more about necessary extension in VSCode for coding in Python [here](../02-getting-started/better-dev-exp.md#vscode-extensions).

## Create a new python project

1. Create a new directory/folder on your desktop and call it "projects":

   ![alt text](./assets/create-new-folder.png)

2. Open it and inside it create a new directory called "HelloWorld".

   <a href="#namingConventions" id="namingConventions">#</a> BTW these are naming conventions are commonly used by many developers:

   ![naming conventions](./assets/naming-conventions.png)

3. Open "HelloWorld" with VSCode.

   You can do it inside file explorer:

   ![alt text](./assets/open-with-vscode.png)

   Or through VSCode:

   ![alt text](./assets/open-folder.png)

## Creating a virtual environment

- For your Python projects we need to create what is called virtual environment which is necessary.
- You can have multiple Python project which use different version of Python, thus you cannot every time for every project just reinstall it, right?
- We also might install 3rd party libraries, in which we do not wanna pollute our global environment.

1. Open Command Palette and type "Python create Environment": ![Create venv](./assets/create-venv.png)
2. Press enter.
3. Wait until it is done creating your virtual environment: ![Create venv in process](./assets/create-venv-in-process.png)
4. You can see that now your virtual env is dictating which Python version should be used in that project: ![alt text](./assets/venv-python-version.png)

## VScode shortcut keys

- Press `ctrl + z` to undo your changes. ![ctrl + z](./assets/ctrl-plus-z.png)
- Press `ctrl + y` to redo. ![ctrl + y](./assets/ctrl-plus-y.png)
- Press `ctrl + d` to kill a REPL. ![CTRL+D](./assets/ctrl-plus-d.png)
- Press <code>ctrl + `</code> to open terminal (it is called command prompt in windows): ![ctrl + backtick](./assets/ctrl-plus-backtick.png)
- Press `ctrl + shift + p` to open "command palette". ![ctrl + shift + p](./assets/ctrl-plus-shift-plus-p.png).

  - Here we can do things like opening a REPL (learn more about REPL [here](../02-getting-started/README.md#python-repl)).

    ![repl](./assets/repl.png)

## Final words

Do not be afraid of reading docs. I wanna show you how you could accomplish same results by just reading VSCode's official documentations:

1. Install VSCode on windows: search in google "Install VSCode on Windows".
2. How to configure newly installed VSCode for Python in Windows: Search in Google: "VSCode + windows + python".
3. How to know which short cut does what in VSCode. Google "VSCode shortcuts" or "VSCode shortcuts cheat sheet".

## YouTube/Aparat

- [https://youtu.be/qPH9oLuTBQk](https://youtu.be/qPH9oLuTBQk).
- [https://aparat.com/v/eyj6b83](https://aparat.com/v/eyj6b83).

# Python

- "Python" is actually a category of snakes:
  - It's not the name of a specific species.
  - It refers to a family of snakes called Pythonidae.
  - Known for their large size & non-venomous constriction method of hunting.
- But here we are talking about a programming language :).
- BTW the language is named after the BBC show ["Monty Python's Flying Circus"](https://www.imdb.com/title/tt0063929/).

## Why Python

### Powerful

- Can be extended/combined with other [programming languages](./glossary.md#programmingLanguageGlossary).

  ![Extension for python, written in C](./assets/pthone-extension-in-c.png)

  Imagine you have a big Lego set with pieces that build almost anything, but there are a few things you want to make that need super-special pieces that aren’t in the set. So, you ask someone who has those special pieces (like shiny or super-strong ones) to build those parts for you. Then, you add them to your Lego set, and now you can build even cooler stuff!

- <a href="#extensiveBuiltinLibrariesInPython" id="extensiveBuiltinLibrariesInPython">#</a> Extensive standard [library](./glossary.md#libraryGlossary); i.e. large collection of [modules](./glossary.md#moduleGlossary) and packages built into the language.
  ![Extensive standard library](./assets/python-extensive-builtin-lib.png)

### Versatile

- Can be used in different fields, domains, or types of [applications](./glossary.md#applicationGlossary).

  ![Some of python domains](./assets/some-of-python-domains.png)

- Runs everywhere.

  ![Python runs on Unix, Linux, Windows, Mac, iOS, Android](./assets/python-runs-on.png)

### Easy to learn

- Some blogs, podcasts:
  - [RealPython](https://realpython.com/).
  - [Planet Python](https://planetpython.org/).
  - [Podcast about Python](https://talkpython.fm/).
  - [Mouse vs. Python](https://www.blog.pythonlibrary.org/).
- Here are some online courses:
  - [edX](https://www.edx.org/learn/python).
  - [Python Essentials 1](https://www.netacad.com/courses/python-essentials-1?courseLang=en-US).
- And if you had any question you can ask in:
  - [Stackoverflow](https://stackoverflow.com/).
  - [Reddit's community for Python](https://www.reddit.com/r/Python/).

### Talk more technical

- Is equipped with efficient high-level [data structures](./glossary.md#dataStructureGlossary).
- Has an effective approach to [Object-Oriented Programming](./glossary.md#objectOrientedProgrammingGlossary).

  - Simplicity and readability: no steep learning curve.

    ![Hello world app in Assembly, C++, and Python](./assets/python-cpp-assembly.png)

  - Flexibility with multiple paradigms: sometimes you need to [mix and match](https://www.collinsdictionary.com/dictionary/english/mix-and-match).
  - Built-in support for OOP principles.

    ![OOP principles](./assets/oop-principles.png)

- Dynamically typed: no need to explicitly declare variable types, resulting in a faster and easier development experience.

  ![Dynamic typing vs static typing](./assets/dynamically-typed-staticly-typed.png)

- [Interpreted](#what-is-an-interpreter) programming language.

## So what now?

First we're gonna touch the most noteworthy aspects of Python. By the end of this journey we will be able to read and understand Python. Then we can jump into next section which is libraries that we need.

> [!NOTE]
>
> My goal here is to equip you with as much as arsenal I can so when you're out fighting your own battle you know how to read docs, ask questions, solve your problems and be a good developer.

### Download and print [this cheatsheet](./assets/cheatsheets/)

## Resources to practice Python

- https://checkio.org.
- https://www.afterhoursprogramming.com/tutorial/python/python-quiz.
- https://www.practicepython.org.
- https://pychallenger.com.

### Refs

- https://wiki.python.org/moin/BeginnersGuide.
- https://docs.python.org/3/tutorial/index.html.
- https://wiki.python.org/moin/BeginnersGuide/Overview.

## YouTube/Aparat

- [https://youtu.be/Ts3JhayINiY](https://youtu.be/Ts3JhayINiY).
- [https://aparat.com/v/rfiu8mf](https://aparat.com/v/rfiu8mf).
