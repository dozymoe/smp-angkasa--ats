from django.forms import ModelForm
#-
from .models import BlogPosting

class BlogPostingForm(ModelForm):
    class Meta:
        model = BlogPosting
        fields = ['image',
                *BlogPosting.title.fields,
                *BlogPosting.slug.fields,
                *BlogPosting.body.fields,
                *BlogPosting.summary.fields]
