import re
import json

class Professor(object):
    def __init__(self,html,regexps):
        self.get_info(html,regexps)

    def __repr__(self):
        result = 'Name: %s\nSecond name: %s\nSurname: %s\nLink: %s\nPhones: %s\nEmail: %s\nPosition: %s\nInterests: %s\n'
        return result % (self.name, self.secondname, self.surname, self.link, str(self.phones), self.email, str(self.position), str(self.interests))

    def get_info(self,html,regexps):
        self.phones = self.get_phones(html,regexps['phones'],regexps['onephone'])
        self.email = self.get_email(html,regexps['email'])
        self.link = self.get_link(html,regexps['link'])
        self.name,self.secondname,self.surname = self.get_name(html,regexps['fullname'])
        self.position = self.get_position(html,regexps['fullposition'],regexps['positions'],regexps['job'],regexps['tosplit'],regexps['deletetags'])
        self.interests = self.get_interests(html,regexps['interests'])

    def get_phones(self,prof,phones,onephone):
        allphones = phones.findall(prof)
        if not allphones:
            return []
        else:
            return onephone.findall(allphones[0])

    def get_email(self,prof,emailre):
        email = emailre.findall(prof)
        if email:
            return ''.join(json.loads(email[0].replace('"-at-"','"@"')))
        else:
            return ''

    def get_link(self,prof,linkre):
        link = 'https://www.hse.ru'+linkre.findall(prof)[0]
        return link

    def get_name(self,prof,namere):
        fullname = namere.findall(prof)[0].split()
        name = fullname[1]
        surname = fullname[0]
        if len(fullname) == 3:
            secondname = fullname[2]
        else:
            secondname = ''
        return name,secondname,surname

    def get_position(self,prof,fullposre,posre,jobre,splitre,tagre):
        fullposition = fullposre.findall(prof)[0]
        positiondict = {}
        positions = posre.findall(fullposition)
        for position in positions:
            job = jobre.findall(position)[0].strip()
            places = re.findall(job+'\:?(.*?)</span>',position,flags=re.DOTALL)
            if not places:
                positiondict[job] = ''
            else:
                places = splitre.split(places[0])
                places = [tagre.sub('',x).strip() for x in places]
                positiondict[job] = ', '.join(places)
        return positiondict

    def get_interests(self,prof,interestsre):
        interests = interestsre.findall(prof)
        return interests


def get_profs(page):
    regexps = {'phones': re.compile('<div class="l-extra small">.*?</div>',flags=re.DOTALL),
               'onephone': re.compile('<span>(.*?)</span>'),
               'email': re.compile('<a class="link" data-at=\'(.*?)\'>'),
               'link': re.compile('<div class="content__inner content__inner_foot1">.*?<a href="((?:(?:/org/persons/)|(?:/staff/)).*?)"',flags=re.DOTALL),
               'fullname': re.compile('<div class="g-pic person-avatar-small2" title="(.*?)"'),
               'fullposition': re.compile('<p class="with-indent7">.*?</p>',flags=re.DOTALL),
               'positions': re.compile('<span>.*?</span>',flags=re.DOTALL),
               'job': re.compile('<span>(.*?)[:<]',flags=re.DOTALL),
               'tosplit': re.compile('\s+/\s+'),
               'deletetags': re.compile('<.*?>'),
               'interests': re.compile('<a class="tag".*?>(.*?)</a>')}
    regprofs = re.findall('<div class="post person">(.*?)</div>\n\n',page,flags=re.DOTALL)
    profs = []
    for prof in regprofs:
        clprof = Professor(prof,regexps)
        profs.append(clprof)
        #печатает карточки всех преподавателей
        #print(clprof)
    return profs
        

profpage = open('e-profs.html','r',encoding='utf-8').read()
profs = get_profs(profpage)
