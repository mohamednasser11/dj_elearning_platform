from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ..models import Course, Departments
from users.models import User

class CoursePayloadValidation(forms.ModelForm):
    title = forms.CharField(
        label=_("Course Title"),
        max_length=255,
        help_text=_("Required. Maximum 255 characters.")
    )
    
    description = forms.CharField(
        label=_("Description"),
        max_length=500,
        help_text=_("Required. Maximum 500 characters.")
    )
    
    price = forms.DecimalField(
        label=_("Price"),
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text=_("Must be a positive number.")
    )
    
    departmentId = forms.ModelChoiceField(
        label=_("Department"),
        queryset=None,  # Will be set in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )
    
    instructorId = forms.ModelChoiceField(
        label=_("Instructor"),
        queryset=None,  # Will be set in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )

    rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False, default=0)
    number_of_students = forms.IntegerField(required=False, default=0)
    image_url = forms.URLField(required=True, max_length=500)

    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'departmentId', 'instructorId']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set department queryset
        self.fields['departmentId'].queryset = Departments.objects.all()
        # Set instructor queryset (only users marked as instructors)
        self.fields['instructorId'].queryset = User.objects.filter(is_instructor=True)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 10:
            raise ValidationError(
                _("Title must be at least 10 characters long."),
                code='title_too_short'
            )
        return title.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 30:
            raise ValidationError(
                _("Description must be at least 30 characters long."),
                code='description_too_short'
            )
        return description.strip()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price > 1000000:
            raise ValidationError(
                _("Price cannot exceed $1,000,000."),
                code='price_too_high'
            )
        return price

    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        
        # Validate instructor belongs to department (if needed)
        instructor = cleaned_data.get('instructorId')
        department = cleaned_data.get('departmentId')
        
        if instructor and department:
            if not instructor.departments_taught.filter(id=department.id).exists():
                errors['instructorId'] = ValidationError(
                    _("Selected instructor doesn't teach in this department."),
                    code='invalid_instructor_for_department'
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
            normalized_field = 'non_field_errors' if field == '__all__' else field
            error_dict[normalized_field] = {
                'messages': [str(e) for e in error_list],
                'codes': [getattr(e, 'code', 'invalid') for e in error_list]
            }
        return error_dict