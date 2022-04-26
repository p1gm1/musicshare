import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class LowercaseValidator:
    """
    Validate wheter the password has at least one lowercase character
    """
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least one lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one lowercase letter, a-z."
        )


class UppercaseValidator:
    """
    Validate wheter the password has at least one uppercase character
    """
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, A-Z."
        )


class SpecialCharactersValidator:
    def validate(self, password, user=None):
        if not re.findall('[@$!\]#?]', password):
            raise ValidationError(
                _("The password must contain at least one of the following characters: !, @, #, ? or ]."),
                code='password_no_special_char'
            )
    
    def get_help_text(self):
        return _(
            "Your password must contain at least one of the following characters: !, @, #, ? or ]."
        )
