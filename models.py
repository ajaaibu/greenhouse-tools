from peewee import *
from settings import *

db = MySQLDatabase(DB_NAME, user=DB_USER) if DB_PASS == 'NO-PASS' else MySQLDatabase(DB_NAME, user=DB_USER, passwd=DB_PASS)

class BaseModel(Model):

    def to_dict(self):
        return self.__data__

    class Meta:
        database = db

class Readings(BaseModel):
    id = IntegerField(primary_key=True)
    sensor = CharField()
    timestamp = CharField()
    type = IntegerField()
    value = DoubleField()
    dbsync = BooleanField(default=False)
    syncref = IntegerField()

class Logs(BaseModel):
    id = IntegerField(primary_key=True)
    user = IntegerField()
    message = CharField()
    date = DateTimeField()  

db.create_tables([Readings], safe=True)