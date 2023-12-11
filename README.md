**Description of the Tool:**

The PDF spec extractor tool extracts the texts and tables from any PDF document to excel, segregates them chapter-wise into separate sheets, converts/processes them as JIRA requirements and make the excel ready for JIRA upload. JIRA uploads can be done using excel plugins like R4J. In addition this tool also outputs an excel that has all the table contents from pdf in a conventional readable format for quick review of contents before upload

**Users:**

This tool is useful for any protocol compliance and certification teams that are required to create the testable/non-testable requirements from a PDF in excel and maintain them as JIRA requirements. 

**Usage:**

python SpecExtractor.py [-h] -f <FILEPATH> -k <PROJECT_KEY> -o <OUTPUT_FILEPATH> -t < TABLE_OUTPUT_FILEPATH>

-h (or) --help
[show this help message and exit]                                                                             

**Mandatory params:**

-f (or) --filepath <FILEPATH>
[PDF file name with path, Mandatory]                                           

-k (or) --jira_project_key <PROJECT_KEY>
[Project Key to be updated in JIRA, Mandatory]

**Optional params:**

-o (or) --output_filepath <OUTPUT_FILEPATH>
[output excel file location, Default: <current working directory>\data_extract_test.xlsx]              
 
-t (or) --table_output_filepath <TABLE_OUTPUT_FILEPATH>
[output excel file location for Table, Default :< current working directory>\data_table_extract_test.xlsx]                                                                      

**Usage Examples:**

**[Use Case 1]** 

To get texts and tables from the PDF in jira format use the script “SpecExtractor.py”

**python SpecExtractor.py -f "C:\users\arunbosco\Desktop\NVM-Express-Base-Specification-2.0c-2022.10.04-Ratified.pdf" -k none**

The available chapters with chapter numbers will be printed on screen console and then the user can choose which chapter(s) or range of chapters to extract

Please enter the chapter number(s) extracted : <chapter(s) or chapter(s) range>

User can give the following options to choose chapters like,

all -> to extract all the chapters

1 -> to extract chapter 1								  

2,3 -> to extract chapters 2 and 3                                        

3-5 -> to extract chapters from 3 to 5

1,3-5 -> to extract chapter 1, 3, 4, 5

**[Use Case 2]**

To get only Tables from the PDF in non-jira format use the script “table_extract.py”

**python table_extract.py -f <path/pdf> -t <excel file path for table>**

**Environment:**

1.Python 3.8 Version required to run this tool
 
2.Python packages prerequisites pypi.org 
(pymupdf, pandas, openpyxl, camelot-py, stylerframe, opencv-python, ghostscript, zipfile2, numpy, Jinja2)
User can install the above packages using the "pip install -r requirements.txt"
“requirements.txt” file contains all the packages above mentioned

3.Third party dependencies and installation
   
https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps

ghostscript dll file download page:

https://ghostscript.com/releases/gsdnld.html

**Input PDF Format:**

The input PDF format must follow standard guidelines like mandatory presence of chapter numbers, figure numbers, table numbers, page numbers etc., 

