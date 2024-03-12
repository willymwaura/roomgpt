
from django.contrib import admin
from django.contrib import admin
from  mainapp. models import User,CreditBalance,ImageHistory,PaymentsActivated


# Register your models here.

admin.site.register(User)
admin.site.register(CreditBalance)
admin.site.register(ImageHistory)
admin.site.register(PaymentsActivated)