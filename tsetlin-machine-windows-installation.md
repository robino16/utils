# Installing pyTsetlinMachine on a Windows Host

This is a guide on how to install the Tsetlin Machine Python package ([pyTsetlinMachine](https://github.com/cair/pyTsetlinMachine)) on a Windows host. 
pyTsetlinMachine installs easily on both Mac and Linux hosts using pip:

    pip install pyTsetlinMachine

Currently this does not work on Windows systems. 
If you are using a Windows machine, you can use services such as [Colaboratory](https://colab.research.google.com/) or on a virtual machine (VM). 
If you still intend to use pyTsetlinMachine locally on a Windows host, this is a short guide to help you. 

!!! note
    This is not an official installation guide.
    Any feedback is greatly appreciated. 

## Prerequisites

* [Python 3.7.x](https://www.python.org/downloads/) (We've tested Python 3.7.9)
* [C++ Build Tools 14.0](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019) or higher
* A make program (such as [MinGW](https://osdn.net/projects/mingw/releases/))
    * If using MinGW, make sure to install all it's primary components. 

## Step 1: Clone The Repository

Clone the ([pyTsetlinMachine GitHub repository](https://github.com/cair/pyTsetlinMachine)) to your local machine.

    git clone https://github.com/cair/pyTsetlinMachine.git
 
This will give you the latest version of the package (in our case version 0.5.9).

## Step 2: Add Missing Headers

The C source for the Tsetlin Machine is contained in the "pyTsetlinMachine" sub folder ("pyTsetlinMachine/pyTsetlinMachine/"). 
Here, the source file "IndexedTsetlinMachine.c" tries to include a header file called "sys/time.h". 
Unfortunately, This file do not exist on Windows.
We can instead use a [sys/time.h Replacement](https://www.codefull.net/2015/12/systime-h-replacement-for-windows/).
Place all the replacement files ("time.h", "time.cpp" and "times.h") under "pyTsetlinMachine/pyTsetlinMachine/sys/".
Now the compiler should be able to find those header files. 

## Step 3: Compile libTM

To make the required library file, we can use a make program, such as MinGW. 
Inside the same directory as the "makefile" ("pyTsetlinMachine/pyTsetlinMachine/") type:

    make

or if you are using MinGW with default settings:

    ming32-make

This will output a shared library (.so) file called "libTM.so" which we'll need later.

## Step 4: Run setup.py

If you want to install pyTsetlinMachine in a virtual environment, first, activate that virtual environment. 
This can be done by typing the path to the venv's "activate.bat" script. 

    venv\Scripts\activate.bat

In the main directory "pyTsetlinMachine/" type:

    python setup.py install

You will likely get a linking error ("LNK2001: unresolved external symbol PyInit_libTM"). 
The command will still create a "build/" directory with a couple of temporary build files. 

## Step 5: Overwrite libTM

Inside the build directory "pyTsetlinMachine/build/" you should able to locate an empty library file (.pyd file with 0KB file size).
In our case it was called: "libTM.cp37-win_amd64.pyd".
Give the library file we compiled earlier ("libTM.so") the same filename: "libTM.cp37-win_amd64.pyd".
Then overwrite the empty library file with the one that we compiled.  

## Step 6: Run setup.py (Once More)

Now run the setup once more:

    python setup.py install

The _pyTsetlinMachine_ package should now be installed in your Python interpreter. 
To quickly test it, see if you can type:

    python
    from pyTsetlinMachine.tm import MultiClassTsetlinMachine

If you do not get any error messages, you've successfully installed the package. 
