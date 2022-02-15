import requests

from apscheduler.schedulers.background import BackgroundScheduler

from requests.structures import CaseInsensitiveDict

from ResourceLocator.models import *

import time

import logging

logger = logging.getLogger('Purge')

scheduler = BackgroundScheduler()


def deleteResource():
    instances = Instance.objects.order_by('VERSION')
    for instance in instances:
        if instance.LDM_Status == False:
            logger.info("{} Instance is down. so skipping the Delete activity".format(instance.VERSION))
        else:
            logger.info(" Started Deletion activity on {}".format(instance.VERSION))
            resources = Resource.objects.filter(ins=instance,MarkForDeletion=True)
            for resource in resources:
                logger.info("Started Deletion resource {}".format(resource.Resource_Name))
                try:
                    res = requests.delete(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+'/access/1/catalog/resources/'+resource.Resource_Name,auth=("GCS_ISC_DSG"+"\\"+resource.Owner,"infa@123"), verify=False)
                    if res.status_code == 200:
                        logger.info("Request for deleting resource {} submitted with job id {}".format(resource.Resource_Name,res.json()['jobId']))
                        
                except:
                    continue
                
def start_scheduler():
    scheduler.add_job(deleteResource, 'interval', minutes=2160)
    scheduler.start()
    logger.info("Delete Resources job scheduled")