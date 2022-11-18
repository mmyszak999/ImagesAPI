from django.contrib import admin

from api.models import Image, Account, AccountTier, ExpiringLinkToken


class ImageAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


class AccountTierAdmin(admin.ModelAdmin):
    pass


class ExpiringLinkTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(ExpiringLinkToken, ExpiringLinkTokenAdmin)

