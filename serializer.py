import numpy as np
from PIL import Image
from io import BytesIO

import requests

class crlImg: # give image url, get array for image
    def __init__(self,url,size=(1000,1500)) -> None:
        self.size = size
        self.path = BytesIO(requests.get(url))
        self.imgToArray(self.path,self.size)
    def imgToArray(self,path: str,newSize: tuple):
        img = Image.open(path)
        img.resize(newSize)
        self.array = np.asarray(img)
        del(img)
    def arrayToImg(self):
        return Image.fromarray(self.array)
    def show(self):
        Image.open(self.path).show()
    def save(self,path):
        Image.open(self.path).save(path)

# if __name__ == "__main__":
#     imgPath = 'demoIMG/2 (1).jpg'

