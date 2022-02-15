#!/usr/bin/bash
sudo systemctl stop EDC_Resource_Locator_gunicorn.service
if [ $? == 0 ] 
then
echo "Gunicorn stopped successfully"
sudo /data/users/dpadala/EDC_Resource_Locator/nginx/nginx -s stop
if [ $? == 0 ]
then
echo "Nginx stopped successfully"
fi
else
echo "Gunicorn stopping failed"
fi
