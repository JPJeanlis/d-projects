from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms


class RenewProductForm(forms.Form):
    """Form for an employee to update information about products."""
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_possesion_date(self):
        data = self.cleaned_data['possesion_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - already owned'))
        # Check date is in range employee allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - owned more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
