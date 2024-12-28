from django.contrib import admin

from reviews.models import Review, Title


admin.site.register(Title)
admin.site.register(Review)
