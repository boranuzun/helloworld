from django.db import models
from backend.users.models import CustomUser

class Place(models.Model):
    venue_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.venue_name)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_pic = models.URLField(max_length=200)
    date = models.DateTimeField()
    event_capacity = models.IntegerField()
    price = models.IntegerField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

class Interested_In_Event(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return 'Event : ' + '{}'.format(self.event) + ', User : ' + '{}'.format(self.user)
        
    class Meta:
        unique_together = ["event", "user"]

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    msg = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)