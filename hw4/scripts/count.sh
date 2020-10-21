#!/bin/bash

usage() {
# heredoc
cat << EOF
Aggregate NGINX logs
Usage: $0 [FILE]
OPTIONS
  -p PATH or -p DIRECTORY
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

if [[ -z $method && -z $code ]]; then wc -l < $path > $output; exit 0; fi

./parse.sh < $path | ./filter.sh -c $code | ./filter.sh -m $method | wc -l > $output
