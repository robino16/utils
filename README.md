# Utilities

## Progress Bar (Python)

A simple progress bar class for Python applications.

    Progress: |█████████████████       | 80/100 (80%) ETA: 2s

**Example:**

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
