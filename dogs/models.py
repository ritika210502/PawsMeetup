from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2  # Import GeoIP2
from datetime import date

# Create your models here.
class Breed(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Dog(models.Model):
    SIZE_CHOICES=[
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    ]
    ENERGY_LEVEL_CHOICE=[
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High'),
    ]
    TEMPERAMENT_CHOICES = [
        ('Calm', 'Calm'),
        ('Friendly', 'Friendly'),
        ('Aggressive', 'Aggressive'),
    ]


    name=models.CharField(max_length=50)
    breed=models.ForeignKey(Breed,on_delete=models.CASCADE)
    dob=models.DateField()
    gender=models.CharField(max_length=10,choices=[('Male','Male'),('Female','Female')])
    size=models.CharField(max_length=10,choices=SIZE_CHOICES)
    energy_level=models.CharField(max_length=10,choices=ENERGY_LEVEL_CHOICE)
    temperament=models.CharField(max_length=10,choices=TEMPERAMENT_CHOICES)
    address=models.CharField(max_length=150)
    vaccination_status=models.BooleanField(default=False)
    photo=models.ImageField(upload_to='dog_photos/',default="/static/images/dog_logo.png",blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT,blank=False, null=False,)
    

    # def save(self, *args, **kwargs):
    #     if self.address:
    #         g = GeoIP2()
    #         location = g.lat_lon(self.address)
    #         if location:
    #             self.latitude, self.longitude = location
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def age(self):
        today=date.today()
        age=today.year-self.dob.year -((today.month,today.day)< (self.dob.month,self.dob.day))
        return age if age > 0 else 1

class Post(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='text'
    )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_content_preview()}"

    def get_content_preview(self):
        if self.content_type == 'text' and self.content:
            return f"{self.content[:20]}..."
        elif self.content_type == 'image':
            return "Image Post"
        elif self.content_type == 'video':
            return "Video Post"
        return "Unknown Content"


class Comment(models.Model):
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    create_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}..."

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    def __str__(self):
        return f"{self.user.username} liked {self.post.content[:20]}..."

