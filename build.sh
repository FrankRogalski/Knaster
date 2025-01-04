#!/bin/bash
set -xe
cc -O3 -shared -fPIC -o knaster.so knaster.c
