import requests
import math
from django.conf import settings



class ApiWrapper:

    def __init__(self):
        self.api_key = settings.USDA_API_KEY
        self.base_url = settings.USDA_BASE_URL
        self.resp_format = settings.USDA_RESPONSE_FORMAT

    def forgeUrl(self, operation):
        url_mask = '{}/{}/?format={}&api_key={}'
        forged_url = url_mask.format(self.base_url,
                                     operation, 
                                     self.format, 
                                     self.api_key)
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
        
        search_url = forgeUrl(operation) + '&q={}'.format(search_item)
        response = requestJson(search_url)
        response_list = response["list"]["item"]

        for item in response_list:
        	print(item["name"])
	
	
class UserUtils:
    
    # Initialize with a 'user' to play with its data.
    def __init__(self, user):
        self.user = user
        
    def getBmi(self):
        height = self.user.userprofile.height
        weight = self.user.userprofile.weight
        # BMI = weight(kg) / height(m)^2
        bmi = round(weight/pow(height/100,2),2)
        return bmi
        
