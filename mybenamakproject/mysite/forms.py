# from django import forms

# from .models import ContactSubmission

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactSubmission
#         fields = ['name', 'email', 't_shirt_type', 'design', 'message']
from django import forms
from .models import PortfolioItem

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    t_shirt_type = forms.CharField(max_length=100)
    design = forms.FileField()
    message = forms.CharField(widget=forms.Textarea)


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title', 'category', 'image', 'description']