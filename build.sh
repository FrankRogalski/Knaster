#!/bin/bash
set -xe
cc -O3 -c knaster.c
cc -shared -o knaster.so knaster.o
rm knaster.o
