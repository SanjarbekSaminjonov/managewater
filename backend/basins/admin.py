from django.contrib import admin
from .models import BasinId, Basin, BasinMessage

# Register your models here.


class BasinIdAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('id',)


class BasinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'belong_to', 'latitude', 'longitude')
    search_fields = ('name', 'id')


class BasinMessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'basin', 'bat', 'net', 'id')


admin.site.register(BasinId, BasinIdAdmin)
admin.site.register(Basin, BasinAdmin)
admin.site.register(BasinMessage, BasinMessageAdmin)
