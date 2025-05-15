from django.contrib.auth.models import User
from image_upload.models import Image, Rating

def run():
    user = User.objects.first()
    image = Image.objects.first()

    if not user or not image:
        print("No user or image found in DB.")
        return

    rating = Rating.objects.create(image=image, user=user, rating=4)
    print(f"Rating {rating.rating} added for image {image.id} by user {user.username}")
    print(f"Average Rating for Image {image.id}: {image.average_rating()}")
