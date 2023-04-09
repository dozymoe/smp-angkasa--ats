"""DRF Serializers for working with web pages
"""
from rest_framework import serializers
#-
from .models import WebPage

class WebPageSerializer(serializers.HyperlinkedModelSerializer):
    """Format web page as json response
    """
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = WebPage
        fields = ['id', 'title', 'body', 'summary', 'created_at', 'url']
