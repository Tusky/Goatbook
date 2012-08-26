from django import forms

class WallPostForm(forms.Form):
    wallpost         = forms.CharField(label="", widget=forms.Textarea(attrs={
                                                                                'autofocus':'autofocus',
                                                                                'placeholder': 'What\'s on your mind?',
                                                                                'autocomplete': 'off',
                                                                                'aria-autocomplete': 'list',
                                                                                'aria-expanded': 'false',
                                                                                'aria-invalid': 'false',
                                                                              }))