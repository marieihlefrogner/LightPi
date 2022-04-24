import datetime, time, os, sys

if len(sys.argv) == 1:
    alarm_time = datetime.datetime.strptime(sys.argv[0][2:], "%d/%m/%Y %H:%M")
    if not alarm_time:
        exit("wrong input")

    while True:
        if datetime.now() >= alarm_time:
            if sys.argv[0][0] == '0':
                os.system("~/wiringPi/off")
            else:
                os.system("~/wiringPi/on")

            break
        else:
            time.sleep(1)

