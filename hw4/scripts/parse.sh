#!/bin/bash
parse() { 
# logs format: 
# $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"

# brackets mean number of group in regex 
regex='^(([0-9]{1,3}[.]){3}[0-9]{1,3}) - '` # ip address (1)
     `'.* \[.*\] "(.*) (.*) HTTP\/.*" '`     # method (3), location (4)
     `'([0-9]{3}) ([0-9]+)'                  # status code (5), response body size (6)
   

replacement='\1|\3|\4|\5|\6|'       # format for awk 

sed -E "s/$regex/$replacement/p" -n 
}

parse
