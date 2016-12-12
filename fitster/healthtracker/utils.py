import requests
import math
import logging
from django.conf import settings


logger = logging.getLogger('django')


class ApiWrapper:

    def __init__(self):
        self.api_key = settings.USDA_API_KEY
        self.base_url = settings.USDA_BASE_URL
        self.resp_format = settings.USDA_RESPONSE_FORMAT
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
        operation = 'search'
        
        search_url = self.forgeUrl(operation) + '&q={}'.format(search_item)
        
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
        
