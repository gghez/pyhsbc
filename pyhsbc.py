__author__ = 'gregoryghez'

import re

import bs4
import mechanize


def read_accounts(user_id, memo_answer, secure_key):
    br = mechanize.Browser()
    br.open('https://www.hsbc.fr/1/2/hsbc-france/particuliers/connexion')
    br.select_form(nr=1)
    br['userID1'] = user_id
    br.select_form(nr=2)
    resp = br.submit()
    print (resp.geturl())
    #print resp.info()

    br.select_form(nr=0)
    br['userid'] = user_id
    resp = br.submit()
    print (resp.geturl())
    #print resp.info()

    br.select_form(nr=0)
    br['memorableAnswer'] = memo_answer
    br['idv_OtpCredential'] = secure_key

    resp = br.submit()
    print (resp.geturl())
    #print resp.info()

    br.select_form(name='form1')
    resp = br.submit()
    print (resp.geturl())
    #print resp.info()
    frame_container = resp.read()
    m = re.search('<frame name="FrameWork" src="(.+?)"', frame_container)
    navigate_url = 'https://client.hsbc.fr%s' % m.group(1)
    resp = br.open(navigate_url)
    print (resp.geturl())
    #print resp.info()
    html = resp.read()
    soup = bs4.BeautifulSoup(html)
    #print soup.prettify()
    accounts = []
    for td_amount in soup.find_all('td', attrs={'class': 'last alignR'}):
        td_account_num = td_amount.find_previous_sibling('td')
        td_account_name = td_account_num.find_previous_sibling('td')
        accounts.append((td_account_num.string, td_account_name.string, td_amount.string))
    return accounts

if __name__ == '__main__':
    import sys

    user_id = sys.argv[1]
    memo_answer = sys.argv[2]
    secure_key = sys.argv[3]

    for (num, name, amount) in read_accounts(user_id, memo_answer, secure_key):
        print '%s%s%s' % (num.ljust(30), name.ljust(30), amount.rjust(10))