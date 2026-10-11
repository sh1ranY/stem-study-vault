#!/bin/zsh
cd -- "$(dirname -- "$0")"
python3 start.py "$@"
if [[ $? -ne 0 ]]; then
  read -r 'reply?Press Return to close. / 按回车关闭。 '
fi
