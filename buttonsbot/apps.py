from django.apps import AppConfig
from django.conf import settings


class ButtonsBotConfig(AppConfig):
    name = "buttonsbot"

    def ready(self):
        import buttonsbot.signals
        from buttonsbot.scheduler import scheduler
        if settings.SCHEDULER_AUTOSTART:
            if not scheduler.running:
                scheduler.start()
        from buttonsbot.bot import ButtonMailBot
        ButtonMailBot.getInstance()
