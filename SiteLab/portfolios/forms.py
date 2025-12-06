from django import forms
from .models import Portfolio, PortfolioTemplate

class PortfolioForm(forms.ModelForm):
    """
    Single form to edit per-user portfolio content and template selection.
    """

    template = forms.ModelChoiceField(
        queryset=PortfolioTemplate.objects.all(),
        required=False,
        label="Change Template",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Portfolio
        fields = [
            'template',
            'first_name',
            'last_name',

            'tagline',
            'about_me',
            'contact_email',

            'project1_title', 'project1_description', 'project1_url',
            'project2_title', 'project2_description', 'project2_url',
            'project3_title', 'project3_description', 'project3_url',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),

            # Project 1 fields
            'project1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project1_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project1_url': forms.URLInput(attrs={'class': 'form-control'}),

            # Project 2 fields
            'project2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project2_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project2_url': forms.URLInput(attrs={'class': 'form-control'}),

            # Project 3 fields
            'project3_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project3_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project3_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['tagline'].label = "Tagline / Profession"
        self.fields['about_me'].label = "About Me"
        self.fields['contact_email'].label = "Contact Email"

        self.fields['project1_title'].label = "Project 1 Title"
        self.fields['project2_title'].label = "Project 2 Title"
        self.fields['project3_title'].label = "Project 3 Title"