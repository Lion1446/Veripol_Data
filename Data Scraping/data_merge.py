import PyPDF2
import os

def get_datasets():
    datasets = []
    file_path = "env\\templates"
    regional = os.listdir(file_path)
    for region in regional:
        provinces = os.listdir(f"{file_path}\\{region}")
        for province in provinces:
            if ".pdf" in province:
                datasets.append(f"{file_path}\\{region}\\{province}")
            else:
                municipalities = os.listdir(f"{file_path}\\{region}\\{province}")
                for municipality in municipalities:
                    datasets.append(f"{file_path}\\{region}\\{province}\\{municipality}")
    return datasets


datasets = get_datasets()
count = len(datasets)

pdfWriter = PyPDF2.PdfFileWriter()
for i in range(count):
    print(f"Merging: {i+1}/{len(datasets)} - {datasets[i]}")
    pdfFile = open(datasets[i], 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        pdfWriter.addPage(pageObj)
pdfOutputFile = open('MergedDatasets.pdf', 'wb')
pdfWriter.write(pdfOutputFile)
pdfOutputFile.close()
pdfFile.close()



# # Open the files that have to be merged one by one
# pdf1File = open('Complete Candidate Dataset files\\files\\BARMM\\BASILAN\\AKBAR.pdf', 'rb')
# pdf2File = open('Complete Candidate Dataset files\\files\\BARMM\\BASILAN\\AL-BARKA.pdf', 'rb')
 
# # Read the files that you have opened
# pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
# pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
 
# # Create a new PdfFileWriter object which represents a blank PDF document
# pdfWriter = PyPDF2.PdfFileWriter()
 
# # Loop through all the pagenumbers for the first document
# for pageNum in range(pdf1Reader.numPages):
#     pageObj = pdf1Reader.getPage(pageNum)
#     pdfWriter.addPage(pageObj)
 
# # Loop through all the pagenumbers for the second document
# for pageNum in range(pdf2Reader.numPages):
#     pageObj = pdf2Reader.getPage(pageNum)
#     pdfWriter.addPage(pageObj)
 
# # Now that you have copied all the pages in both the documents, write them into the a new document
# pdfOutputFile = open('MergedFiles.pdf', 'wb')
# pdfWriter.write(pdfOutputFile)
 
# # Close all the files - Created as well as opened
# pdfOutputFile.close()
# pdf1File.close()
# pdf2File.close()