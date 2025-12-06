from django import forms
from .models import Portfolio, ContactMessage, PortfolioTemplate

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        exclude = ('user', 'created_at', 'last_updated', 'is_published')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'tagline': forms.TextInput(attrs={'class':'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'hidden-file-input',}),
            'about': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
            'contact_email': forms.EmailInput(attrs={'class':'form-control'}),
            'instagram': forms.TextInput(attrs={'class':'form-control', 'placeholder':'instagram.com/yourname'}),
            'twitter': forms.TextInput(attrs={'class':'form-control', 'placeholder':'twitter.com/yourname'}),
            'website': forms.URLInput(attrs={'class':'form-control', 'placeholder':'https://example.com'}),
            'project1_title': forms.TextInput(attrs={'class':'form-control'}),
            'project1_description': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'project1_url': forms.URLInput(attrs={'class':'form-control'}),
            'project2_title': forms.TextInput(attrs={'class':'form-control'}),
            'project2_description': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'project2_url': forms.URLInput(attrs={'class':'form-control'}),
            'project3_title': forms.TextInput(attrs={'class':'form-control'}),
            'project3_description': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'project3_url': forms.URLInput(attrs={'class':'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'message': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
        }
