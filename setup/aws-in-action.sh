#!/usr/bin/env bash
set -x
mkdir -p examples/AWSinAction/flat
cd examples/AWSinAction
git clone https://github.com/AWSinAction/code2.git
find . -name *.yaml -print > cloudformation.txt
find . -name *.yaml -print | sed -e 's/^./python ..\/..\/..\/cloudformation\/NodeLoader.py ./' > flatten.sh
chmod +x flatten.sh
./flatten.sh
ls -l flat
cd ../..
ls -l examples
