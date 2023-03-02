# Development
## Pre-requisities

Install antlr4
```
$ apt-get install antlr4
```

## Generate Interpreter

```bash
$ antlr4 -Dlanguage=Python3 LaTeX.g4 -visitor -o latex/
```

## View AST

Update the content of the variable `in` in the file [App.java](treeviewer/pyomoforge/src/main/java/pyomoforge/App.java).

```
cd treeviewer/pyomoforge
cp ../../LaTeX.g4 src/main/antlr4/pyomoforge/ && rm src/main/java/pyomoforge/LaTeX*; mvn clean antlr4:antlr4 compile exec:java -Dexec.mainClass="pyomoforge.App"
```
