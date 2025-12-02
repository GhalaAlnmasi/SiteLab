from django import forms
from django.forms.widgets import CheckboxInput
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Username'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Email'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get("password")
        cp = cleaned.get("confirm_password")
        if p != cp:
            raise forms.ValidationError("Passwords do not match")
        return cleaned
    
    def save(self, commit=True):
        # استدعاء دالة save الأصلية لكن لا تقم بحفظها في قاعدة البيانات (commit=False)
        user = super().save(commit=False)
        
        # استخدام set_password لتشفير كلمة المرور وتعيينها للمستخدم
        # هذا يضمن أن كلمة المرور مشفرة قبل الحفظ
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            
        return user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Password'
    }))

class ProfileForm(forms.ModelForm):
    avatar_clear = forms.BooleanField(required=False, widget=CheckboxInput)
    class Meta:
        model = Profile
        fields = ["avatar", "job_title", "bio"]
        widgets = {
            "avatar": forms.FileInput(attrs={
                'class': 'hidden-file-input',
                'id': 'id_avatar'
            }),
            "job_title": forms.TextInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Job Title'
            }),
            "bio": forms.Textarea(attrs={
                'class': 'minimal-input',
                'rows': 4,
                'placeholder': 'Bio'
            }),
        }

    def save(self, commit=True):
      instance = super().save(commit=False)
      
      if self.cleaned_data.get('avatar_clear'):
          if instance.avatar:
              instance.avatar.delete(save=False) 
      
      if commit:
          instance.save()
          
      return instance