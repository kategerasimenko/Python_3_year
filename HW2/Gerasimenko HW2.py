import json
from lxml import etree, html
import urllib.request

class Professor(object):
    def __init__(self,html,lxmltype):
        if lxmltype == 'etree':
            self.get_info_etree(html)
        if lxmltype == 'xpath':
            self.get_info_xpath(html)

    def __repr__(self):
        result = 'Name: %s\nSecond name: %s\nSurname: %s\nLink: %s\nPhones: %s\nEmail: %s\nPosition: %s\nInterests: %s\n'
        return result % (self.name, self.secondname, self.surname, self.link, str(self.phones), self.email, str(self.position), str(self.interests))

       
    def get_name(self,fullname):
        fullname = fullname.split()
        name = fullname[1]
        surname = fullname[0]
        if len(fullname) == 3:
            secondname = fullname[2]
        else:
            secondname = ''
        return name,secondname,surname

    
    def get_info_etree(self,prof):
        #phones and email
        self.phones = []
        self.email = ''
        phones = prof[0][0]
        if phones.get('class') == 'l-extra small':
            for phone in phones:
                if phone.tag == 'span':
                    self.phones.append(phone.text)
                elif phone.tag == 'a':
                    self.email = ''.join(json.loads(phone.attrib['data-at'].replace('"-at-"','"@"')))
            link = prof[0][1][0][0]
            positions = prof[0][1][0][1]
    
        elif phones.get('class') == 'main content small':
            link = prof[0][0][0][0]
            positions = prof[0][0][0][1]
             
        #link
        self.link = 'https://www.hse.ru'+link.get('href')

        #fullname
        fullname = link[0].get('title')
        self.name,self.secondname,self.surname = self.get_name(fullname)
        
        #position
        self.position = {}
        for position in positions:
            if position.tag == 'span':
                job = position.text.strip().strip(':')
                departments = []
                if '\t' in job:
                    a = [x.strip() for x in job.split('\t') if x and x != '\n']
                    if a[0].endswith(':'):
                        job = a[0].strip(':')
                    else:
                        job = ''
                    departments.append(a[-1])
                for department in position:
                    departments.append(department.text)
                    textdep = department.tail.strip()
                    if textdep and textdep != '/':
                        departments.append(textdep[1:].strip())
                self.position[job] = departments

        #interests
        self.interests = []
        try:
            interests = prof[0][1][0][2]
            for interest in interests:
                self.interests.append(interest.text)
        except:
            pass


    def get_info_xpath(self,prof):
        self.phones = prof.xpath('.//div[@class="l-extra small"]/span/text()')
        self.email = prof.xpath('string(.//*[@data-at]/@data-at)')
        if self.email:
            self.email = ''.join(json.loads(self.email.replace('"-at-"','"@"')))
        self.link = 'https://www.hse.ru'+prof.xpath('string(.//*[@class="link link_dark large b"]/@href)')
        fullname = prof.xpath('string(.//div[@class="g-pic person-avatar-small2"]/@title)')
        self.name,self.secondname,self.surname = self.get_name(fullname)
        positions = prof.xpath('.//p[@class="with-indent7"]/span')
        self.position = {}
        for position in positions:
            departments = position.xpath('./a/text()')
            alljobs = [x.strip() for x in position.xpath('./text()') if x.strip() and x.strip() != '/']
            job = alljobs[0].strip(':')
            if len(alljobs) > 1:
                departments += [x[1:].strip() for x in alljobs[1:]]
            if '\t' in job:
                a = [x.strip() for x in job.split('\t') if x and x != '\n']
                departments.append(a[-1])
                if a[0].endswith(':'):
                    job = a[0].strip(':')
                else:
                    job = ''
            self.position[job] = departments
        self.interests = prof.xpath('.//a[@class="tag"]/text()')
        

def teachers_with_etree(page):
    tree = etree.HTML(page)
    profs = []
    treeprofs = tree[1][1][3][2][1][0][2][1]
    for prof in treeprofs:
        clprof = Professor(prof,'etree')
        profs.append(clprof)
        #печатает карточки всех преподавателей
        #print(clprof)
    return profs
                    
def teachers_with_xpath(page):
    tree = html.fromstring(page)
    profs = []
    xpathprofs = tree.xpath('//div[@class="post person"]')
    for prof in xpathprofs:
        clprof = Professor(prof,'xpath')
        profs.append(clprof)
        #печатает карточки всех преподавателей
        #print(clprof)
    return profs
        

profpage = open('e-profs.html','r',encoding='utf-8').read()
a = input('etree or xpath? ')
if a.lower() == 'etree':
    teachers_with_etree(profpage)
elif a.lower() == 'xpath':
    teachers_with_xpath(profpage)
