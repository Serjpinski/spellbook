#!/usr/bin/env bash

alias spellreload='source $PWD/book.alias'

function spell () {
        python3 $PWD/spellbook.py "$@"
        if [[ $? -eq 0 ]]; then
                [[ $# = 2 ]] && [[ $1 = "remove" ]] && unset -f $2
                spellreload
        fi
}

spellreload