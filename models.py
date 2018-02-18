from peewee import *
from settings import *

db = MySQLDatabase(DB_NAME, user=DB_USER) if DB_PASS == 'NO-PASS' else MySQLDatabase(DB_NAME, user=DB_USER, passwd=DB_PASS)

class BaseModel(Model):

    def to_dict(self):
        return self.__data__

    class Meta:
        database = db
        auto_increment = True

class Readings(BaseModel):
    id = AutoField(primary_key=True)
    sensor = CharField()
    timestamp = CharField()
    type = IntegerField()
    value = DoubleField()
    dbsync = BooleanField(default=False)
    syncref = IntegerField(null = True)

class Logs(BaseModel):
    id = AutoField(primary_key=True)
    user = IntegerField()
    message = CharField()
    date = DateTimeField()  

db.create_tables([Readings, Logs], safe=True)