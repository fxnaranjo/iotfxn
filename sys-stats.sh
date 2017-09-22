#!/bin/bash
# Generates a JSON output with some system load statistics
# Taken from: https://unix.stackexchange.com/questions/63320/bandwidth-cpu-memory-stats-returned-in-single-line-from-terminal
# Thanks to livingstaccato (https://unix.stackexchange.com/users/31025/livingstaccato)
{ printf '%s' '{"load":["'$(cut -d' ' --output-delimiter='","' -f-3 /proc/loadavg); printf '%s' '"],"net":{'; tail -n+3 /proc/net/dev|awk -F' ' '{ gsub(/:/,""); printf "\"%s\":{\"rxbytes\":\"%s\",\"rxpackets\":\"%s\",\"rxerrs\":\"%s\",\"rxdrop\":\"%s\",\"txbytes\":\"%s\",\"txpackets\":\"%s\",\"txerrs\":\"%s\",\"txdrop\":\"%s\"},",$1,$2,$3,$4,$5,$10,$11,$12,$13 }'|sed 's/,$//'; printf '%s' '},"mem":{'; grep -E '^(MemTotal|MemFree|SwapTotal|SwapFree):' /proc/meminfo|tr 'A-Z' 'a-z'|awk -F' ' '{gsub(/:/,""); printf "\"%s\":\"%s\",",$1,$2}'|sed 's/,$//'; printf '%s' '}}'; }

