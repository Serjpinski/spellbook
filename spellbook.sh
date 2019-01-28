#!/bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

alias spellreload='source ${BASE_DIR}/book.alias'

function spell () {

    python3 ${BASE_DIR}/spell.py "$@"

    if [[ $? -eq 0 ]]; then
        [[ $# = 2 ]] && [[ $1 = "remove" ]] && unset -f $2
        spellreload
    fi
}

spellreload
