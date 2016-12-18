import requests
import math
import logging
import os
import json
from django.conf import settings


# Intitalize the logger object.
logger = logging.getLogger('django')


# ApiWrapper class has methods to query and process the food and exercise 
# information from external API's or JSON formatted files.
class ApiWrapper:

    # Initialize using project settings in the settings.py
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


    # Create the baseline URL according to project settings.
    def forgeUrl(self, operation):
        
        url_mask = '{}/{}/?format={}&api_key={}'
        forged_url = url_mask.format(self.base_url,
                                     operation, 
                                     self.resp_format, 
                                     self.api_key)
        logger.debug("API Forged URL: " + forged_url)
        return forged_url
    
    
    # May be used to implement the offset property of the queries. 
    # Still needs to be implemented.
#    def forgeUrl(self, operation, max_results, offset):
#        url_mask = '{}/{}/?format={}&api_key={}&max={}&offset={}'
#        forged_url = url_mask.format(self.base_url, 
#                                     operation, 
#                                     self.format, 
#                                     self.api_key, 
#                                     max_results, 
#                                     offset)
#        return forged_url
    
    
    # Extracts the JSON from the response.
    def requestJson(self, url):
        
        response_json = requests.get(url).json()
        return response_json
    
    
    # This is the actual method to query the API for keywords.
    def searchFood(self, search_item):
        
        logger.info("Querying food...")
        operation = 'search'
        data_source = 'Standard Reference'
        search_url = self.forgeUrl(operation) + '&q={}'.format(search_item) + '&ds={}'.format(data_source)
        logger.info("API Query URL: " + 
                    search_url)
        response = self.requestJson(search_url)
        
        # If the response list is Null, convert it to an empty list.
        try:
            response_list = response["list"]["item"]
        except KeyError:
            response_list = []
            
        logger.debug("\nQuery results:\n")
        
        for item in response_list:
            print(item["name"])
            logger.debug(item["name"])
        
        return response_list


    # Query the API for nutrient information of the related ndbno.
    def getFoodReport(self, food_ndbno):
        
        ndbno = food_ndbno
        logger.info("Querying food details for" + str(ndbno) + "...")
        operation = 'reports'
        report_type = 'f'
        report_url = self.forgeUrl(operation) + '&ndbno={}'.format(ndbno) + '&type={}'.format(report_type)
        logger.info("API Query URL: " + report_url)
        report = self.requestJson(report_url)
        
        # If the response list is Null, convert it to an empty list.
        try:
            report_list = report["report"]["food"]
        except KeyError:
            report_list = []
            
        logger.debug("\nQuery results:\n")
        
        for item in report_list["nutrients"]:
            print(str(item["name"]) + 
                  " : " + 
                  str(item["value"]) + 
                  str(item["unit"]))
            logger.debug(str(item["name"]) + 
                         " : " + 
                         str(item["value"]) + 
                         str(item["unit"]))
            
        return report_list


    # Load the list of activities from a JSON file on the server.
    def getActivities(self, json_file):
        
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, json_file)
        with open(file_path) as json_data:
            d = json.load(json_data)
            return d


    # Load the list of activity groups from a JSON file on the server.
    def getActivityGroups(self):
        
        activity_group_file = self.activity_group_file
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, activity_group_file)
        with open(file_path) as json_data:
            d = json.load(json_data)
            return d


# UserUtils class has methods to manage backend operations related to the user.
class UserUtils:
    
    # Initialize with a 'user' to play with its data.
    def __init__(self, user):
        logger.info("User utilities initialized for " + 
                    user.username + 
                    ".")
        self.user = user
    
    
    # Calculate and return the current user's BMI.
    def getBmi(self):
        height = self.user.userprofile.height
        weight = self.user.userprofile.weight
        # BMI = weight(kg) / height(m)^2
        bmi = round(weight/pow(height/100,2),2)
        logger.debug("User " + 
                     self.user.username + 
                     "\n\tHeight: " + 
                     str(height) + 
                     "\n\tWeight: " + 
                     str(weight) +
                     "\n\tBMI: " + 
                     str(bmi))
        
        return bmi
