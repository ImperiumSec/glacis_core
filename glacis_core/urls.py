from django.conf.urls import url

from .api.get_keys import get_keys

app_name = 'glacis_core'

urlpatterns = [
    url(r'^api/1.0/dynamic_key', get_keys)
]
