from ast import Try
from numpy import alltrue
import requests as reqs
from bs4 import BeautifulSoup as bs


def getHtml(link:str,verb: bool):
    raw = reqs.get(link)
    if raw.status_code == 200:
        if verb:
            print('raw retiveal succesful')
        souped = bs(raw.content, 'html.parser')
        return souped
    else:
        if verb:
            print('raw retieval failed')

def getSauceHtml(id:int,verb: bool):
    link = 'https://nhentai.net/g/'+str(id)+'/'
    print(link)
    return getHtml(link,verb)


class Sauce:
    def __init__(self,id) -> None:
        self.id = id
        
        sHtml = getSauceHtml(id,False) #gives a soupy html
        
        self.title = sHtml.find('h1','title') # finds the title
        
        allTags = sHtml.find_all('div','tag-container field-name') #makes a list of the each of the tag sections
        for sect in allTags: # checks each found tag container for type then stores as such
            if str(sect)[47:55] == 'Parodies':
                self.parodies = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:57] == 'Characters':
                self.characters = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:52] == 'Tags':
                self.tags = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:54] == 'Artists':
                self.artists = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:53] == 'Groups':
                self.groups = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:56] == 'Languages':
                self.languages = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:57] == 'Categories':
                self.categories = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:52] == 'Pages':
                self.pages = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:55] == 'Uploaded':
                self.time = sect.find('time')
    
    def textExt(self,spans:list): # cycles through list extracting the text from each entry
        outList = []
        for span in spans:
            outList.append(str(span).split('>')[1].split('<')[0])
        return outList
    def timeExt(self,time): # same thing as before except now we are extracting the time attrubute, not the text
        return str(time).split('e="')[1].split('"')[0]        
                
                
# print(getSauceHtml(399458,True).find_all('div','tag-container field-name')[8].find('time'))
