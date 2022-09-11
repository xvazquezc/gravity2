#!/bin/bash

# mcl installation
apt-get install mcl -y

# hmmer installation
apt-get install hmmer -y

# blast installation. Assumes Linux x64 build!
apt install ncbi-blast+

# hhsuite installation
mkdir -p ~/programs/hh-suite && cd ~/programs/hh-suite
git clone https://github.com/soedinglab/hh-suite.git .
mkdir build && cd build
cmake ..
make
export HHLIB="~/programs/hh-suite"
export PATH="$PATH:$HHLIB/bin:$HHLIB/scripts"

# muscle installation. Assumes Linux x64 build!
mkdir -p ~/programs/muscle && cd ~/programs/muscle
wget https://github.com/rcedgar/muscle/releases/download/v5.1/muscle5.1.linux_intel64
mv muscle5.1.linux_intel64 muscle
chmod 777 muscle

# booster installation
cd ~/workspace
wget https://github.com/evolbioinfo/booster/releases/download/v0.1.2/booster_linux64
