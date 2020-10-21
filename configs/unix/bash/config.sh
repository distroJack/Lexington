#!/bin/bash

BASHFILE=~/.bashrc

TIME="\[\033[01;32m\][\T]"
USER="\[\033[01;31m\]{\u}"
BRANCH="\[\033[01;33m\]\$(parse_git_branch)"
PATH="\[\033[01;34m\]\W"
CLEAR="\[\033[00m\]"

PAYLOAD="PS1='${TIME}${USER}${BRANCH}${PATH}${CLEAR}\$'"

echo "parse_git_branch() {
	git branch 2> /dev/null 2>&1 | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
" >> $BASHFILE

echo $PAYLOAD >> $BASHFILE
