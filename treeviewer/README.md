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

Update the content of the variable `in` in the file [App.java](treeviewer/tex2pyomo/src/main/java/tex2pyomo/App.java).

```
cd treeviewer/tex2pyomo
cp ../../LaTeX.g4 src/main/antlr4/tex2pyomo/ && rm src/main/java/tex2pyomo/LaTeX*; mvn clean antlr4:antlr4 compile exec:java -Dexec.mainClass="tex2pyomo.App"
```
