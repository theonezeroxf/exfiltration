import smtplib
import time

smtp_server='smtp.163.com'
smtp_port=465
smtp_acct='18063436642@163.com'
smtp_password='AXDYBCNNCSUSGXTU'
# smtp_password='XFblackzero9810'
tgt_accts=['1480210287@qq.com']
def plain_email(subject,contents):
    message=f'Subject: {subject}\nFrom {smtp_acct}\n'
    message+=f'To: {tgt_accts}\n\n{contents}'
    server=smtplib.SMTP_SSL(smtp_server,smtp_port)
    # server.set_debuglevel(1)
    # server.starttls()
    # server.ehlo()
    server.login(smtp_acct,smtp_password)
    
    server.sendmail(smtp_acct,tgt_accts,message)
    time.sleep(1)
    server.quit()

if __name__=='__main__':
    plain_email('introduction','hello, I am zero,can you give me source code.')
    print('[*] email send success')