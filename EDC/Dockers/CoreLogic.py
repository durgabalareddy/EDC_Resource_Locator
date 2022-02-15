from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from .models import dockers, user
import logging
import requests
from ResourceLocator.models import *
from dotenv import load_dotenv
import os

load_dotenv()

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
    scheduler.add_job(getdockerlist, 'interval', minutes=15)
    scheduler.start()
    logger.info("docker refresh job scheduled")



def getDockerVersion():
    logger.info("Getting Dockers Versions")
    Dockers = dockers.objects.all()
    for docker in Dockers:
        logger.info("Getting Version of Docker {}".format(docker.Host))
        try:
            ssh = subprocess.check_output(['sh','/home/EDC_BALA/EDC/docker.sh',docker.Host])
            versionList = ssh.decode('utf8').split('"')
            if len(versionList) == 7:
                version = versionList[5]
            elif len(versionList) == 5:
                version = versionList[3]
            elif len(versionList) == 1:
                version = 'unknown'
            else:
                version = versionList[1]
            
            if version != 'unknown':
                d = dockers.objects.get(Host=docker.Host)
                d.Version = version
                logger.info(version)
                d.save()
        except Exception as e:
            logger.info(e)
            continue
    logger.info("Done Getting Dockers Versions")


def getdockerlist():
    RefreshCount = Search_count.objects.get(id=22)
    refreshCount = RefreshCount.search_count + 1
    RefreshCount.search_count = RefreshCount.search_count + 1
    RefreshCount.save()
    logger.info("Docker API started")
    url = os.getenv('DOCKER_API')
    users = user.objects.all()
    for userid in users:
        logger.info("getting dockers for user {}".format( userid.email.split('@')[0]))
        username = userid.email.split('@')[0]
        r = requests.post(url, json={'email': username })
        dockers_list = r.json()
        try:
            for docker in dockers_list['data']:
                logger.info("Getting docker {}".format(docker['CONTAINER_ID']))
                logger.info("-------------------------------------------------------------------")
                if dockers.objects.filter(Host=docker['CONTAINER_ID']).count() != 0:
                    logger.info("Docker with Host {} already exists in the DB".format(docker['CONTAINER_ID']))
                    logger.info("-------------------------------------------------------------------")
                    d = dockers.objects.get(Host=docker['CONTAINER_ID'])
                    logger.info("-------- Docker Details from DB ---------")
                    logger.info("Host : {}".format(d.Host))
                    logger.info("CaseNo : {}".format(d.CaseNo))
                    logger.info("expiryDate : {}".format(d.expiryDate))
                    logger.info("pVersion : {}".format(d.pVersion))
                    logger.info("createdDate : {}".format(d.createdDate))
                    logger.info("region : {}".format(d.region))
                    logger.info("email : {}".format(d.email))
                    logger.info("Version : {}".format(d.Version))
                    logger.info("Note : {}".format(d.Note))
                    logger.info("Visibilty : {}".format(d.Visibilty))
                    logger.info("refreshNumber : {}".format(d.refreshNumber))
                    logger.info("-------------------------------------------------------------------")
                    logger.info("-------- Docker Details from API ---------")
                    logger.info("Host : {}".format(docker['CONTAINER_ID']))
                    logger.info("CaseNo : {}".format(docker['CASENUM']))
                    logger.info("expiryDate : {}".format(docker['EXPIRY_DATE']))
                    logger.info("pVersion : {}".format(docker['PVERSION']))
                    logger.info("createdDate : {}".format(docker['CREATION_DATE']))
                    logger.info("region : {}".format(docker['REGION']))
                    logger.info("email : {}".format(docker['EMAIL']))
                    logger.info("Version : {}".format(d.Version))
                    logger.info("Note : {}".format(d.Note))
                    logger.info("Visibilty : {}".format(d.Visibilty))
                    logger.info("refreshNumber : {}".format(d.refreshNumber))
                    logger.info("-------------------------------------------------------------------")
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
                    if d.CaseNo != docker['CASENUM']:
                        d.CaseNo = docker['CASENUM']
                        d.Visibilty = True
                        d.Note = ""
                    d.Visibilty = d.Visibilty
                    d.Note = d.Note
                    d.refreshNumber = refreshCount
                    logger.info("---------------------crossed refresh Number----------------")
                    d.save()
                else:
                    logger.info("--------------creating docker {}-----------------------------------------------------".format(docker['CASENUM']))
                    d = dockers(CaseNo=docker['CASENUM'],Host=docker['CONTAINER_ID'] if docker['CONTAINER_ID'] != None else 'unknown',Version='unknown',expiryDate=docker['EXPIRY_DATE'].split('T')[0] if docker['EXPIRY_DATE'] != None else 'Not marked',pVersion=docker['PVERSION'] if docker['PVERSION'] != None else 'unknown',createdDate=docker['CREATION_DATE'].split('T')[0],region=docker['REGION'],status=False if docker['STATUS'] != 'UP' else True,email=docker['EMAIL'],Visibilty = True, Note = "",refreshNumber = refreshCount)
                    d.save()
            logger.info("-------------- refresh count {}-----------------------------------------------------".format(refreshCount))
        except Exception as e:
            logger.info(e)
            continue
    logger.info("-------------- Deleting the dockers less than the refresh count {}-----------------------------------------------------".format(refreshCount))
    dockers.objects.filter(refreshNumber__lte=refreshCount-1).delete()
    logger.info("Docker API Completed")
    getDockerVersion()