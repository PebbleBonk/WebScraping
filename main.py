'''
Created on 4.2.2016
@author: t_ollrii
'''
from time import localtime, strftime, time
from simpleProgressBar import progressBar
from tkinter import filedialog
from bs4 import BeautifulSoup
from os import path

import webScrapingFunctions as wsf
import wikipedia as wiki
import warnings


''' ======================= Function for saving a file ====================='''
def companyInfoFromCSV(companyListFile, keyWordList, infoList, saveName=None):
    ''' 
    A function for scraping information off wikipedia pages.
    Made for checking information about different companies 
    but should be easily transformed to check other kind of
    information as well. Saves the information in .csv file
    using unicode-32 encoding.
        
    .. note::
        The Microsoft Excel doesn't recognize the utf-32 encoding
        in the same way it recognizes, for example, utf-8 or ANSI
        encoded .csv files. Thus the .csv file has to be imported
        manually to excel through Data -> Import -> From text
    
    :param  companyListFile: a path to a .csv -file that contains the list
            of companies the function goes through and finds information about.
    :param  keyWordList: Key Word List. A _list_ of containing the keywords as
            _strings_ that the function 'searchForKeyWords()' will look for.
    :param  infoList: Company Information List. A _list_ containing the kinds of
            information, e.g. "industry" or "Services" as _strings_ that the
            function 'searchForCompanyInfo()' will look for. 
    :param  saveName: The name of the file where the results will be saved
            and the path to the file as a @string. If parameter is omitted,
            the path of companyListFile is used instead. Name of the save
            will be the name of the companyListFile appended with "_results" 

    .. todo::   Change naming so that the function works for
                scraping all kinds of information from Wikipedia.
    .. todo::   Define a return value showing how well the 
                values given were found, how long it took etc....
    .. todo::   Implement a log file for errors, warnings
                and random statistics for later inspection.
    .. todo::   Figure out how to save the information with
                proper text encoding. The current one doesn't work with
                excel automatically but has to be encoded again using
                for example Notepad. (save as -> encoding: Unicode/ANSI)
    .. todo::   Add a number utilizing the matchingAlgortihm() to value
                how well the found wikipedia page matches with the 
                original one. This to ease the process of going through 
                the excel sheet.
    '''
    # open the log file to write a log about the program's running to
    # Go to the end of the file and write information about the session
    # starting.
    path.relpath(__file__)
    logFile = open(path.dirname(\
                   ''.join([path.dirname(__file__), "\\logfile.plg"]) ), 'a')

    logFile.write("\n")
    logFile.write(''.join(["Starting session on",\
                           strftime("%Y-%m-%d %H:%M:%S", localtime()),\
                           "With companyList:", companyListFile, \
                           "\nID: ", strftime("%Y%m%d%H%M%S", localtime()), 
                           "\nSettings: KeyWords:", str(keyWordList), 
                           "; infos:", str(infoList), 
                           "; save file:", str(saveName), "\n" ]))
    
    # If the save file's name is not given in the parameters,
    # ask for it with a file dialogue (slower, but more control)
    if saveName == None:
        savefile = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
        
    # If set to AUTO, just add '_Result' to end of the filename
    # to create the path for saving the results. Piece of cake.
    elif saveName == "AUTO":
        filename = path.basename(companyListFile)
        savefilename = ''.join([path.dirname(companyListFile),\
                                '\\', path.splitext(filename)[0],\
                                "_Results.csv"])
        savefile = open(savefilename, 'w', encoding='utf-32')
    else:
        savefile = open(saveName,'w', encoding='utf-32')
    
    # Write the first row to the save file (categories/headers)
    savefile.write(';'.join(["Company;Found Wiki page"]+infoList+["KeyWords\n"]))
    
    # Count the size of the file to initiate the progress bar
    lineCountTotal = len(open(companyListFile,'r',encoding='utf8').readlines())
    
    print("Total amount of companies to go through:", lineCountTotal)
    logFile.write("Total amount of companies to go through:", lineCountTotal)
    
    # Open the file containing the company names
    with open(companyListFile, 'r', encoding="utf8") as csvFile:
    
        start_time = time()
        lineNo = -1
        missed = 0
        # Go through the companies (the main thing!)
        # a line on the file represents one company
        # thus the naming
        for company in csvFile:
            lineNo = lineNo + 1
            
            # Update the progress bar:
            progressBar(lineNo, lineCountTotal, elapsedTime=(time()-start_time))

            # Searching the company from Wikipedia. Skip the company if 
            # it or close matches are not found (auto_suggest=True):
            savefile.write(''.join(['\n', company.strip(), ';']))
            try:
                wp = wiki.page(company, auto_suggest=True)
                savefile.write(''.join([wp.title, ';']))
            except:
                savefile.write(''.join(['404 not found', ';']))
                missed = missed + 1
                continue
            
            # Create BeautifulSoup for html scraping
            soup = BeautifulSoup(wp.html(), "html.parser")
            
            # If company is found from Wikipedia, search
            # for information about the company and so on.
            for wi in infoList:
                info = wsf.searchForCompanyInfo(soup, wi)
                savefile.write(', '.join(info))
                savefile.write(';')
                
            # Also search for the keywords given in parameters. 
            # Define the industry of the company based on them:               
            foundKeyWords = wsf.searchForKeyWords(soup, keyWordList)
            if len(foundKeyWords) != 0:
                savefile.write(', '.join(foundKeyWords))
                    
    # Close the files and exit the function         
    progressBar(lineCountTotal, lineCountTotal) 
    savefile.close()
    csvFile.close()
    
    print(' -   DONE! With success rate of: {0:.2f}%        ',\
          ((lineCountTotal-missed)/lineCountTotal))
    
    
''' ======================== Main function for testing ====================='''
if __name__== "__main__":
    
    # Ignore the annoying, mystery error of beautifulSoup
    warnings.filterwarnings("ignore", category=UserWarning)
    print("Starting something almost horrible:")
    print("Started at:", strftime("%Y-%m-%d %H:%M:%S", localtime()))
    
    # These could be deleted with small changes in the function above...
    searchIndustryServices = True
    search4KeyWords = True
    
    # keywords and info to scrape from Wikipedia:
    keywordList = ["comminut", "dewater", "flotat", "beneficiat", \
                   "metallurg","concentrat", "tank", "smelt", \
                   "mineral", "processing", "mining", "automation"]
    
    companyInfoList = ["Industry", "Services"]


    # Files to handle:
    companyListFiles = ["..\\AllOfThecompanies.csv"]

    
    for compListFile in companyListFiles:
        
        # Start handling a new file:
        start_time = time()
        print("\nStarting with file:", path.basename(compListFile),\
               "at", strftime("%Y-%m-%d %H:%M:%S", localtime()))
        
        # Do the real magic. For over-night runs a try-except
        # model was implemented. This way miscellaneous crashes
        # will not affect the whole run and log is preserved:
        try:
            companyInfoFromCSV(compListFile, keywordList, \
                               companyInfoList,\
                               saveName="AUTO")
        except Exception as e:
            print("\n", compListFile, "didn't finish properly!:\n", e)
        
        # Print information on how long the executing took.
        # Interesting pieces of information to add here are
        # e.g. the average execute time, average change etc:
        print("Finished with file:", path.basename(compListFile),\
              "at", strftime("%Y-%m-%d %H:%M:%S", localtime()))
        
        hours, rem = divmod((time()-start_time), 3600)
        mins, secs = divmod(rem, 60)
        
        print('{}: {}h {}m {}s'.format("Time spent on file",\
                                       int(hours), int(mins),\
                                       int(secs)))
        
    print("All DONE! Check the results!")
