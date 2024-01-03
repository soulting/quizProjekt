from django.db import models

class User(models.Model):
    pole1 = models.CharField(max_length=100)
    pole2 = models.IntegerField()

    id = models.IntegerField()(Integer, primary_key=True)
    username = models.(String, nullable=False)
    password = models.Column(String, nullable=False)
    quiz_ids = models.Column(ARRAY(Integer))
    is_admin = models.Column(Boolean, nullable=False)
    icon_name = models.Column(String)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    quiz_ids = Column(ARRAY(Integer))
    is_admin = Column(Boolean, nullable=False)
    icon_name = Column(String)