import requests
import time
from .models import *
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger('ResourceLocator')
scheduler = BackgroundScheduler()

def get_ldm_status():
    for instance in Instance.objects.all():
        logger.info("pinging domain " + instance.VERSION)
        instance.LDM_Status = False
        print(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+"/ldmadmin")
        try:
            r = requests.get(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+"/ldmadmin",verify=False,timeout=20)
            print(r)
            instance.LDM_Status = True
        except Exception as e:
            logger.info(e)
        finally:
            instance.save()


def get_resource_list():
    RefreshCount = Search_count.objects.get(id=21)
    refreshCount = RefreshCount.search_count + 1
    RefreshCount.search_count = RefreshCount.search_count + 1
    RefreshCount.save()
    for instance in Instance.objects.all():
        print(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+"/ldmadmin")
        logger.info("started getting resource list from " + instance.VERSION)
        try:
            r = requests.get(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+os.getenv('GET_RESOURCES_API'), auth=(instance.SECURITY_DOMAIN+"\\"+instance.USERNAME,instance.PASSWORD), verify=False,timeout = 20)
            resource_list = r.json()
            for resource in resource_list:
                logger.info("getting resource " + resource['resourceName'])
                createdTime = time.strftime('%Y-%m-%d', time.localtime(resource['createdTime']/1000))
                modifiedTime = time.strftime('%Y-%m-%d', time.localtime(resource['modifiedTime']/1000))
                print(modifiedTime)
                if len(Resource_Type.objects.filter(resource_type=resource['resourceTypeName'])) == 0 :
                    res_type = Resource_Type(resource_type=resource['resourceTypeName'],provider_id='dummy',MITI_Scanner='False')
                    res_type.save()
                r = requests.get(instance.HOST_NAME+":"+str(instance.CATALOG_PORT)+os.getenv('GET_RESOURCES_API')+resource['resourceName'], auth=(instance.SECURITY_DOMAIN+"\\"+instance.USERNAME,instance.PASSWORD), verify=False,timeout=20)
                configuration_temp = r.json()
                str_temp = ""
                for i in configuration_temp["scannerConfigurations"]:
                    if i["enabled"] == True:
                        str_temp = str_temp + i['scanner']['providerTypeName'] +', '
                str_temp = str_temp[:-2]
                print(Resource.objects.filter(ins=instance,Resource_Name=resource['resourceName']).count())
                if Resource.objects.filter(ins=instance,Resource_Name=resource['resourceName']).count() == 0:
                        res = Resource(Resource_Name=resource['resourceName'],Owner=resource['createdBy'],Config=str_temp,Resource_Type=Resource_Type.objects.filter(resource_type=resource['resourceTypeName'])[0],ins=instance,createdTime=createdTime,modifiedTime=modifiedTime,MarkForDeletion=False,Refresh_Number=refreshCount)
                        res.save()
                else:
                    res_db = Resource.objects.filter(ins=instance,Resource_Name=resource['resourceName'])[0]
                    print(res_db.Config)
                    if res_db.Owner != resource['createdBy'] or res_db.Config != str_temp or res_db.Resource_Type != Resource_Type.objects.filter(resource_type=resource['resourceTypeName'])[0] or res_db.createdTime != createdTime or res_db.modifiedTime != modifiedTime:
                        print("inside change")
                        res_db.Owner = resource['createdBy']
                        res_db.Config = str_temp
                        res_db.Resource_Type = Resource_Type.objects.filter(resource_type=resource['resourceTypeName'])[0]
                        res_db.createdTime = createdTime
                        res_db.modifiedTime = modifiedTime
                    res_db.Refresh_Number = refreshCount
                    res_db.save()
                    print("resource saved ----------\n")
            Resource.objects.filter(ins=instance,Refresh_Number__lte=refreshCount-1).delete()

               
        except Exception as e:
            logger.info(e)
            continue



def start_schedular():
    scheduler.add_job(get_ldm_status, 'interval', minutes=1)
    scheduler.add_job(get_resource_list, 'interval', minutes=30)
    scheduler.start()