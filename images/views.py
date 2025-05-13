from django.shortcuts import render
from django.http import JsonResponse
from .models import Image
from .forms import ImageForm

def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Image uploaded successfully!"})
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})
