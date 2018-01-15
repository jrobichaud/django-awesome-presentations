from django.db import models


class AwesomeModel(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Kitten(models.Model):
    """
    Kitten used to have a `name = models.CharField(max_length=100)` and was replaced by a KittenName model in order
    support multiple names
    """


class KittenName(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
