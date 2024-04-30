#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author  ：sangea
@Date    ：2023/10/21 13:04 
"""
import base64
import logging
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class Mail:
    def __init__(self, mail_host, mail_pass, sender, sender_name):
        # 第三方 SMTP 服务
        self.mail_host = mail_host  # 填写邮箱服务器:这个是qq邮箱服务器，直接使用smtp.qq.com
        self.mail_pass = mail_pass  # 填写在qq邮箱设置中获取的授权码 moanxkttqcuwbfgh --> zstudvkwkgnnbfej
        self.sender = sender  # 填写发送方邮箱地址
        self.sender_name = sender_name

    def send(self, receivers, subject, txt, attach_path=None):
        """
        发送邮件
        :param receivers: 填写收件人的邮箱，QQ邮箱或者其他邮箱，可多个，中间用,隔开
        :param subject:
        :param txt:
        :param attach_path:
        """
        # 构造邮件对象MIMEMultipart
        message = MIMEMultipart('mixed')

        # 主题、发件人、收件人、日期显示在邮件页面上
        message['From'] = Header(f'=?utf-8?B?{base64.b64encode(self.sender_name.encode()).decode()}=?= <{self.sender}>')  # 必须填发送者邮箱
        message['To'] = Header(';'.join(receivers), 'utf-8')  # 邮件接收者姓名
        message['Subject'] = Header(subject, 'utf-8')

        # 构造文字内容
        text_plain = MIMEText(str(txt), 'plain', 'utf-8')
        message.attach(text_plain)

        # 构造图片附件
        # send_image_file = open(r'bizhi.jpg', 'rb').read()  # 打开文件，可以使用相对路劲和绝对路径
        # image = MIMEImage(send_image_file)
        # image.add_header('Content-ID', '<image1>')
        # image["Content-Disposition"] = 'attachment; filename="bizhi.jpg"'
        # msg.attach(image)

        # 构造附件
        if attach_path:
            send_file = open(attach_path, 'rb').read()
            text_att = MIMEText(send_file, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            # 重命名附件文件
            text_att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_path))
            message.attach(text_att)

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 建立smtp连接，qq邮箱必须用ssl边接，因此边接465端口
            smtpObj.login(self.sender, self.mail_pass)  # 登陆
            smtpObj.sendmail(self.sender, receivers, message.as_string())  # 发送
            smtpObj.quit()
            logger.info('邮件发送成功！')
        except smtplib.SMTPException as e:
            logger.error(e.__traceback__.tb_lineno, e)
            logger.info('邮件发送失败！')


if __name__ == '__main__':
    mail = Mail('smtp.qq.com', 'zswdekwrgtnbgej', '802203474@qq.com', 'sangea')
    mail.send(['sangea0606@163.com'], '这是主题', '这是文本内容')
    # mail.send(['sangea0606@163.com'], '这是主题', '这是文本内容', r"E:\data\smt\2023-10-21.xls")
