import requests
import math
import logging
import os
import json
from django.conf import settings


logger = logging.getLogger('django')


class ApiWrapper:

    def __init__(self):
        self.api_key = settings.USDA_API_KEY
        self.base_url = settings.USDA_BASE_URL
        self.resp_format = settings.USDA_RESPONSE_FORMAT
        self.activity_file = settings.ACTIVITY_JSON
        self.activity_group_file = settings.ACTIVITY_GROUP_JSON
        logger.debug("API Wrapper object initializing with" +
                        "\n\tAPI Key: " +
                        self.api_key +
                        "\n\tBase URL: " +
                        self.base_url +
                        "\n\tFormat: " +
                        self.resp_format
                    )
        logger.info("API Wrapper ready...")


    def forgeUrl(self, operation):
        url_mask = '{}/{}/?format={}&api_key={}'
        forged_url = url_mask.format(self.base_url,
                                     operation, 
                                     self.resp_format, 
                                     self.api_key)
        logger.debug("API Forged URL: " + forged_url)
        return forged_url
    
#    def forgeUrl(self, operation, max_results, offset):
#        url_mask = '{}/{}/?format={}&api_key={}&max={}&offset={}'
#        forged_url = url_mask.format(self.base_url, 
#                                     operation, 
#                                     self.format, 
#                                     self.api_key, 
#                                     max_results, 
#                                     offset)
#        return forged_url
    
    def requestJson(self, url):
        response_json = requests.get(url).json()
        return response_json
    
    def searchFood(self, search_item):
        logger.info("Querying food...")
        operation = 'search'
        data_source = 'Standard Reference'
        
        search_url = self.forgeUrl(operation) + '&q={}'.format(search_item) + '&ds={}'.format(data_source)
        
        logger.info("API Query URL: " + search_url)
        
        response = self.requestJson(search_url)
        try:
            response_list = response["list"]["item"]
        except KeyError:
            response_list = []
        logger.debug("\nQuery results:\n")
        
        for item in response_list:
            print(item["name"])
            logger.debug(item["name"])
        
        return response_list
        
    def getFoodReport(self, food_ndbno):
        ndbno = food_ndbno
        logger.info("Querying food details for" + str(ndbno) + "...")
        operation = 'reports'
        report_type = 'f'
        
        report_url = self.forgeUrl(operation) + '&ndbno={}'.format(ndbno) + '&type={}'.format(report_type)
        
        logger.info("API Query URL: " + report_url)
        
        report = self.requestJson(report_url)
        
        try:
            report_list = report["report"]["food"]
        except KeyError:
            report_list = []
            
        logger.debug("\nQuery results:\n")
        
        for item in report_list["nutrients"]:
            print(str(item["name"]) + " : " + str(item["value"]) + str(item["unit"]))
            logger.debug(str(item["name"]) + " : " + str(item["value"]) + str(item["unit"]))
            
        return report_list
        
    def getActivities(self):
        activity_file = self.activity_file
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, activity_file)
        with open(file_path) as json_data:
            d = json.load(json_data)
            return d
        
    def getActivityGroups(self):
        activity_group_file = self.activity_group_file
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, activity_group_file)
        with open(file_path) as json_data:
            d = json.load(json_data)
            return d
        
        
class UserUtils:
    
    # Initialize with a 'user' to play with its data.
    def __init__(self, user):
        logger.info("User utilities initialized for " + user.username + ".")
        self.user = user
        
    def getBmi(self):
        height = self.user.userprofile.height
        weight = self.user.userprofile.weight
        # BMI = weight(kg) / height(m)^2
        bmi = round(weight/pow(height/100,2),2)
        
        logger.debug("User " + self.user.username + 
                        "\n\tHeight: " + str(height) + 
                        "\n\tWeight: " + str(weight) +
                        "\n\tBMI: " + str(bmi)
                    )
        
        return bmi
        
