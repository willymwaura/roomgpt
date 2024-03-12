
from django.contrib import admin
from django.contrib import admin
from . models import User,CreditBalance,ImageHistory


# Register your models here.

admin.site.register(User)
admin.site.register(CreditBalance)
admin.site.register(ImageHistory)