#!/bin/bash
#
# chkconfig: 2345 80 30 
# description: 
#
RETVAL=0
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin

start () {
  exec sudo -u pi nohup /home/pi/PiTracking/submit.sh </dev/null >/dev/null 2>&1 &
}

stop () {
  echo "not implemented" > /dev/null
  RETVAL=$?
}
case "$1" in
  start)
    start
    RETVAL=$?
    ;;
  stop)
    stop
    RETVAL=$?
    ;;
  restart)
    start
    RETVAL=$?
    ;;
  *)
    start
    RETVAL=$?
    ;;
esac
exit $RETVAL

