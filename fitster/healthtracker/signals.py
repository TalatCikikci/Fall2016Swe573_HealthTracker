import django.dispatch

# user_initiated signal will be used to inform the system of a new user being
# saved to the datbase
user_initiated = django.dispatch.Signal(
                providing_args=["instance", 
                                "dateofbirth", 
                                "gender", 
                                "height", 
                                "weight", 
                                "notes"])

# item_added signal will inform the system of a new item being saved by the 
# user.
item_added = django.dispatch.Signal(
                providing_args=["itemno", 
                                "itemname", 
                                "itemquantity", 
                                "itemunit", 
                                "itemdate", 
                                "userid"])
