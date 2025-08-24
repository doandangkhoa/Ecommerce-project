from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter your password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm password',
        'class' : 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        
    # override
    def __init__(self, *args, **kwags):
        super(RegistrationForm, self).__init__(*args, **kwags)
        for field_name, field_object in self.fields.items():
            field_object.widget.attrs['class'] = 'form-control'
            
    # Override
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean() # a dictionary stored data from the form
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
            
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match!')
        return cleaned_data
    
        