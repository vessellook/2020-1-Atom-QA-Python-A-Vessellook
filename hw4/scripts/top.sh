#!/bin/bash

usage() {
# heredoc
cat << EOF
Aggregate NGINX logs
Usage: $0 [FILE]
OPTIONS
  -p PATH
      Set path to logs. This script uses /dev/stdin by default
  -o OUTPUT
      Set file for output. This script uses /dev/stdout by default
  -c CODE
      Filter output by status code
      Examples:
            -c 4     filter all requests with client errors
            -c 403   filter all requests with 403 error
  -m METHOD
      Filter output by HTTP method
  -s SORT_BY
      Set sorting. Available values are
        SIZE
            Sort lines by response message size. The heaviest response is the first
        LOCATION
            Sort lines by frequency of location. Lines with the most frequent location are at the top
  -l LIMIT
      Set maximal count of lines in output
  -f FILLER
      Set filler for output. Default value is space
  -h
      Show this help and exit 
EOF
}


format() {
	if [ -z $1 ]; then d=' '; else d=$1; fi
	printf_format="%s$d%s$d%s$d%s$d%s"
	awk -F'|' "{printf \"$printf_format"'\n", $1, $2, $3, $4, $5}' 
}

limit=10
filler=' '
path=/dev/stdin
output=/dev/stdout

while getopts :s:p:o:m:c:l:f:h opt; do
	case $opt in
		s) order=$OPTARG;;
		p) path=$OPTARG;;
		o) output=$OPTARG;;
		m) method=$OPTARG;;
		c) code=$OPTARG;;
		l) limit=$OPTARG;;
		f) filler=$OPTARG;;
		h) usage && exit 1;;
		?) echo Invalid option $opt. Use -h to see help info;;
	esac;
done

./parse.sh < $path |
if [ -z $code   ]; then cat; else ./filter.sh -c $code  ; fi |
if [ -z $method ]; then cat; else ./filter.sh -m $method; fi |
if [[ ! -z $order && $order = LOCATION ]]
  then
    awk -F'|' '{location[$0] = $3; count[$3]++} '`
         `'END {for(line in location)'`
               `'{ printf "%s|%s\n", line, count[location[line]]}'`
	     `'}' |
    sort -t'|' -k7 -rn;
elif [[ ! -z $order && $order = SIZE  ]]
  then
    sort -t'|' -k5 -rn;
else cat;
fi |
if [ -z $limit ]; then cat; else head -n $limit | format $filler > $output

