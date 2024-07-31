from django.shortcuts import render,redirect
from .forms import DogForm
from .models import Dog
# Create your views here.
def add_dog(request):
    if request.method=='POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dog_list')

    else:
        form=DogForm()
    return render(request,'dogs/add_dog.html',{'form':form})

def dog_list(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})
