

# Create your models here.
from django.db import models

# Create your models here.
class Zhuce(models.Model):
    username=models.CharField(max_length=20)
    age=models.IntegerField()
    # 地理位置
    location=models.CharField(max_length=100)
    # 摄氏度
    centigrade=models.CharField(max_length=20)
    # 手机号
    ipone=models.CharField(max_length=30)
    # 时间第一次被创建的时间
    showtime=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "temperature"
