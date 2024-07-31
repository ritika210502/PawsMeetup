from django.db import models
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
    photo=models.ImageField(upload_to='dog_photos/',blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def age(self):
        today=date.today()
        age=today.year-self.dob.year -((today.month,today.day)< (self.dob.month,self.dob.day))
        return age