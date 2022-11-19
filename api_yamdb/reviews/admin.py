from django.contrib import admin

from .models import Group, User


class GroupAdmin(admin.ModelAdmin):
    list_display = ("vkId", "updated", "type", "name", "screenName", "photo",
                    "cover", "mainSection", "country", "city", "activity",
                    "status", "description", "ageLimits", "membersCount",
                    "fixedPost", "contacts", "site",)
    search_fields = ("name", "description", "membersCount")
    list_filter = ("type", "country", "city",)
    # list_editable = ("category",)
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)
admin.site.register(User)
