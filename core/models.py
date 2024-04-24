from django.db import models
from django.contrib.auth.models import User

class Code(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(("Code a envoyer par sms"), max_length=6)