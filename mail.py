import imaplib
import email
from bs4 import BeautifulSoup


#credentials
user_email='austinandogola@gmail.com'
password='fbryihgleqxvzapx'

imap_server='imap.gmail.com'
imap=imaplib.IMAP4_SSL(imap_server)

imap.login(user_email,password)

status,messages=imap.select('INBOX')
messages=int(messages[0])

n=15

def clean(text):
    # clean text for creating a folder
    return "".join(c for c in text if c.isalnum() )


    

def filterEmail():
    codes=[]
    for i in range(messages,messages-n,-1):

        #fetch email by id
        res,msg=imap.fetch(str(i), '(RFC822)')

        for response in msg:
            if isinstance(response, tuple):

                #parse bytes into a message object
                msg=email.message_from_bytes(response[1])

                #print(msg['From'])
                if('Namecheap' in msg['From'] and 'confirmation' in msg['Subject']):

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()

                            try:
                                #get email body
                                body=part.get_payload(decode=True).decode()
                                clean_body=clean(body)
                                soup=BeautifulSoup(body,'lxml')
                                # print(soup.encode('utf-8'))
                                for td in soup.find_all('td',{'data-ncid':"code"}):
                                    codes.append(clean(td.text))
                            except:
                                pass



                    else:
                        content_type = msg.get_content_type()

                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        clean_body=clean(body)
                        soup=BeautifulSoup(body,'lxml')
                        # print(soup.encode("utf-8"))
                        for td in soup.find_all('td',{'data-ncid':"code"}):
                            codes.append(clean(td.text))
    return codes
    


def createFile():
    f=open('myemails.txt','a')
    f.write(body)
    breaks=['-' for i in range(500)]
    breaks_string=''.join(str(i) for i in breaks)
    f.write(breaks_string)
    f.close()



the_codes=filterEmail()

for code in the_codes:
    print(code)


