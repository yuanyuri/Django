from django.db import models
from mongoengine import *
connect('ganji', host='127.0.0.1', port=27017)

# ORM


class ItemInfo(Document):
    title = StringField()
    url = StringField()
    pub_date = StringField()
    area = ListField(StringField())
    cates = ListField(StringField())
    look = StringField()
    time = StringField()
    price = IntField()
    meta = {'collection': 'Ganji'}



# Create your models here.
