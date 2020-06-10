export GOPATH=~/code/go

export PATH=$PATH:~/code/go/bin:./bin:./node_modules/.bin/:~/bin

eval "$(direnv hook zsh)"

# #Enable SSH Key on Yubikey Device
# killall gpg-agent
# echo "KILLED GPG"
# killall ssh-agent
# echo "KILLED SSH"
# eval $( gpg-agent --daemon --enable-ssh-support )
# echo "STARTED GPG"
# export GPG_TTY=$(tty)
# echo "HHHHH"

alias equipgo="cd $GOPATH/src/github.com/18F/e-QIP-prototype"
alias notify="afplay /System/Library/Sounds/Ping.aiff -v 2"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

export PATH="$HOME/.cargo/bin:$PATH"
