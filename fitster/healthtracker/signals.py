import django.dispatch

user_initiated = django.dispatch.Signal(providing_args=["instance", "dateofbirth", "gender", "height", "weight", "notes"])
