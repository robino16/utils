# Utilities

## Progress Bar (Python)

> utils/progress_bar.py

A simple progress bar class for Python applications.

    Progress: |█████████████████       | 80/100 (80%) ETA: 2s

**Example usage:**

```python
from progress_bar import ProgressBar

epochs = 100
bar = ProgressBar(epochs, resolution=1000)
for i in range(epochs)
    # do tasks here
    bar.set(i) # alternatively use: bar.next()
bar.finish()
```

## File I/O Service (Python)

> utils/file_io.py

A simple service for handling files and directories. 

**Example usage:**

```python
from file_io import FileIO

FileIO.append_line('my_file.txt', 'Hello, World!')
```

## PDF Freeze

> utils/pdf_freeze.py

Great for finalizing confidential PDF documents. 
Converts a PDF into JPG, then back to PDF. 
Reduces risk of PDF tampering.
Make signatures made with Adobe Acrobat static
so that no one can copy/steal your signature. 

**Example usage:**

From a terminal window:

```bash
python -m pdf_freeze --i original.pdf --o freezed.pdf
```

!!! important
    See dependencies inside the script file. 

## String Search & Replace

> utils/string_replace.py

Tool for renaming variables/replacing strings in a project. 
Some IDEs (e.g. SEGGER Embedded Studio) does not feature
proper refactoring of variables. 
Thus, this script was made to make life a little bit easier. 

**Example usage:**

From a terminal window:

```bash
python -m string_replace
```

Then follow the on-screen prompts. 
Here we replace bananas with apples:

    apple.c
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    found 'banana'
    in file '.\bananas\apple.c'

        occurrence #1
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        line #1:       "i have a banana"
              ->       "i have a apple"

                       ACCEPTED

## App Config Template

> templates/app_config.py

Template for app config useful in larger python applications. 
Modify the template to your desires. 

**Example usage:**

```python
import app_config

CONF = app_config.conf
LOG = app_config.log

MY_PARAMETER = CONF.parameter
LOG.info(f'using parameter:{MY_PARAMETER}')
```
