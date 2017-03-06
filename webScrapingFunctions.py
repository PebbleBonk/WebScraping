'''
Created on 4.2.2016

@author: t_ollrii
'''
import re

''' Functions for scraping information off Wikipedia
    ************************************************
    These functions were made to scrape information 
    off wikipedia to ease the workflow of bigger
    excels. First function searches the html-code
    of the wanted page for tags and information
    under them, whereas the second one searches 
    for wanted keywords from the whole page.
    
'''

''' ===================== Information from html webpage =================== '''

def searchForCompanyInfo(soup, wantedInfo):
    ''' 
    This function searches for information given in parameter
    'wantedInfo' from the webpage, given as a BeautifulSoup object
    in parameter 'soup'. Function uses regular expressions to extract
    the data from the html code for maximum efficiency & precision.
    
    .. note::
        It would be interesting to put some timers within this module
        to find out how much different parts of the code differ in
        their respective runtimes...
        
    :param  soup: The html parsed webpage where the information is
            searched from.
    :type   soup: :mod:`BeautifulSoup4` object
    :param  wantedInfo: A list of strings that the function will try
            to find from the given soup.
    :type   wantedInfo: list of str

    :returns: A list of strings, found under the html tag(s) given
            in parameter 'wantedInfo'
            
    .. todo:: Errors:  Raising errors on different occasions. E.g. empty 
            lists, undefined character etc.
    .. todo:: Encoding:  Handle site encoding better. At the moment there 
            are some difficulties with special characters, such as "&".
    '''
    
    infoData = []
    resultData = []
    infoStr = ""
    for i in soup.find_all(text=wantedInfo):
        p = re.compile('>[^<>].[^<>]*<')
        r = p.findall(str(i.parent.parent))
        
        for x in r:
            x = x.replace(">", "").replace("<", "")
            if not x.isspace() and x != wantedInfo:
                infoStr = ','.join([infoStr, x])
        infoData = infoStr.split(",")

    for i in infoData:
        i = i.replace("\n", "").replace("&amp;", "&")\
             .replace(";", ":").replace(",", "")
        if not i.isspace() and i!="":
            resultData.append(i)
    return resultData


''' ========================= KeyWords from html webpage ==================='''
def searchForKeyWords(soup, keyWordList):
    ''' This function searches for keywords given in parameter
    'keyWordList' from the webpage, given as a BeautifulSoup object
    in parameter 'soup'. Function uses regular expressions to find
    the words from the html code for maximum efficiency & precision.
    
    .. note::
        Keywords should be written in their **depricated** form
        as then also their conjugated forms will be found.
        
    :param  soup: The html parsed webpage where the information is
            searched from.
    :type   soup: BeautifulSoup4 object
    :param  keyWordList: A list of strings that the function will
            look for in the page given in parameter 'soup'
    :type   keyWordList: A list of str
    
    :returns: The list of found key words that were found from the
            document as a list of strings.
    '''
    
    foundKeyWords = []
    for kWord in keyWordList:
        if soup.find(text=re.compile(kWord)) != None:
            foundKeyWords.append(kWord.strip())
    return foundKeyWords





