# board/forms.py
from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['card_to']
        widgets={'password':forms.PasswordInput()}
