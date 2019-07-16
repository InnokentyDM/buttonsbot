from django.db.models.signals import post_save
from django.dispatch import receiver

from buttonsbot.scheduler import scheduler
from buttonsbot.bot import ButtonMailBot
from buttonsbot.models import BotUsers, Message, MessageButton


def send_multiple_messages(msg):
    bot = ButtonMailBot.getInstance()
    parent_button = MessageButton.objects.filter(child_message=msg).first()
    if parent_button:
        users = BotUsers.objects.filter(is_blocked=False, last_pressed_button=parent_button)
        for user in users:
            bot.send_message(chat_id=user.chat_id, msg=msg.text,
                             buttons={button.name: button.id for button in msg.buttons.all()})
            msg.is_sent = True
            msg.save()
    else:
        users = BotUsers.objects.filter(is_blocked=False)
        for user in users:
            bot.send_message(chat_id=user.chat_id, msg=msg.text,
                             buttons={button.name: button.id for button in msg.buttons.all()})
            msg.is_sent = True
            msg.save()


@receiver(post_save, sender=Message, dispatch_uid="save_message")
def message_saved(sender, instance, **kwargs):
    if not instance.is_sent:
        parent_button = MessageButton.objects.filter(child_message=instance).first()
        if parent_button:
            bot_users = BotUsers.objects.filter(is_blocked=False, last_pressed_button=parent_button)
        else:
            bot_users = BotUsers.objects.filter(is_blocked=False)

        bot = ButtonMailBot.getInstance()
        buttons = instance.buttons.all()
        file = None
        if instance.image:
            file = instance.image.file or None
        if instance.send_now:
            for user in bot_users:
                bot.send_message(chat_id=user.chat_id, msg=instance.text,
                                 buttons={button.name:button.id for button in buttons}, photo=file)
                instance.is_sent = True
                instance.save()
        else:
            scheduler.add_job(send_multiple_messages, 'date', run_date=instance.send_at,
                              args=[instance,],
                              id='send message {} to all'.format(instance.short_text),
                              replace_existing=True)