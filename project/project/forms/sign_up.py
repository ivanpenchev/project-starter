from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    """
        A sign up form for creating ordinary user with no privileges by
        given his first and last name and his email and preferred password.
    """
    error_messages = {
        'email_already_used' : 'The entered email address is already signed up.',
        'password_confirm' : "Password confirmation didn't match."
    }
    fname = forms.CharField(label="First name", required=True)
    lname = forms.CharField(label="Last name", required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean_email(self):
        """
            Check if the entered email address isn't already in the database
            and if it is - raise form ValidationError.
        """
        email = self.cleaned_data['email']
        user_with_this_email = User.objects.filter(email=email).all()
        if user_with_this_email:
            raise forms.ValidationError(
                self.error_messages['email_already_used']
            )
        return email

    def clean_confirm_password(self):
        """
            Check whether confirm_password is the same as password
            or not. If it isn;t we return form validation error.
        """
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_confirm'])
        return confirm_password
