# Generated by Django 2.2.3 on 2019-07-12 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttonsbot', '0002_auto_20190712_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]
