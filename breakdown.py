# based on glenbambrick.com, Geospatiality
# modified/improved by Alex Simoneau, @afsimoneau on github
# designed to break down pdf master file for AMZ labels into renamed FNSKU labels

# import the necessary modules
import os
import PyPDF2
import re
import progressbar

# function to extract the individual pages from each pdf found


def split_pdf_pages(root_directory, extract_to_folder):
    # traverse down through the root directory to sub-directories
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            # if a file is a pdf
            if extension == ".pdf":
                # create a reference to the full filename path
                fullpath = root + "/" + basename + extension

                # open the pdf in read mode
                opened_pdf = PyPDF2.PdfFileReader(open(fullpath, "rb"))

                # for each page in the pdf
                print("extracting \""+filename+ "\" ...")
                for i in progressbar.progressbar(range(opened_pdf.numPages)):
                    # write the page to a new pdf
                    output = PyPDF2.PdfFileWriter()
                    output.addPage(opened_pdf.getPage(i))
                    with open(extract_to_folder + "/" + basename.replace(" ", "_") + "-%s.pdf" % i, "wb") as output_pdf:
                        output.write(output_pdf)

# function for renaming the single page pdfs based on text in the pdf


def rename_pdfs(extraced_pdf_folder, rename_folder):
    # traverse down through the root directory to sub-directories
    print("renaming all...")
    for root, dirs, files in os.walk(extraced_pdf_folder):
        for filename in progressbar.progressbar(files):
            basename, extension = os.path.splitext(filename)
            # if a file is a pdf
            if extension == ".pdf":
                # create a reference to the full filename path
                fullpath = root + "/" + basename + extension

                # open the individual pdf
                pdf_file_obj = open(fullpath, "rb")
                pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

                # access the individual page
                page_obj = pdf_reader.getPage(0)
                # extract the the text
                pdf_text = page_obj.extractText()

                # use regex to find information
                match = re.search(expression, pdf_text)
                # close pdf to rename
                pdf_file_obj.close()
                if match:
                    # rename the pdf based on the information in the pdf
                    os.rename(fullpath, rename_folder +
                              "/" + match.group(0) + ".pdf")


# parameter variables
root_dir = os.path.dirname(os.path.abspath(__file__))+"/source-files-here"
extract_to = os.path.dirname(os.path.abspath(__file__))+"/extract"
rename_to = os.path.dirname(os.path.abspath(__file__))+"/rename"
expression = "[BX]+[\dA-Z]{9}"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)
if not os.path.exists(extract_to):
    os.makedirs(extract_to)
if not os.path.exists(rename_to):
    os.makedirs(rename_to)
# use the two functions
split_pdf_pages(root_dir, extract_to)
rename_pdfs(extract_to, rename_to)
