from django.shortcuts import render,redirect,get_object_or_404
from .forms import DogForm
from .models import Dog
from .matching import match_dogs_knn,preprocess_data,train_knn_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm



def home(request):
    return render(request, 'home.html')

def password(request):
    return render(request,'registration/password_reset_form.html')

# Create your views here.
def register(request):
    if(request.method=="POST"):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request,'registration/register.html',{'form':form})

@login_required
def profile(request):
    try:
        dog = Dog.objects.get(owner=request.user) 
    except Dog.DoesNotExist:
        dog = None

    if request.method == 'POST':
        if dog is None:
            form = DogForm(request.POST, request.FILES)
            if form.is_valid():
                new_dog = form.save(commit=False)
                new_dog.owner = request.user
                new_dog.save()
                return redirect('profile')
        else:
            form = DogForm(instance=dog)
    else:
        if dog:
            form = DogForm(instance=dog)
        else:
            form = DogForm()

    context = {
        'form': form,
        'dog': dog
    }

    return render(request, 'registration/profile.html', context)



@login_required
def add_dog(request):
    if request.method=='POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('ai_match_dogs',dog_id=dog.id)
            return redirect('profile')

    else:
        form=DogForm()
    return render(request,'dogs/add_dog.html',{'form':form})

def dog_list(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})

# @login_required
# def ai_match_dogs(request,dog_id):

#     try:
#         dog_id = int(dog_id)
#     except ValueError:
#         return HttpResponseBadRequest("Invalid dog ID")

#     target_dog=get_object_or_404(Dog,id=dog_id)
#     dogs=preprocess_data()
#     model,scaler=train_knn_model(dogs)
#     matched_dogs_df = match_dogs_knn(dog_id, model, scaler)

#     # Convert DataFrame to a list of dictionaries
#     matched_dogs = matched_dogs_df.to_dict(orient='records')

#     # print("Target Dog:", target_dog)
#     # print(matched_dogs_df.dtypes)


#     # Prepare context
#     context = {
#         'target_dog': target_dog,
#         'matched_dogs': matched_dogs
#     }

#     return render(request, 'dogs/ai_match_results.html', context)

@login_required
def ai_match_dogs(request):
    # Check if the user has added any dogs
    user_dogs = Dog.objects.filter(owner=request.user)

    if user_dogs.exists():
        # Use the first dog from the user's dogs for the matching process
        target_dog = user_dogs.first()

        # Perform the matching
        dogs = preprocess_data()
        model, scaler = train_knn_model(dogs)
        matched_dogs_df = match_dogs_knn(target_dog.id, model, scaler)

        # Convert DataFrame to a list of dictionaries
        matched_dogs = matched_dogs_df.to_dict(orient='records')

        # Prepare context
        context = {
            'target_dog': target_dog,
            'matched_dogs': matched_dogs,
        }

        return render(request, 'dogs/ai_match_results.html', context)
    else:
        messages.info(request, 'You have not added any dogs yet. Please add a dog to view matches.')
        return redirect('add_dog')
