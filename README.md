# spellbook
Shell alias manager

# Usage

Add to shell config file:
```sh
alias spell='python3 {spellbook_path}/spellbook.py'
source {spellbook_path}/book.alias
```

After reloading your shell config, you will be able to:
```sh
~$ spell add goto p1 -c "cd $HOME/projects/project1"
~$ spell list
goto >
goto p1 > cd $HOME/projects/project1
~$ goto p1
~/projects/project1$
```
