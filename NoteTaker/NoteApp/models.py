from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Note(models.Model):
    # fields: auto-increment primary key, title, body, auto Date, User author
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    # string representation of model
    def __str__(self):
        return self.title