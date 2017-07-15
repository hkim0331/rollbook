#!/bin/sh
if [ $# -ne 1 ]; then
  echo usage: $0 VERSION
  exit
else
  VERSION=$1
fi

# linux's sed is gnu sed, macos not.
if [ -e /usr/local/bin/gsed ]; then
    SED=/usr/local/bin/gsed
else
    SED=`which sed`
fi
if [ -z ${SED} ]; then
    echo can not find SED
    exit
fi

${SED} -E -i.bak "s/\(define version \"[0-9.]+\"\)/(define version \"${VERSION}\")/" attend.rkt
${SED} -E -i.bak "s/VERSION = \"[0-9.]+\"/VERSION = \"${VERSION}\"/" attends.cgi
