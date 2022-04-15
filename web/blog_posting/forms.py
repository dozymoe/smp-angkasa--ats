from django.forms import ModelForm
#-
from .models import BlogPosting

class BlogPostingForm(ModelForm):
    class Meta:
        model = BlogPosting
        exclude = []
        #fields = ['title', 'body', 'summary', 'slug', 'image']
