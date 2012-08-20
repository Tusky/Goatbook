from django import forms

class Chat(forms.Form):
    message         = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'}))
