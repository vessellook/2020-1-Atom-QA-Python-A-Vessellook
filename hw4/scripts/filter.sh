#!/bin/bash

filter_code() {
code=$1
if [ -z $code   ]; then cat; else awk -F'|' '$4 ~ /^'$code'/    { print $0}'; fi
}

filter_method() {
method=$1
if [ -z $method ]; then cat; else awk -F'|' '$2 ~ /^'$method'$/ { print $0}';  fi
}

if [ $1 == '-c' ]; then filter_code   $2; fi
if [ $1 == '-m' ]; then filter_method $2; fi
