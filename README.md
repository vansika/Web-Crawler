#Web-Crawler

A web Crawler in Python that crawls the world wide web starting with a given url as a seed upto the specified depth and retrieves pdf files which are converted to text documents with proper formatting and minimum loss of data. 

##Input : 1. seed URL
        2. Path to directory where pdf and text fils should be saved
        
##Tools :

Requests library has been used to send HTTP requests to access the web pages
HTML utility of LXML package has been used to parse web pages
XPath utility of LXML package of Python has been used to extract href text (urls) from anchor tags.
Python’s OS module ( provides operating system functionality) has been used to save pdf files with appropriate extensions 
Requests library has been used to send HTTP requests to access the pdf files
HTTP response content (string that stores file data) has been used to download pdfs files
PyPDF module has been used to remove downloaded files that are not .pdf/.PDF
PDFMiner, an extensible pdf parser, has been used to extract information from pdf files and store in text files
Sys module has been used to switch from default ASCII to other encodings (such as UTF - 8)
StringIO module has been used to create a buffer object to hold pdf information for processing
OS module has been used to access downloaded pdf files from local directory
Formatting of text files has been done using inbuilt Python functions

##Limitations: 

Complex pdfs which include non trivial text fonts and images would not be converted efficiently into text format.
Redundant formation of pdf due to multiple links mapping to same URI happens.
Since the entire script is running in single thread, its slow down the process.
Unnecessary data or noise in the pdfs.


