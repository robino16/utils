# Utilities

## Progress Bar (Python)

A simple progress bar class for Python applications.

    Progress: |█████████████████       | 80/100 (80%) ETA: 2s

**Example usage:**

```python
from progress_bar import ProgressBar

epochs = 100
bar = ProgressBar(epochs)
for i in range(epochs)
    # do tasks here
    bar.set(i) # alternatively use: bar.next()
bar.finish()
```

## File I/O Service (Python)

A simple service for handling files and directories. 

**Example usage:**

```python
from file_io import FileIO

FileIO.append_line('my_file.txt', 'Hello, World!')
```

## PDF Freeze

Great for finalizing confidential PDF documents. 
Converts a PDF into JPG, then back to PDF. 
Reduces risk of PDF tampering.
Make signatures made with Adobe Acrobat static
so that no one can copy/steal your signature. 

**Example usage:**

'''batch
python -m pdf_freeze --i original.pdf --o freezed.pdf
'''

!!! important
    See notes in the script. 
