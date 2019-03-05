from os import listdir
import PyPDF2
import random
from reportlab.pdfgen import canvas

all_qs = []  # stores every question
pdfs = listdir("worksheets")  # list of all current worksheets


def extract_qs(text, current_question):
    questions = []  # questions for this one page
    has_more = True
    while has_more:  
        start_loc = text.find(" " + str(current_question) + ".")
        end_loc = text.find(" " + str(current_question + 1) + ".")
        q = text[start_loc:end_loc]
        has_more = len(q) is not 0 
        if has_more:
            questions.append(q)
            current_question += 1
    return (questions, current_question)


for pdf in pdfs:
    pdf_file = open("worksheets/" + pdf, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    num_pages = read_pdf.getNumPages()
    current_question = 1
    for i in range(num_pages):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        (these_qs, current_question) = extract_qs(page_content, current_question)
        all_qs.extend(these_qs)

# implement resevoir sampling
sample = []
k = 10
i = 0
n = len(all_qs)
# initialize sample with first k elements
for i in range(k):
    sample.append(all_qs[i])

while (i < n):
    j = random.randrange(i + 1)
    if (j < k):
        sample[j] = all_qs[i]
    i += 1

with open("review.txt", "wb") as f:
    for q in sample:
        string = q + "\n"
        f.write(string.encode())
