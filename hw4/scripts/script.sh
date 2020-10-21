#!/bin/bash

method=GET
limit=10
separator=' '
path=/dev/stdin

usage() {
# heredoc
cat << EOF
Aggregate NGINX logs
Usage: $0 [FILE]
OPTIONS
  -t TASK
      Choose task number. Available values are 1 to 5
  -c CODE
      Filter output by code
      Examples:
            -c 4     filter all requests with client errors
            -c 403   filter all requests with 404 error
  -m METHOD
      Filter output by method. Default values is GET
  -l NUMBER
      Set limit for output. Default value is 10
  -s SEPARATOR
      Set separator for output. Default value is space
  -h
      Show this help and exit 
EOF
}


while getopts :t:p:m:l:s:c:h opt; do
	case $opt in
		t) task=$OPTARG;;
		p) path=$OPTARG;;
		m) method=$OPTARG;;
		l) limit=$OPTARG;;
		s) separator=$OPTARG;;
	esac;
done

format() {
if [ -z $1 ]; then d=' '; else d=$1; fi

printf_format="%s$d%s$d%s$d%s$d%s"
awk -F'|' "{printf \"$printf_format"'\n", $1, $2, $3, $4, $5}' 
}

case $task in
	1) wc -l < $path;;
	2) ./parse.sh < $path | grep -e ".*|$method|" | wc -l;;
	3) ./parse.sh < $path | sort -t'|' -k5 -rn | head -n $limit | format $separator;;
	4) ./parse.sh < $path | sed -e '/^.*|.*|.*|4..|/p' -n | awk -F'|' '{location[$0] = $3; count[$3]++} END {for(line in location) { printf "%s|%s\n", line, count[location[line]]}}' | sort -t'|' -k7 -rn | head -n $limit | format $separator;;
	5) ./parse.sh < $path | sed -e '/^.*|.*|.*|5..|/p' -n | sort -t'|' -k5 -rn | head -n $limit  | format $separator;;
esac
