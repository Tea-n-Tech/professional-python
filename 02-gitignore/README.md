
# 🗑️ Gitignore

A python project creates many files we don't want to commit
to our codebase.
An example is the built package within the `dist` folder from
the previous step.
To avoid this, use a `.gitignore` file.
Simply add it to your project root and add the files or folders
which you want to ignore.
As we are lazy we take a recommended `.gitignore` from GitHub
and use it:

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
...
```

I shortened the list to make it more readable here so check out
the file for more.

These files will not show up during `git status` and you cannot
accidentally commit them.
Great!
No more users commiting and pushing autogenerated files with 20k
lines of code 🥳