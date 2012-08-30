from django import forms

class WallPostForm(forms.Form):
    wallpost         = forms.CharField(label="", widget=forms.Textarea(attrs={
                                                                                'autofocus':'autofocus',
                                                                                'placeholder': 'What\'s on your mind?',
                                                                                'autocomplete': 'off'}))

class WallCommentForm(forms.Form):
    wallcomment      = forms.CharField(label="", widget=forms.Textarea(attrs={
                                                                                'class':        'commentbox',
                                                                                'placeholder':  'Write a comment...',
                                                                                'autocomplete': 'off'}))