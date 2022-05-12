import PyPDF2

def pdf_to_text(filename):
    try:
        pdfFileObj = open('Article_Summarization/pdftemp/'+filename, 'rb')
        #pdfFileObj = filename
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        text = ''
        #print(pdfReader.numPages) 
        for page in range(pdfReader.numPages):
            text = text + pdfReader.getPage(page).extractText()
        text = text.replace('\n', '')
        body = ' '.join(text.split())
        #print(body)
        pdfFileObj.close() 
        body = str(body)
        status = 0
        #print(body)
    except Exception as e:
        body = str(e)
        status = 1
    return status, body