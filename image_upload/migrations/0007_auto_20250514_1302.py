from django.db import migrations
from django.contrib.auth.models import User

def link_images_to_users(apps, schema_editor):
    Image = apps.get_model('image_upload', 'Image')  #  'image_upload' is your app name
    for image in Image.objects.all():
        if isinstance(image.user, str):  # Check if image.user is still a string
            try:
                user = User.objects.get(username=image.user)
                image.user = user  # Assign the User object
                image.save()
            except User.DoesNotExist:
                print(f"Warning: User '{image.user}' not found for image ID {image.id}")
                image.user = None  # Or assign a default user if appropriate
                image.save()

def reverse_link_images_to_users(apps, schema_editor):
    #  For reversing, you'd need to convert the User ID back to a username.
    #  This is lossy if you don't have a way to reliably get the username
    #  from the User ID.  For simplicity, we'll leave it blank.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('image_upload', '0006_image_archived'),  #  Replace '0006_image_archived' with the name of the migration that added the archived field
    ]

    operations = [
        migrations.RunPython(link_images_to_users, reverse_link_images_to_users),
    ]

