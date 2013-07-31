#!/usr/bin/env bash
### Ockle Python Environment Initializer
#
# Pushed on 5773 Av 24/2013 Jul 31
#
# All the different steps for creating the python environment needed by ockle in
# one convenient script.
#
# @author: E.S. Rosenberg <esr+ocklesource at mail.hebrew.edu>
###

usage() {
    cat <<EOF
usage: $0 [init|reinit] (optional: python-env-folder-name)

This script initializes/installs the python environment needed by ockle.
Done at: ~/${python-env-folder-name}/

EOF
}

if (( $# == 0 )); then
    usage
    exit 1
fi

if [ -z "$2" ]; then
    env_folder='python-ockle-env'
else
    env_folder=$1
fi

if [ ! -z "$1" ]; then
    case $1 in
	'reinit')
     	    rm -r ~/${env_folder}
	    ;;
	'init')
	    if [ -d ~/${env_folder} ]; then
		echo "Folder already exists!"
		exit 1
	    fi
	    ;;
	*)
	    usage
	    ;;
    esac
fi

python2.7 /usr/bin/virtualenv ~/${env_folder}

~/${env_folder}/bin/easy_install pyramid==1.2.7

mkdir ~/${env_folder}/downloads/
cd ~/${env_folder}/downloads/
svn checkout http://networkx.lanl.gov/svn/pygraphviz/trunk pygraphviz

~/${env_folder}/bin/easy_install waitress
~/${env_folder}/bin/easy_install WebError
~/${env_folder}/bin/easy_install pyramid-handlers
~/${env_folder}/bin/easy_install pyramid-beaker
~/${env_folder}/bin/easy_install pyramid_debugtoolbar
~/${env_folder}/bin/easy_install psycopg2
~/${env_folder}/bin/easy_install pycrypto
~/${env_folder}/bin/easy_install SQLAlchemy
~/${env_folder}/bin/easy_install lxml
~/${env_folder}/bin/easy_install paramiko
~/${env_folder}/bin/easy_install pysnmp

if [ -d /usr/lib/graphviz/ ]; then
    sed -i "s#^library_path=None#library_path='/usr/lib/graphviz/'#g" ~/${env_folder}/downloads/pygraphviz/setup.py
else
    echo "Graphviz library not found, please complete the last stages of this script manually."
    exit 1
fi

if [ -d /usr/include/graphviz/ ]; then
    sed -i "s#^include_path=None#include_path='/usr/include/graphviz/'#g" ~/${env_folder}/downloads/pygraphviz/setup.py
else
    echo "Graphviz include not found, please complete the last stages of this script manually."
    exit 1
fi

cd ~/${env_folder}/downloads/pygraphviz/
~/${env_folder}/bin/python setup.py install
