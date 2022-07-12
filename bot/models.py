import os
from django.db import models
from telegram import ReplyKeyboardRemove, Update
from telegram import User as TelegramUser
# Create your models here.


class User(models.Model):
    id: int
    chat_id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=100, null=True)
    is_registered = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    start_time = models.DateTimeField(auto_now_add=True)
    reg_date = models.DateTimeField(null=True)

    __str__ = lambda self: f"{self.name} | {self.number} | {self.chat_id}"




    @classmethod
    def get(cls, update:Update) -> "tuple[TelegramUser, User]":
        user = (update.message or update.callback_query).from_user
        # os.system('cls')
        return user, cls.objects.filter(chat_id=user.id).first()
    
    @classmethod
    def all(cls) -> "list[User]":
        return cls.objects.all()



class Post(models.Model):
    media = models.FileField(upload_to="media/")
    media_type = models.IntegerField(choices=[
        (0, 'Text'),
        (1, 'Photo'),
        (2, 'Video'),
        (3, 'Audio'),
        (4, 'Document'),
    ])
    caption = models.TextField(max_length=1024)

    def send_to(self, user:TelegramUser):
        
        if self.media_type == 0:
            user.send_message(self.caption, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        elif self.media_type == 1:
            user.send_photo(open(self.media.path, 'rb'), caption=self.caption, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        elif self.media_type == 2:
            user.send_video(open(self.media.path, 'rb'), caption=self.caption, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        elif self.media_type == 3:
            user.send_audio(open(self.media.path, 'rb'), caption=self.caption, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        elif self.media_type == 4:
            user.send_document(open(self.media.path, 'rb'), caption=self.caption, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())



class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    @property
    def json(self):
        return {
            'name': self.name,
            'url': self.url
        }