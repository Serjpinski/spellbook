# spellbook
Shell alias manager

# Usage

Add to shell config file:
```sh
source {spellbook_path}/spellbook.sh
```

After reloading your shell, you will be able to:
```sh
~$ spell add goto p1 -c "cd $HOME/projects/project1"
~$ spell list
goto >
goto p1 > cd $HOME/projects/project1
~$ goto p1
~/projects/project1$
```
