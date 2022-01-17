"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path
from django.utils.translation import gettext as _
#-
from website import views

urlpatterns = i18n_patterns(
    path(_('news/'), include('blog_posting.urls', namespace='BlogPosting')),
    path('files/', include('my_files.urls', namespace='MyFile')),
    path('admin/editor-helptext.<str:format>', views.EditorHelpText.as_view(),
        name='EditorHelpText'),
    path('', include('web_page.urls', namespace='WebPage')),

    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('index.<str:format>', views.Home.as_view(), name='Home'),
    path('', views.Home.as_view()),
]
