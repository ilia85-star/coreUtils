#!/usr/bin/env bash

case $1 in
	mv) mv "$2" "$3" | pv "$2" || printf '\e[A\e[K';;
	cp) cp "$2" "$3" | pv "$2" ;;
	*) echo "I didn't get it. :(";;
esac

