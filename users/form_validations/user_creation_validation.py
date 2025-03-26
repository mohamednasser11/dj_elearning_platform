from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        help_text=_("Required. Enter a valid email address.")
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        validators=[validate_password]
    )
    
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=128,
        required=False
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=128,
        required=False
    )
    
    is_instructor = forms.BooleanField(
        label=_("Is Instructor"),
        required=False
    )
    
    is_student = forms.BooleanField(
        label=_("Is Student"),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 
                 'last_name', 'is_instructor', 'is_student')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("A user with that email already exists."),
                code='email_exists'
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        
        # Role validation
        is_instructor = cleaned_data.get('is_instructor')
        is_student = cleaned_data.get('is_student')
        if is_instructor and is_student:
            errors['non_field_errors'] = ValidationError(
                _("A user cannot be both an instructor and a student."),
                code='invalid_role_combination'
            )

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    def get_validation_errors(self):
        """Returns validation errors in API-friendly format"""
        if not self.errors:
            return None
            
        error_dict = {}
        for field, error_list in self.errors.items():
            # Convert field name for non-field errors
            normalized_field = 'non_field_errors' if field == '__all__' else field
            error_dict[normalized_field] = {
                'messages': [str(e) for e in error_list],
                'codes': [getattr(e, 'code', 'invalid') for e in error_list]
            }
        return error_dict

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user