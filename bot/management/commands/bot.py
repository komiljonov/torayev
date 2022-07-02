from django.core.management.base import BaseCommand




class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from tgbot import Bot
        print("Bot is running")
        Bot()