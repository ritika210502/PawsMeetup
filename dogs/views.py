from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import DogForm,PostForm,CommentForm,UsernameChangeForm
from .models import Dog,Post,Like,Comment,Message
from django.db import models
from .matching import match_dogs_knn,preprocess_data,train_knn_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.urls import reverse



def home(request):
    return render(request, 'home.html')

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

    posts = Post.objects.filter(user=request.user)
    likes = Like.objects.filter(user=request.user)

    context = {
        'form': form,
        'dog': dog,
        'posts':posts,
        'likes':likes
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

@login_required
def edit_dog(request, dog_id):
    dog=get_object_or_404(Dog,id=dog_id,owner=request.user)

    if request.method=="POST":
        form=DogForm(request.POST,request.FILES,instance=dog)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form=DogForm(instance=dog)

    return render(request,'dogs/edit_dog.html',{'form':form,'dog':dog})

@login_required
def delete_dog(request, dog_id):
    dog=get_object_or_404(Dog,id=dog_id,owner=request.user)
    if request.method=="POST":
        dog.delete()
        return redirect('profile')

    return render(request, 'dogs/delete_dog.html', {'dog': dog})

def view_dog_profile(request, id):
    dog = get_object_or_404(Dog, id=id)
    return render(request, 'dogs/dog_profile.html', {'dog': dog})


def dog_list(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})

# @login_required
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

        # Fetch matched Dog instances based on IDs in the matched_dogs_df
        matched_dogs_ids = matched_dogs_df['id'].tolist()  # Assuming 'id' is the column name for dog IDs
        matched_dogs = Dog.objects.filter(id__in=matched_dogs_ids)

        # Prepare context
        context = {
            'target_dog': target_dog,
            'matched_dogs': matched_dogs,
        }

        return render(request, 'dogs/ai_match_results.html', context)
    else:
        messages.info(request, 'You have not added any dogs yet. Please add a dog to view matches.')
        return redirect('add_dog')

def healthcare(request):
    return render(request,'dogs/healthcare.html')

def training(request):
    return render(request,'dogs/training.html')

def catch_mouse(request):
    return render(request,'games/catch_mouse.html')


# def chat_room(request, room_name):
#     return render(request, 'dog/room.html', {
#         'room_name': room_name
#     })

def feed(request):
    posts=Post.objects.all().order_by('-created_at')
    dog = Dog.objects.get(owner=request.user) 

    return render(request, 'dogs/feeds.html', {'posts': posts,'dog':dog})

@login_required
def post_create(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form=PostForm()
    return render(request,'dogs/post_create.html',{'form':form})

@login_required
def post_delete(request,pk):
    post=get_object_or_404(Post,pk=pk,user=request.user)
    post.delete()
    return redirect('profile')

@login_required
def comment_create(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.user=request.user
            comment.post=post
            comment.save()
            return redirect('feed')
    else:
        form=CommentForm()
    return render(request,'dogs/comment_create.html',{'form':form,'post':post})

@login_required
def comment_delete(request,pk):
    comment=get_object_or_404(Comment,pk=pk,user=request.user)
    comment.delete()
    return redirect('feed')

@login_required
def like(request,pk):
    post = get_object_or_404(Post, pk=pk)
    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like_obj.delete()
    like_count=Like.objects.filter(post=post).count()
    return redirect('feed')


def search_user(request):
    pass

def get_profile_photo(request,owner_id):
    obj=get_object_or_404(Dog,owner_id=owner_id)
    if obj.photo:
        image_data = obj.photo.read()
        return HttpResponse(image_data, content_type="image/jpeg")
    else:
        return HttpResponse(status=404)  


def chat_view(request, dog_id):
    target_dog = get_object_or_404(Dog, id=dog_id)
    current_dog = Dog.objects.get(owner=request.user)
    messages = Message.objects.filter(
        (models.Q(sender=current_dog, receiver=target_dog) |
         models.Q(sender=target_dog, receiver=current_dog))
    ).order_by('timestamp')

    return render(request, 'dogs/chat.html', {
        'current_dog': current_dog,
        'target_dog': target_dog,
        'messages': messages
    })

def send_message(request):
    if request.method == 'POST':
        sender = Dog.objects.get(owner=request.user)
        receiver_id = request.POST.get('receiver_id')
        receiver = get_object_or_404(Dog, id=receiver_id)
        message_text = request.POST.get('message')
        timestamp = timezone.localtime(timezone.now()).strftime("%I:%M %p %d/%m/%Y") 

        # Create the message
        message = Message.objects.create(sender=sender, receiver=receiver, message=message_text)

        # Prepare email content
        email_subject = "You have a new message!"
        email_message = render_to_string('dogs/email_notification.html', {
            'receiver': receiver.owner,  # Receiver's name
            'sender_dog': sender.name,   # Sender's dog name
            'message_text': message_text,  # Actual message text
            'chat_url': request.build_absolute_uri(reverse('chat', args=[receiver.id])),  # Chat URL
        })

        # Send the email with HTML content
        send_mail(
            email_subject,
            email_message, 
            'no-reply@pawsmeetup.com',
            [receiver.owner.email],
            fail_silently=False,
            html_message=email_message  
        )

        # Return success response with message details for UI update
        return JsonResponse({
            'status': 'success',
            'message': 'Message sent!',
            'sender_name': sender.name,  
            'message_text': message_text,
            'timestamp': timestamp
 
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


