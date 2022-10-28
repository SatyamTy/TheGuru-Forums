from django import forms
from .models import Post, id_info
from tinymce.models import HTMLField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "tags"]
class id_form(forms.ModelForm):
    class Meta:
        model = id_info
        fields = ["name", "Class", "section", "father_name", "mother_name", "mobile", "Adress", "pic"]
