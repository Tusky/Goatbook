from django import forms

class Chat(forms.Form):
    message         = forms.CharField(label="", widget=forms.Textarea(attrs={'autofocus':'autofocus', 'placeholder': 'Type your message here...'}))
