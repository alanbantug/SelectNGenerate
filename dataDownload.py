#! python

import requests
import re
import os
import shutil

from bs4 import BeautifulSoup

class dataDownload(object):

    def __init__(self, baseUrl, saveName):

        self.base_url = baseUrl

        fileObject = self.getFileLocation(baseUrl)
        self.writeToFile(saveName, fileObject)

    def getFileLocation(self, baseUrl):

        ''' This function will parse the CALottery website and get the location of the winning numbers
        '''

        r = requests.get(baseUrl)

        soup = BeautifulSoup(r.text, 'html.parser')

        links = []

        for link in soup.find_all('a'):

            link_url = link.get('href')

            if link_url != None and link_url.find('download-numbers') > 0:
                links.append(link_url)

        dataLocation = "http://www.calottery.com/" + links[0]

        fileObject = requests.get(dataLocation, stream=True)

        return fileObject

    def writeToFile(self, saveName, fileObject):

        ''' This function will convert data from the downloaded file into text and write it to name provided
        '''
        
        with open(saveName, 'w') as o_file:

            for d_line in fileObject.iter_lines():

                d_line_decode = d_line.decode("utf-8")

                o_file.write(d_line_decode)
                o_file.write('\n')

        o_file.close()
