# spellbook
Shell alias manager

# Usage

Add to shell config file:
```sh
##### SPELLBOOK CONF #####
alias spellreload='source {spellbook_path}/book.alias'

function spell () {
        python3 {spellbook_path}/spellbook.py "$@"
        if [ $? -eq 0 ]; then
                [ $# = 2 ] && [ $1 = "remove" ] && unset -f $2
                spellreload
        fi
}

spellreload
##########################
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
