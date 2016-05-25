#!/bin/bash
cd /opt/seafile/seafile-pro-server-4.3.3/
./seahub.sh stop
./seafile.sh stop

wait
cd /opt/seafile/seafile-pro-server-4.3.3/upgrade/
source ./migrate_seafile_data_3.0.sh
wait

cd /opt/seafile/seafile-pro-server-4.3.3/
./seafile.sh start
./seahub.sh start

cd /home/zdvadmin/sf-checker/Url_Checker_Main
#/bin/bash
python main.py
