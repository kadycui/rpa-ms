#! /bin/bash

PWD=$(dirname $0)
DCS_LOG="$PWD/operation.log"
cd $PWD
# env
if [ -f ops.env ];then
  source ops.env 
else
  echo "deploy env file non-existent"
  exit 1
fi

# show info
function showinfo(){
    # source .env
    echo "---------- gms $N deploy info ----------"
    echo "  ver: $V"
    echo "mysql: ${MYSQL_HOST}:${MYSQL_PORT}/$D"
    echo "  web: http://${PORT}:${P}1"
}

# operation log
function operation_log(){
    #source .env
    #[ ! -f ${DCS_LOG} ] && touch ${DCS_LOG}   # >> 在没有文件的时候会创建文件
    echo "[`date +"%F %T"`] `basename $0` $COM D=$D N=$N P=$P V=$V DB_HOST=${DB_HOST} DBUP=$DBUP" >> ${DCS_LOG}
}

# start  restart  ps  down
COM=${1:-start}
case $COM in
  "start")
    docker-compose up -d
    showinfo
    operation_log
    ;;
  "stop")
    docker-compose stop
    operation_log
    ;;
  "restart")
    docker-compose restart
    operation_log
    ;;
  "ps")
    docker-compose ps
    ;;
  "down")
    docker-compose down
    operation_log
    ;;
  "downv")
    docker-compose down -v
    operation_log
    ;;
  "config")
    docker-compose config
    ;;
  "showinfo")
    showinfo
    ;;
  *)
    echo "bash $0 [start|stop|down|downv|ps|restart|showinfo|config]"
    ;;
esac