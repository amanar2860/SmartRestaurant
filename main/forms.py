"""
from django import forms
from .models import Item

class AddForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('created_by',
        'title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug')
        """
from django import forms
from django.contrib.auth.models import User

from . import models
class FeedbackForm(forms.ModelForm):
    name=forms.CharField();
    message=forms.CharField();
    class Meta:
        model=models.Feedback
        fields=('name','message')