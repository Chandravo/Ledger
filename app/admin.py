from django.contrib import admin
from .models import User, Room, money_request, receipt

admin.site.register(User)
admin.site.register(Room)
admin.site.register(money_request)
admin.site.register(receipt)
