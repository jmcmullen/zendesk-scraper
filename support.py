#!/usr/bin/python
import re
import os
import sys
import urllib2
import subprocess
from bs4 import BeautifulSoup

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    articleUrl = getUrl()
    articleSrc = getSrc(articleUrl)
    print 'Searching ' + articleUrl
    brokenImages = getImages(articleUrl, articleSrc)
    print 'Downloading ' + str(len(brokenImages)) + ' images...'
    saveImages(brokenImages)
    print 'Downloading complete!'
    setClipboard(getNewSrc(articleSrc))
    print 'New source copied!'

def getUrl():
    return sys.argv[1] if len(sys.argv) == 2 else raw_input('Enter URL: ')

def getSrc(articleUrl):
    return BeautifulSoup(urllib2.urlopen(articleUrl));

def getImages(articleUrl, articleSrc):
    return articleSrc.findAll('img', src = re.compile('support.one-education.org'))

def saveImages(brokenImages):
    for image in brokenImages:
        imageUrl = image['src']
        imageUrl = imageUrl.replace('support.one-education.org', 'oneedu.zendesk.com')
        fileName = getFileName(imageUrl)
        downloadFile(imageUrl, fileName)

def getFileName(imageUrl):
    return imageUrl[imageUrl.rfind('/'):]

def downloadFile(imageUrl, fileName):
    imageData = urllib2.urlopen(imageUrl).read()
    imageOutput = open(os.getcwd() + '/output' + fileName, 'wb')
    imageOutput.write(imageData)
    imageOutput.close()

def getNewSrc(articleSrc):
    articleSrc = articleSrc.find('article')
    articleSrc = re.sub('support.one-education.org([^<>\"]*[\\\/])', 'one-education.org/support-assets/', str(articleSrc))
    return articleSrc

def setClipboard(articleSrc):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(articleSrc.encode('utf-8', 'ignore'))

main()
