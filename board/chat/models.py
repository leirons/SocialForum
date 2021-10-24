from django.db import models
from board import settings
# Create your models here.


class Chat(models.Model):
    title  = models.CharField(max_length=255,unique=True,blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,help_text='Пользователи подключенные  к чату')

    def __str__(self):
        return self.title

    def connect_user(self,user):
        """
        Возвращаем True. если пользователь добавлен в чат
        """
        is_user = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user = True
        elif user in self.users.all():
            is_user = True
        return is_user

    def disconnect(self,user):
        """
        Возвращаем True, если юзер вышел.
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
            return f"Chat-{self.id}"


class ChatMessageManager(models.Manager):
    def by_room(self,room):
        qs = ChatMessage.object.filter(room=room).order_by('-timestamp')
        return qs

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False,blank=False)

    objects = ChatMessageManager()
    def __str__(self):
        return self.content
