#!/usr/bin/bash
sudo systemctl start EDC_Resource_Locator_gunicorn.service
if [ $? == 0 ] 
then
echo "Gunicorn started successfully"
sudo /data/users/dpadala/EDC_Resource_Locator/nginx/nginx
if [ $? == 0 ]
then
echo "Nginx started successfully"
fi
else
echo "Gunicorn starting failed"
fi
