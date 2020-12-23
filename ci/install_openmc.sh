#!/bin/bash

set -ex

mkdir ~/openmc
cd ~/openmc

git clone https://github.com/openmc-dev/openmc -b v0.12.0

cd openmc
mkdir build
cd build

cmake .. -DCMAKE_INSTALL_PREFIX=~/openmc

make all install

cd ..
pip install .
