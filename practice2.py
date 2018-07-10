
import requests
import os
from lxml import html
from PyPDF2 import PdfFileReader
from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed

pdf = []

webpage = raw_input("Enter the seed page: ")
path = raw_input("Enter path to download pdfs: ")


reload(sys)
sys.setdefaultencoding('utf8')         #to ensure unicode encoding

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages: 
        pagenums = set()      #checks the page numbers 
    else:
        pagenums = set(pages)

    output = StringIO()       #creates a string object 
    manager = PDFResourceManager() 
    converter = TextConverter(manager, output, laparams=LAParams()) 
    interpreter = PDFPageInterpreter(manager, converter)     #object to process page contents

    infile = file(fname, 'rb')     #read the pdfs
    #process the pdfs
    #raise exception if text is not extractable
    try:
        for page in PDFPage.get_pages(infile, pagenums): 
            interpreter.process_page(page)
    except PDFTextExtractionNotAllowed:
        print fname + " : " + 'This pdf won\'t allow text extraction!'

    #close the objects

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

    #converts all pdfs in specified directory, saves all resulting txt files to the same directory
def convertMultiple(pdfDir, txtDir):
    for pdf in os.listdir(pdfDir):     #iterate through pdfs in pdf directory
        fileExt = pdf.split(".")[-1]    #check for .pdf extension
        if fileExt == "pdf" or fileExt == 'PDF':
            pdfFilename = pdfDir + pdf 
            text = convert(pdfFilename)     #get string of text content of pdf
            textFilename = txtDir + pdf + ".txt"
            textFile = open(textFilename, "w")     #make text file
            textFile.write(text)     #write text to text file
            newname =  txtDir + pdf + ".converted" + ".txt"
            with open(textFilename) as f:
                with open(newname, 'w') as w:
                    count = 0
                    for line in f:
                        if line == '\n':
                            count = count + 1
                        else:
                            if count > 0:
                                w.write('\n')
                            line = line.replace('\n','')
                            w.write(line)
                            count = 0
    
def download_pdf(url):
	r = requests.get(url, stream = True)    #fetch pdf
	if r.status_code == 200: #check for status
		with open(path + os.path.basename(url), 'wb') as pdf: 
			for chunk in r.iter_content(chunk_size=1024):  #download large pdf files in chuunks
				if chunk:
					pdf.write(chunk)
	else:
		return       #return if status code other than 200

def get_all_links(url):    #procedure to retrieve links from specified page
    links = []            #list to store all links within a particular page passed in url
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content) #to parse html documents

        itr = tree.xpath('//a/@href')  #find 'href' in all <a> tags in the document

        for tag in itr:   #iteratee over href's

            if(tag == None):  #check for empty tags
                continue

            if(check_url(tag) == False):    #check for extensions other than html (.jpg, .zip, etc.)
                continue

            if(check_url(tag) == 'pdf'):
            	pdf.append(tag)
                download_pdf(tag)

            else:
                links.append(tag)      #create list of links
        return links

    except Exception as E:
        return E


def merge(a, b):     #procedure to create list of pages to be crawled to reach the next depth
    for i in b:  
        if i not in a:
            a.append(i)


def check_url(link):     #procedure to check for pdf's and other extensions
    if link and (link[0] != 'h'):
        return False
    if link and (link.find('.jpeg') != -1):
        return False
    if link and (link.find('.zip') != -1):
        return False
    if link and (link.find('.png') != -1):
        return False
    if link and (link.find('.jpg') != -1):
        return False
    if(link.find('.pdf') != -1 or link.find('.PDF') != -1):
        return 'pdf'


def crawl_web(seed):
    tocrawl = [seed]   #list containing pages that need to be crawled                    
    crawled = []       #list containing pages that have been crawled
    depth_list = []   #list of pages at a particular depth
    depth = 0 
    print 'Running...'    
    while tocrawl and depth <= 3:
        page = tocrawl.pop()        #to get the seed page
        if page not in crawled:     #to prevent looping 
            crawled.append(page) 
            new_links = get_all_links(page)   #get links for page that has not been crawled
            merge(depth_list, new_links) 

        if not tocrawl:      #if tocrawl list is empty, update tocreate with depth_list
            tocrawl, depth_list = depth_list, []
            depth = depth + 1

    files = os.listdir(path)   #make list of all files in the specified directory
    for i in files:
    	xpath = os.path.join(path,i) #create absolute path
    	if xpath.endswith(".pdf") or xpath.endswith(".PDF"): #check for pdf files
    		try:
    			doc = PdfFileReader(open(xpath, "rb")) 
    		except:
    			os.remove(xpath) #remove the files from the directory if format other than pdf

    convertMultiple(path, path) #function to convert pdf's to text

crawl_web(webpage)