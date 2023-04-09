"""Django views for working with files via Rest API
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
#-
from .models import MyFile
from .serializers import MyFileSerializer

@method_decorator(login_required, name='dispatch')
class List(ListAPIView):
    """List all files
    """
    queryset = MyFile.objects.filter(mimetype__startswith='image/')
    serializer_class = MyFileSerializer
