from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
#-
from .models import WebPage
from .serializers import WebPageSerializer


@method_decorator(login_required, name='dispatch')
class List(ListAPIView):
    queryset = WebPage.objects.filter(published_at__isnull=False)
    serializer_class = WebPageSerializer
