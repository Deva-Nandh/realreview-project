from rest_framework.exceptions import ValidationError

def validate_image(image):
    # Limit size to 5MB
    if image.size > 5 * 1024 * 1024:
        raise ValidationError("Image file size must be less than 5MB.")
    
    # Limit types to JPEG, PNG, or GIF
    if not image.name.lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
        raise ValidationError("Invalid image format. Only JPEG, PNG, and GIF are allowed.")
