from django.db import models


class AwesomeModel(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Kitten(models.Model):
    name = models.CharField(max_length=100)

