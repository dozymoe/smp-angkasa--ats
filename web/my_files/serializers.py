from rest_framework import serializers
#-
from .models import MyFile


class MyFileSerializer(serializers.HyperlinkedModelSerializer):
    attr_src = serializers.CharField(source='get_absolute_url')
    attr_srcset = serializers.CharField(source='get_html_attr_srcset')
    attr_sizes = serializers.CharField(source='get_html_attr_sizes')

    class Meta:
        model = MyFile
        fields = ['id', 'description', 'alt_text', 'created_at', 'attr_src',
                'attr_srcset', 'attr_sizes']
