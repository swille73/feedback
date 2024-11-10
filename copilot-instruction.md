# Copilot Instruction Guide

## Coding Standards
- Use Python as the primary language.
- Use descriptive variable and function names.
- Follow PEP 8 guidelines for Python code.
- Include docstrings for all functions and classes.
- Include toplevel docstring for the script.
- Use Pylint as the the primary linter.

## Project-Specific Guidelines
- Database interactions should be handled using SQLAlchemy.
- Use the `logging` module for logging instead of print.
- Or use the `Rich` module for logging like `rich.console` instead of print.
- Use the `pandas` module for data analysis.
- Use the `matplotlib` module for data plotting
- put code in logically split functions if possible.
- Every new Script should have a entrypoint like `__name__ == '__main__'`