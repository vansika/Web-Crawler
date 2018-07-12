# Web-Crawler

A web Crawler in Python that crawls the world wide web starting with a given url as a seed upto the specified depth and retrieves pdf files which are converted to text documents with proper formatting and minimum loss of data. 

## Input : 
        1. seed URL
        2. Path to directory where pdf and text fils should be saved

## Limitations: 

Complex pdfs which include non trivial text fonts and images would not be converted efficiently into text format.
Redundant formation of pdf due to multiple links mapping to same URI happens.
Since the entire script is running in single thread, its slow down the process.
Unnecessary data or noise in the pdfs.


