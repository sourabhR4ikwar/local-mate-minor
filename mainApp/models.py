from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    profile = models.CharField(max_length=250,default='')
    isGuide = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Guide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=250)
    quote = models.CharField(max_length=300)
    rate = models.IntegerField()
    ratings = models.IntegerField(default=0)
    i_will_show_you = models.TextField()
    about_me =  models.TextField()
    languages = models.CharField(max_length=250)
    isAvailable = models.BooleanField(default=True)

class Trips(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    location = models.CharField(max_length=250)
    dateStart = models.DateField()
    dateEnd = models.DateField()
    price = models.IntegerField()
    paymentVerified = models.BooleanField(default=False)
    # conversations = models.ForeignKey('Conversations', on_delete=models.CASCADE)
    reviews = models.ForeignKey('Reviews',default=None, on_delete=models.CASCADE)

class Conversations(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE, default=None, related_name='%(class)s_requests_created')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    message = models.TextField()

class Reviews(models.Model):
    # trip = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name='%(class)s_requests_created' )
    review = models.TextField(default='')
    rating = models.IntegerField(default=0)



