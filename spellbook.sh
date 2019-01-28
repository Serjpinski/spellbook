#!/bin/bash

BASE_DIR=$1

alias spellreload='source ${BASE_DIR}/book.alias'

function spell () {

    python3 ${BASE_DIR}/spell.py "$@"

    if [[ $? -eq 0 ]]; then
        [[ $# = 2 ]] && [[ $1 = "remove" ]] && unset -f $2
        spellreload
    fi
}

spellreload
