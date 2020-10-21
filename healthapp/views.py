import logging

import pymysql
import xlwt
from django.shortcuts import render
from datetime import date, timedelta
# Create your views here.
from django.shortcuts import render
# Create your views here.
import requests
from django.shortcuts import HttpResponse, render, redirect
import datetime
from healthapp.models import Zhuce

logger=logging.getLogger('log')
def index(request):
    return  render(request,'index.html')

def submit(request):
    try:
        username=request.POST['username']
        age=request.POST['age']
        location=request.POST['location']
        centigrade=request.POST['centigrade']
        ipone=request.POST['ipone']
        if request.POST['showtime']:
            showtime=request.POST['showtime']
        else:
            showtime=datetime.datetime.now()
        logger.info(f"姓名：{username},年龄：{age},地理位置：{location},温度：{centigrade},手机号：{ipone},时间：{showtime}")
        Zhuce.objects.create(username=username, age=age,
                             location=location, centigrade=centigrade,ipone=ipone,showtime=showtime)
        logger.info("入库成功")
        return HttpResponse(f"入库成功,姓名：{username},年龄：{age},地理位置：{location},温度：{centigrade},手机号：{ipone},时间：{showtime}")
    except Exception as p:
        logger.error(f"错误的信息为{p}")
        return HttpResponse(f"入库失败")


def zhanshi(request):
    try:
    # 数据从数据库中获取
        messages=Zhuce.objects.all()
        return render(request,'zhanshi.html',{"messages": messages})
    except Exception as w:
        logger.error(f"展示失败，错误信息：{w}")
        return HttpResponse("展示错误，请刷新")

def send_email(request):
    try:
        # 查询的所有记录
        # wa = xlwt.Workbook()
        # b = wa.add_sheet('health')
        # lists=Zhuce.objects.all()
        # for index,td in enumerate(lists):
        #     b.write(index,td.showtime)
        # number=Zhuce.objects.get(centigrade=str(36.4))

        # start_date=datetime.datetime.today()
        # number=Zhuce.objects.filter(pub_date__range=(today, tomorrow))
        # print(number)
        # 创建连接
        coon = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                               db='healthproject')
        # 创建游标对象
        cuoer = coon.cursor()
        sql_number="SELECT * FROM temperature WHERE centigrade >34"
        today = date.today()
        tomorrow = today + timedelta(1)
        sql="SELECT * FROM temperature WHERE showtime BETWEEN '2020-10-20' and '2020-10-21'"
        result_number = cuoer.execute(sql_number)
        people_number=result_number
        # 记录
        cuoer.execute(sql)
        jilus = cuoer.fetchall()  # 接收全部的返回结果；
        li=[]
        for i in jilus:
            li.append(i)
        from email.mime.text import MIMEText
        import smtplib
        mail_host = "smtp.163.com"
        mail_user = "自己的网易邮箱"
        mail_pass = "密码"
        receivers = ["发送人的邮箱"]  # 接收邮件，
        content = f"""总人数{people_number}和详情{li}"""
        title = '健康项目管理人数详情'
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(mail_user)
        message['To'] = ",".join(receivers)
        message['Subject'] = title
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())  # 发送
        smtpObj.quit()
        logger.info(f"发送邮件成功：收件人地址{receivers}")
        return HttpResponse(f"发送邮件成功：收件人地址{receivers}")
    except Exception as q:
        logger.error(f"发送邮件失败，错误信息{q}")
        return HttpResponse(f"发送邮件失败，错误信息{q}")