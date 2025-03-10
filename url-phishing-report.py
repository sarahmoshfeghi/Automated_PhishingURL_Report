
from PSHDB import PSHDB
from phish_tank import Phish_Tank
from open_phish import Open_phish
from mail_send import send_mail

def urlphishingreport():
    urls = []
    phish_db = PSHDB.phishingdb()
    phish_t = Phish_Tank.phishtank()
    open_sh = Open_phish.open_phish()
    full = sorted(phish_db + phish_t + open_sh)
    with open('full.txt', 'r', encoding='utf8') as f:
        full_phishing = [line.strip() for line in f]
    dbfile = open('full.txt', 'a')
    with open('P_L.txt', 'w', encoding='utf8') as nf:
        for item in full:
            if item in full_phishing:
                continue
            nf.write(item.strip()+'\n')
            dbfile.write(item.strip()+'\n')
            urls.append(item.strip())
    send_mail("test@test.com", "test@test.com","URL_Phishing")
   # return urls
if __name__ == '__main__':
    urlphishingreport()
