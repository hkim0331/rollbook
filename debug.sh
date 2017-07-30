#!/bin/sh
if [ $# -ne 1 ]; then
    echo "usage $0 [on|off]"
    exit;
fi
if [ $1 = "on" ]; then
    sed -i.bak "s/DEBUG *= *false/DEBUG = true/" common.rb
    sed -i.bak "s/debug\* *#false/debug* #true/" common.rkt
else
    sed -i.bak "s/DEBUG *= *true/DEBUG = false/" common.rb
    sed -i.bak "s/debug\* *#true/debug* #false/" common.rkt
fi
