#!/bin/bash
tail -n 2500 "$1" > "$1".tmp
mv "$1".tmp "$1"
