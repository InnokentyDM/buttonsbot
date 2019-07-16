from django.contrib import admin
from buttonsbot.models import Message, MessageButton, BotUsers


class MessageButtonAdmin(admin.ModelAdmin):
    readonly_fields = ['click_count', ]
    fields = ('name', 'child_message', 'click_count')


admin.site.register(MessageButton, MessageButtonAdmin)


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['views', ]
    list_display = ('short_text', 'send_at', 'is_sent', 'views', )

    def short_text(self, obj):
        return obj.text[0:50]


admin.site.register(Message, MessageAdmin)


class BotUsersAdmin(admin.ModelAdmin):
    model = BotUsers
    readonly_fields = ['notification_count', 'chat_id', ]
    list_display = ('username', 'chat_id', 'notification_count', 'is_blocked',)

admin.site.register(BotUsers, BotUsersAdmin)