from django.db import models

class User(models.Model):

    name=models.CharField(max_length=255)
    surname=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=2048)
    logged_in=models.BooleanField(default=False)

    def __str__(self):
        self.full_name=self.name+' '+self.surname
        return self.full_name


class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    content=models.TextField()
    likes=models.IntegerField(default=0)

    def __str__(self):
        self.full_name=self.author.name+' '+self.author.surname+' - '+self.title
        return self.full_name