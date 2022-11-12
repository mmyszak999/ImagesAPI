from django.contrib import admin

from api.models import Image, Account


class ImageAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(Account, AccountAdmin)

