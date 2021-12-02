from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title, User

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comments)
