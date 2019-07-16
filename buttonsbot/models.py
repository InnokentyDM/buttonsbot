from django.db import models

from buttonsbot.scheduler import scheduler


class Message(models.Model):
    send_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время отправки')
    text = models.TextField(blank=True, null=True, verbose_name='Текст сообщения')
    buttons = models.ManyToManyField('buttonsbot.MessageButton', blank=True, verbose_name='Кнопки')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    send_now = models.BooleanField(default=False, verbose_name='Отправить сразу')
    image = models.ImageField(upload_to='message_images/', blank=True, null=True, default=None, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @property
    def short_text(self):
        return self.text[0:20]

    def save(self, *args, **kwargs):
        instance = super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.text[0:50]


class MessageButton(models.Model):
    child_message = models.OneToOneField(Message, blank=True, null=True, on_delete=models.CASCADE,
                                         verbose_name='Письмо при нажатии на кнопку')
    name = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='Текст кнопки')
    click_count = models.IntegerField(default=0, verbose_name='Количество нажатий')

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return '{}'.format(self.name)


class BotUsers(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='Имя пользователя')
    chat_id = models.IntegerField(verbose_name='Идентификатор чата')
    notification_count = models.IntegerField(default=0, verbose_name='Уведомлен раз')
    is_blocked = models.BooleanField(default=False, verbose_name='Пользователь заблокирован')
    last_pressed_button = models.ForeignKey(MessageButton, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='Нажатая кнопка')

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

