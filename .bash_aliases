#!/bin/bash

# apt-get 
alias update='sudo apt-get update -y'
alias upgrade='sudo apt-get upgrade -y'
alias install='sudo apt-get install -y'

# zip
alias targz='tar -zcvf'
alias untar='tar -xzf'

# gnome
alias gopen='gnome-open'


# shell
alias listalias='cat ~/.bash_aliases'

# scripts
export PATH=$PATH:/opt/bin

# uio
alias sshuio='ssh -YC anderjaa@login.ifi.uio.no'
alias uiofiler='sshfs anderjaa@login.ifi.uio.no: ~/Documents/uio-home -o reconnect,modules=iconv,from_code=utf8'
