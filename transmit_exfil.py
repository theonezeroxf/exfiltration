import ftplib
import os
import socket
def plain_ftp(docpath,server='117.78.11.71'):
    ftp=ftplib.FTP(server)
    ftp.login("root","xfblackzero9810")
    ftp.cwd("/root/")
    ftp.storbinary('STOR '+os.path.basename(docpath),open(docpath,"rb"),1024)
    ftp.quit()
if __name__=="__main__":
    plain_ftp('./key.pub')