# Map Metadata Extraction

This repository is a proof of concept of (most of the steps of) extracting catalog-like
data from physical print books into a spreadsheet. 

The key concept is that when a catalog-like text has consistent punctuation demarking
different types of information (in this example, dates vs cities vs map identifiers), 
it is possible to pull out the data and completely reformat it. 

For more information about the project, see both the Methods section below and [this series
of blog posts that I wrote.](https://erinwatson.people.sites.carleton.edu/from-history-book-index-to-digital-database/)
The blog posts give the context and story of the whole project while the Methods section
here focuses on the technical process.

Note: The code in this repository is _not_ particularly helpful for extracting data from 
a print document that is already arranged in a table. Other tools for that purpose exist.

# Methods

Using a very nice scanner at Carleton College's Gould Library, I scanned two different 
indexes from Robert W. Karrow's book, _Mapmakers of the Sixteenth Century and Their Maps_. 
For a full citation of the pages, see the License to this repository.
Then, using Adobe Acrobat, I applied OCR to the PDFs, which made the text highlightable.

I copied the text out of the PDFs into the two files that live in the `raw-ocr-text` 
folder in this repository. Then, because each of these files are relatively short 
(3-4 pages in the physical book), I went through and fixed some of the formatting
so that key pieces like country names would be easier to locate with Python string 
pattern matching, as well as correcting glaring typos.

To get the data out of the text files and into tables, I took advantage of Karrow's 
clear and meticulous punctuation that helps mark out the nested structure of the data. 
For example, in the Index to Place and Date, each country (marked with an extra newline) 
has multiple cities (each preceded by a dash). Each city has information for multiple 
years (separated by semicolons). Each year has multiple map IDs (separated by commas). 
Finally, each map ID has two components, an identifier for the mapmakers and an identifier 
for the specific map (separated by a slash). 

I used Python's built in string methods and a few tools from the regular expressions 
library to do the pattern matching. Finally, I organized all of the data into a 
Pandas dataframe for easy exporting.

In the near term, I hope to combine the information from each index, along with 
the Table of Contents that gives a name to each mapmaker identifier, to create
one large table with all the extractable information about each map. 

This table could then be used for data visualizations to explore questions
about the scale and scope of mapmaking in the sixteenth century. 

