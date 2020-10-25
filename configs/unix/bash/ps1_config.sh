parse_git_branch() {
git branch 2> /dev/null 2>&1 | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

PS1='\[\033[01;32m\][\T]\[\033[01;31m\]{\u}\[\033[01;33m\]$(parse_git_branch)\[\033[01;34m\]\w\[\033[00m\]$'
