#!/bin/bash

cp lib/ta-lib-0.4.0-src.tar.gz /tmp/ta-lib-0.4.0-src.tar.gz

cd /tmp

tar -xvzf ta-lib-0.4.0-src.tar.gz

cd ta-lib/

./configure --prefix=/usr

make

sudo make install

echo "/usr/local/lib" >> sudo /etc/ld.so.conf
sudo ldconfig