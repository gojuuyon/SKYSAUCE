import pickle
import requests as reqs
from bs4 import BeautifulSoup as bs


def getHtml(link:str,verb: bool): 
        #get HTML of given page
        raw = reqs.get(link) 
        if raw.status_code == 200: #check if retrival was successful
            if verb:
                print('raw retiveal succesful')
            souped = bs(raw.content, 'html.parser') # parse html
            return souped
        else:
            if verb:
                print('raw retieval failed')


class Sauce:
    # when given a 6 digit, get info and images
    def __init__(self,id) -> None:
        # init
        self.id = id
        sHtml = self.getSauceHtml(id,False) #gives a soupy html
        self.title = self.textExt(sHtml.find('h1','title').find_all(class_='pretty')) # finds the title
        
        
        allTags = sHtml.find_all('div','tag-container field-name') #makes a list of the each of the tag sections
        for sect in allTags: # checks each found tag container for type then stores as such
            if str(sect)[47:55] == 'Parodies':
                self.parodies = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:57] == 'Characters':
                self.characters = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:51] == 'Tags':
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
                self.pagec = self.textExt(sect.find_all('span',class_='name'))
            elif str(sect)[47:55] == 'Uploaded':
                self.time = self.timeExt((sect.find('time')))
        
        
        # make list of image links
        allImages = sHtml.find_all(class_="lazyload")
        self.pages = []
        for n,image in enumerate(allImages):
            if n == 0:
                self.cover = str(image).split('c="')[1].split('"')[0]
            else:
                self.pages.append(str(image).split('c="')[1].split('"')[0].replace('t.','.'))
        
          
    def textExt(self,spans:list): 
        # cycles through list extracting the text from each entry
        outList = []
        for span in spans:
            outList.append(str(span).split('>')[1].split('<')[0])
        return outList
    

    def timeExt(self,time): 
        # cycles through list extracting the time attrubute, not the text
        return str(time).split('e="')[1].split('"')[0]
    
    
    def getSauceHtml(self,id:int,verb: bool): 
        # get the HTML of a given id
        link = 'https://nhentai.net/g/'+str(id)+'/'
        # print(link)
        return getHtml(link,verb)



class masterIndices: 
    # the master index for all of the tags for ease of serialization (EX: an artist has is converted to a number)
    def __init__(self) -> None:
        self.jsonPaths = {
            'artist':'https://nhentai.net/artists/',
            'tag':'https://nhentai.net/tags/',
            'group':'https://nhentai.net/characters/',
            'characters':'https://nhentai.net/characters/',
            'parodies':'https://nhentai.net/parodies/'
        }
        self.tables = {}   
    
                
    def getPageCnt(self,path): 
        #get page count from one of the tag pages
        shtml = self.getHtml(path,False) # saves the soupy html
        unpPages = shtml.find('a',class_='last').prettify() #gets chunk of html for the to end button
        return int(unpPages.split('page=')[1].split('">')[0])


    def getTags(self,path):
        shtml = self.getHtml(path,False)
        tLst = shtml.find_all('span',class_='name')
        outLst = []
        for span in tLst:
            outLst.append(str(span).split('>')[1].split('<')[0])
        return outLst


    def getAllTags(self,key):
        # print(key)
            path = self.jsonPaths[key]
            pageC = self.getPageCnt(path)
            tLst = []
            for n in range(pageC):
                tempPath = path + f'?page={n+1}'
                tLst.append(self.getTags(tempPath))
            self.tables[key] = tLst


    def regen(self,*kwarg):    
        if kwarg == ():
            for key in list(self.jsonPaths.keys()):
                self.getAllTags(key)
        else:
            try:
                self.getAllTags(kwarg[0])
            except:
                pass #invalid key


    def save(self,filename):
        with open(f'{filename}.pkl','w') as outp:
            pickle.dump(self.tables,outp,pickle.HIGHEST_PROTOCOL)


    def load(self,path):
        with open(f'{path}','rb') as outp:
            self.tables = pickle.load(outp)
                
                
                
                

mI = masterIndices()
               

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
# print(getSauceHtml(399458,True).find_all('div','tag-container field-name')[2])
# gex = Sauce(399458)