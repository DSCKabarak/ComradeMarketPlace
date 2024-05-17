from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class FileSizeValidator:
    max_size = 1.5 * 1024 * 1024

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(f"File size should be less than {self.max_size / (1024 * 1024)}MB.")