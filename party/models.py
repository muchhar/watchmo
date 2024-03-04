# models.py
from django.db import models
from account.models import User
import random
import string
class Party(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255)
    game_id = models.CharField(max_length=255)
    data = models.JSONField()
    invite_code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        while True:
            # Generate a six-digit random code
            self.invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            try:
                # Try to save the object
                super().save(*args, **kwargs)
                break
            except:
                # If IntegrityError is raised, it means the code is not unique
                continue

    def __str__(self):
        return f"{self.name} - {self.game}"
class JoinParty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party_id = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return f"{self.user.username} - {self.party_id}"
