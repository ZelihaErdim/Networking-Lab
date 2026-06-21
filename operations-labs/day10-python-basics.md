# Day 10 — Python Basics

## Learn
- variables
- if/else logic
- loops
- functions
- lists
- dictionaries

## Useful Example
```python
import subprocess

result = subprocess.run(["ping", "-c", "3", "8.8.8.8"], capture_output=True, text=True)
print(result.returncode)
print(result.stdout)
```

## Practice Tasks
- Write a script that checks whether a device responds to ping
- Store results in a dictionary
- Print a clean summary
