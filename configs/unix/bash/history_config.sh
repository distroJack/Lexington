
# Prevent duplicate commands from being logged
export HISTCONTROL=ignoredups

# Save multiline commands as a single line in history
shopt -s cmdhist

# Append instead of overwrite to history
shopt -s histappend

# Append when prompt is shown not when 
PROMPT_COMMAND='history -a'
