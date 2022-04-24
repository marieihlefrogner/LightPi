[ $# -lt 1 ] && echo Needs one parameter && exit
irsend SEND_START /home/pi/lircd.conf $1 && sleep 1 && irsend SEND_STOP /home/pi/lircd.conf $1

