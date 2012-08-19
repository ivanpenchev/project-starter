from django import forms

class SignUpForm(forms.Form):
    """
        A sign up form for creating ordinary user with no privileges by
        given his first and last name and his email and preferred password.
    """
    error_messages = {
        'password_confirm' : "Password and confirmation didn't match."
    }
    fname = forms.CharField(label="First name", required=True)
    lname = forms.CharField(label="Last name", required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, weidget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

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
