from django.contrib import admin
from .models import Role,User,Child,Activity


# Register your models here.

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Child)
admin.site.register(Activity)