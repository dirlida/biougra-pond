#!/bin/bash
cd ~/pond
echo "OTS $(date -u +%FT%TZ)"
ls -1 *.ots | wc -l
find . -maxdepth 1 -name "*.ots" -mmin +60 | head -10
