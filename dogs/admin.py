from django.contrib import admin
from .models import Dog,Breed,Post,Comment,Like,Message
# Register your models here.

class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'size', 'energy_level', 'temperament')

admin.site.register(Dog, DogAdmin)

class BreedAdmin(admin.ModelAdmin):
    list_display=('name',)

admin.site.register(Breed,BreedAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Message)


