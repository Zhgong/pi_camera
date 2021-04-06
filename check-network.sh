#!/bin/bash
FILE=$(basename "$0") # get base name from absolute path
LOGFILE=/var/log/$FILE.log
exec 1>>"${LOGFILE}"
exec 2>&1

echo -------------------------------------------------------------------------------
echo +             [$(date)] start Script to check netork connection               +
echo -------------------------------------------------------------------------------
echo $(timedatectl)

network_status=0
network_status_old=0
count=0
retry=0
send_mode=0 # 0: send once (after bootup), 1: in loop

function send_message() {
	source "$(dirname $0)/.env-bash" # use this file to transfer enviroment variables otherwise it will not work if this script was called by system

	curl -X POST -H "Content-Type: application/json" -u "${MESSAGE_TOKEN}:" -d "{\"message\":\"[Mailbox] [$1]\"}" -k https://${SERVER_IP}:${PORT}/api/v1/send
}

while true; do
	ping -c 2 8.8.8.8 >/dev/null
	result=$?
	if [ ${result} -eq 0 ]; then
		network_status=1
	else
		network_status=0

	fi

	if [ ${network_status} -eq 1 ] && [ ${network_status_old} -eq 0 ]; then
		echo ["$(date)"] [Network OK]
		if [ ${count} -eq 0 ]; then
			name=$(hostname)
			current_date=$(date)
			ip=$(hostname -I | cut -d' ' -f1)
			send_message "[${current_date}][${name} Network ok. http://${ip}:8080] "
			result=$?
			if [ ${result} -eq 0 ]; then
				retry=0
			else
				retry=1

			fi
			echo $(timedatectl)
		elif [ ${send_mode} -eq 1 ]; then
			send_message "Network ok"
		elif [ ${retry} -eq 1 ]; then
			send_message "[${current_date}][${name} Network ok. http://${ip}:8080] "
			result=$?
			if [ ${result} -eq 0 ]; then
				retry=0
			else
				retry=1

			fi
		fi
		count=$((count + 1))
		echo Network reconnect count: ${count}

	elif [ ${network_status} -eq 0 ] && [ ${network_status_old} -eq 1 ]; then
		echo ["$(date)"] [Network is unconnected]
		echo $(timedatectl)
	fi

	# echo network_status: ${network_status}
	# echo network_status_old: ${network_status_old}

	network_status_old=${network_status}
	sleep 5

done
