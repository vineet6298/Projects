import PyPDF2
import pyttsx3
file='\\'.join(input("Enter File Name(with location):").split('/'))
#pdfFileObj=open("QB_ICT_B-Tech_Cloud_4S_TSec.pdf","rb")
pdfFileObj=open(file,"rb")
pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
mytext=""
for pageNum in range(pdfReader.numPages):
    pageObj=pdfReader.getPage(pageNum)
    mytext+=pageObj.extractText()
pdfFileObj.close()
print(mytext)
engine = pyttsx3.init()
engine.say(mytext)
engine.setProperty('rate',120)
engine.setProperty('volume', 0.9)
engine.runAndWait()