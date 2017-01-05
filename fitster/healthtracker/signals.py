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

# item_add_requested signal will inform the system of a new item being saved by 
# the user.
item_add_requested = django.dispatch.Signal(
                providing_args=["itemno", 
                                "itemname", 
                                "itemquantity", 
                                "itemunit", 
                                "itemdate", 
                                "userid"])

# item_added signal will inform the system that a log item has been created in 
# the database.
item_added = django.dispatch.Signal(
                providing_args=["historyitem",
                                "itemcalories",
                                "itemquantity"
                                "itemmodifier"])

# history_requested signal will inform the system that the calories and 
# nutritients should be calculated to be displayed to the user.
history_requested = django.dispatch.Signal(
                providing_args=["itemno",
                                "unitmodifier"])
