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

If you want to recreate what I've done with code, here's the rough order. See the commit 
messages for more details if you're stuck.
1. Run `python scripts/extract_place_and_date.py` to turn the cleaned OCR _Index to Place and Date_ into `outputs/index_to_place_and_date_v4.csv`. You should see in the terminal what snippets failed.
2. Run `python scripts/extract_mapmaker_names.py` to turn the cleaned _Table of Contents_ into `outputs/mapmakers.csv`. 
3. Run `python scripts/combine_index_and_names.py` to attach the mapmakers' names to their ID in the Index. This creates the file `outputs/index_to_place_and_date_and_mapmaker_names.csv`. 
4. Next, open the notebook `scripts/date_range.ipynb`. It's a Jupyter notebook, you may need to install some things. Or, you can copy all the code into a python script. Run each cell one at a time to see details of the processing, or press the run all button for the Jupyter notebook. This creates the final file, `outputs/index_to_place_and_date_and_mapmaker_names_with_date_estimates.csv`.
5. Finally, to add in some helpful columns to categorize the type of object (map/book, original edition yes/no), run `scripts/add_object_types.py`.


This table could then be used for data visualizations to explore questions
about the scale and scope of mapmaking in the sixteenth century. 

Potential improvements:
- Cross reference with the _Index to Date and Place_ to hopefully get more maps and catch errors.
- Research more about certain maps and mapmakers to better deal with the ambiguous index entries (see `outputs/errors_from_index_to_place_and_date_parsing.txt`) or the date ranges.
