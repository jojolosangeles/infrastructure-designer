#!/usr/bin/env bash
set -x
mkdir -p examples/AWSinAction/flat
mkdir -p examples/AWSinAction/graph
cd examples/AWSinAction
git clone https://github.com/AWSinAction/code2.git
find . -name *.yaml -print > cloudformation.txt
find . -name *.yaml -print | sed -e 's/^./python ..\/..\/..\/setup\/flatten.py ./' > flatten.sh
chmod +x flatten.sh
./flatten.sh
find . -name *.flat -print | sed -e 's/^./python ..\/..\/..\/cloudformation\/nodeloader.py ./' > graphdata.sh
chmod +x graphdata.sh
./graphdata.sh
ls -l flat
ls -l graph
cd ../..
