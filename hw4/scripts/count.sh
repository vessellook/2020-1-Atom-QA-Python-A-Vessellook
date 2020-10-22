#!/bin/bash

usage() {
# heredoc
cat << EOF
Count filtered lines in NGINX logs
Usage: $0 [FILE]
OPTIONS
  -p PATH
      Set path to logs. This script uses /dev/stdin by default
  -c CODE
      Filter output by status code
      Examples:
            -c 4     filter all requests with client errors
            -c 403   filter all requests with 403 error
  -m METHOD
      Filter output by HTTP method
  -h
      Show this help and exit 
EOF
}

path=/dev/stdin
output=/dev/stdout

while getopts :p:o:c:m:h opt; do
	case $opt in
		p) path=$OPTARG;;
		m) method=$OPTARG;;
		c) code=$OPTARG;;
		h) usage && exit 1;;
		?) echo Invalid option $opt. Use -h to see help info;;
	esac;
done

if [[ -z $method && -z $code ]]; then wc -l < $path; exit 0; fi

if [[ $(file $path ) = *dir* ]]
  then
    cat $(find $path -maxdepth 1 -type f -name *.log) | ./parse.sh
  else ./parse.sh < $path
fi |
if [ -z $code   ]; then cat; else ./filter.sh -c $code  ; fi |
if [ -z $method ]; then cat; else ./filter.sh -m $method; fi |
wc -l

