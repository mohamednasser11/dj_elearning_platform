from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        help_text=_("Required. Enter a valid email address."),
        required=True
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'password')

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