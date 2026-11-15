import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_publisher_name(value):
    if not value or not value.strip():
        raise ValidationError(_('Publisher name is required.'))
    val = value.strip()
    if len(val) < 2:
        raise ValidationError(_('Publisher name must contain at least two characters.'))
    if len(val) > 150:
        raise ValidationError(_('Publisher name cannot exceed 150 characters.'))
    
    # Check for digits (Western digits 0-9 and Arabic-Indic digits ٠-٩)
    if re.search(r'[\d٠-٩]', val):
        raise ValidationError(_('Numbers are not allowed in publisher names.'))
    
    # Must contain at least one alphabetic letter (Unicode letter category)
    if not re.search(r'[^\W\d_]', val, re.UNICODE):
        raise ValidationError(_('Publisher name must contain valid letters and permitted separators.'))

def validate_article_title(value):
    if not value or not value.strip():
        raise ValidationError(_('Article title is required.'))
    val = value.strip()
    if len(val) < 5:
        raise ValidationError(_('Article title must contain at least five characters.'))
    if len(val) > 2048:
        raise ValidationError(_('Article title exceeds the maximum allowed length.'))
    
    # Must contain at least one alphabetic letter (rejects titles consisting only of numbers or symbols)
    if not re.search(r'[^\W\d_]', val, re.UNICODE):
        raise ValidationError(_('A title cannot consist only of numbers or symbols.'))

def validate_article_content(value):
    if not value or not value.strip():
        raise ValidationError(_('Article content is required.'))
    val = value.strip()
    
    # Check minimum length of non-whitespace characters (>= 30)
    non_ws_chars = [c for c in val if not c.isspace()]
    if len(non_ws_chars) < 30:
        raise ValidationError(_('Article content must contain at least 30 non-whitespace characters.'))
    
    # Must contain at least one alphabetic letter (rejects numbers-only or symbols-only content)
    if not re.search(r'[^\W\d_]', val, re.UNICODE):
        raise ValidationError(_('Article content must contain written text, not only numbers or symbols.'))
