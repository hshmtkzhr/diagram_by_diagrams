# diagram_by_diagrams
[Diagrams](https://diagrams.mingrammer.com/) is the python library providing the functionality to draw diagram as a code. This is my practical code for drawing diagram with the Diagrams.

## setup
Graphviz is depended by diagrams as executable command. So you have to install and add PATH env previously.
```bash
# on mac we can install by homebrew.
brew install graphviz
# confirm "dot" is in command search path
which dot
```
If you've not installed poetry package manager for python and pyenv. 
```bash
poetry install
```
Before running, need to activate virtual-env
```bash
source ./.venv/bin/activate
```

## Diagrams

### Web Service No-Where
This diagrams is my first mockup for practice. It describe sample web service architecture.
<img src="./images/main_diagram.png" width="1024">
