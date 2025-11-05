from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_kb_size = 2000

    if file.size > max_kb_size * 1024:
        raise ValidationError(
            f'File size cannot be larger than {max_kb_size} KB!'
        )
    
