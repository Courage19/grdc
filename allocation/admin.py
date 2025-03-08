from django.contrib import admin
from .models import CustomUser, Stand, Application, TitleDeedRequest

admin.site.register(CustomUser)
admin.site.register(Stand)
admin.site.register(Application)
admin.site.register(TitleDeedRequest)
