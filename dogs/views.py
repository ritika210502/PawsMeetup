from django.shortcuts import render,redirect,get_object_or_404
from .forms import DogForm
from .models import Dog
from .matching import match_dogs_knn,preprocess_data,train_knn_model

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

def ai_match_dogs(request,dog_id):

    try:
        dog_id = int(dog_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid dog ID")

    target_dog=get_object_or_404(Dog,id=dog_id)
    dogs=preprocess_data()
    model,scaler=train_knn_model(dogs)
    matched_dogs_df = match_dogs_knn(dog_id, model, scaler)

    # Convert DataFrame to a list of dictionaries
    matched_dogs = matched_dogs_df.to_dict(orient='records')

    # print("Target Dog:", target_dog)
    # print(matched_dogs_df.dtypes)


    # Prepare context
    context = {
        'target_dog': target_dog,
        'matched_dogs': matched_dogs
    }

    return render(request, 'dogs/ai_match_results.html', context)
