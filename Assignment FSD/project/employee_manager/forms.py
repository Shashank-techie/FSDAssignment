from django import forms

class UserLoginDetails(forms.Form):
    userName = forms.CharField(
        label="User Name",
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            "id": "userName",
        })
    )

    userPassword = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "userPassword",
        })
    )


class UserRegistrationDetails(forms.Form):
    userName = forms.CharField(
        max_length=75, 
        required=True,
        label="User Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "userName",
        })
    )

    userEmail = forms.EmailField(
        label="Email Id",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "userEmail"
        })
    )

    userPassword = forms.CharField(
        label="Password",
        required=True,
        min_length=8,
        max_length=25,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "userPassword"
        })
    )

    confirmPassword = forms.CharField(
        label="Confirm Password",
        required=True,
        min_length=8,
        max_length=25,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "confirmPassword"
        })
    )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("userPassword")
        confirm_password = cleaned_data.get("confirmPassword")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data