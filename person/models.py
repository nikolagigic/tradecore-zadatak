from django.db import models

# This is a test !

class User(models.Model):

    name=models.CharField(max_length=255)
    surname=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=2048)
    logged_in=models.BooleanField(default=False)
    print(logged_in)

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


class Like(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post)
    like=models.BooleanField(default=False)

    liked=models.DateTimeField(auto_now_add=True)

class LookupUserInfo(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)

    givenName=models.CharField(max_length=255, null=True, blank=True, default=None)
    familyName=models.CharField(max_length=255, null=True, blank=True, default=None)
    email=models.CharField(max_length=255, null=True, blank=True, default=None)
    gender=models.CharField(max_length=6, null=True, blank=True, default=None)
    location=models.CharField(max_length=255, null=True, blank=True, default=None)
    timeZone=models.CharField(max_length=255, null=True, blank=True, default=None)
    bio=models.CharField(max_length=255, null=True, blank=True, default=None)
    site=models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        self.full_name=self.user.name+' '+self.user.surname+' - Lookup Info'
        return self.full_name
