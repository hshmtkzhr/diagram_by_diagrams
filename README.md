# diagram_by_diagrams
[Diagrams](https://diagrams.mingrammer.com/) is the python library providing the functionality to draw diagram as a code. This is my practical code for drawing diagram with Diagrams.

## setup
Graphviz is depended by diagrams as executable command. So you have to install and add PATH env for this previously.
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