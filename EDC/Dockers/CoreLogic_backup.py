from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from .models import dockers, user
import logging
import requests

logger = logging.getLogger('Docker')


scheduler = BackgroundScheduler()

def get_docker_list():
    logger.info("Docker Update started")
    dockers.objects.all().delete()
    myfile = open("/home/EDC_Resource_Locator/static/Docker_list.txt", "r")
    for line in myfile:
        version = "unknown"
        try:
            if len(line.rstrip().split(",")[4]) == 0:
                if len(line.rstrip().split(",")[3]) == 0 and len(line.rstrip().split(",")[2]) != 0:
                    version = line.rstrip().split(",")[2].split("=")[1][1:-1]
                elif len(line.rstrip().split(",")[3]) != 0:
                    version = line.rstrip().split(",")[3].split("=")[1][1:-1]
            else:
                version = line.rstrip().split(",")[4].split("=")[1][1:-1]
            docker = dockers(CaseNo=line.rstrip().split(",")[0].split(".")[0][line.rstrip().split(",")[0].split(".")[0].index("0"):],Host=line.rstrip().split(",")[1][:-1],Version=version,expiryDate=' ',pVersion=' ',createdDate=' ',region=' ',status=False,email='Unknown@informatica.com')
            docker.save()

        except Exception as e:
            print(e)
            continue
    logger.info("Docker Update Completed")
    getdockerlist()
    

def refresh_docker_list():
    logger.info("Docker Script Execution Started")
    subprocess.call(['sh','/home/EDC_Resource_Locator/static/docker.sh'])
    logger.info("Docker Script Execution Completed")
    get_docker_list()

def start_schedular():
    scheduler.add_job(refresh_docker_list, 'interval', minutes=15)
    scheduler.start()
    logger.info("docker refresh job scheduled")
    
def getdockerlist():
    logger.info("Docker API started")
    url = 'http://iservernext/labconsole/api/v1/getdockers'
    users = user.objects.all()
    for userid in users:
        print("getting dockers for user {}".format( userid.email.split('@')[0]))
        username = userid.email.split('@')[0]
        r = requests.post(url, json={'email': username })
        dockers_list = r.json()
        for docker in dockers_list['data']:
            if dockers.objects.filter(CaseNo=docker['CASENUM']).count() != 0:
                d = dockers.objects.get(CaseNo=docker['CASENUM'])
                if docker['EXPIRY_DATE'] != None:
                    d.expiryDate = docker['EXPIRY_DATE'].split('T')[0]
                else:
                    d.expiryDate =  'Not Marked'
                d.pVersion = docker['PVERSION'] if docker['PVERSION'] != None else 'unknown'
                d.createdDate = docker['CREATION_DATE'].split('T')[0]
                d.region = docker['REGION']
                if docker['STATUS'] == 'UP':
                    d.status = 1
                else:
                    d.status = 0
                d.email = docker['EMAIL']
                d.Visibilty = True
                d.Note = ""
                d.save()
            else:
                d = dockers(CaseNo=docker['CASENUM'],Host=docker['CONTAINER_ID'] if docker['CONTAINER_ID'] != None else 'unknown',Version='unknown',expiryDate=docker['EXPIRY_DATE'].split('T')[0] if docker['EXPIRY_DATE'] != None else 'Not marked',pVersion=docker['PVERSION'] if docker['PVERSION'] != None else 'unknown',createdDate=docker['CREATION_DATE'].split('T')[0],region=docker['REGION'],status=False if docker['STATUS'] != 'UP' else True,email=docker['EMAIL'],Visibility = True, Note = "")
                d.save()
                
    logger.info("Docker API Completed")