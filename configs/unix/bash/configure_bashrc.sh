#!/bin/bash

# Configure bash terminal cmd line format
BASHFILE=~/.bashrc

# cat ps1_config.sh >> $BASHFILE
cat aliases_config.sh >> $BASHFILE
cat history_config.sh >> $BASHFILE
