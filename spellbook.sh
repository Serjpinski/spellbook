#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

alias spellreload='source ${DIR}/book.alias'

function spell () {
        python3 ${DIR}/spellbook.py "$@"
        if [[ $? -eq 0 ]]; then
                [[ $# = 2 ]] && [[ $1 = "remove" ]] && unset -f $2
                spellreload
        fi
}

spellreload