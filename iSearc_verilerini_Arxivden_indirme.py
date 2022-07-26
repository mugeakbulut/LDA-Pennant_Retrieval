from urllib import request
from bs4 import BeautifulSoup
import xlrd
import xlsxwriter
import time

BASLANGICSATIRI = 403622 #başlangıç satır no
BITISSATIRI = 403623 #bitiş satır no (son satır 434814)

myFile = '/Users/mugeakbulut/Desktop/iSearch_muge/iSearchIDs.xlsx'  #dosyanın bulunduğu adres (bu dosya iSearch'teki orijinal iSearchIDs dosyası)
myOutputFile = '/Users/mugeakbulut/Desktop/iSearch_muge/output.xlsx'   #output dosyasının oluşturulması istenen adres


print('excel aciliyor...')
wb = xlrd.open_workbook(myFile)
print('excel acildi!')
print('Veri Cekmeye baslaniyor.')
sheet = wb.sheet_by_index(0)

BITISSATIRI -= 1
i = BASLANGICSATIRI - 2
sonsatir=sheet.nrows

outWorkbook = xlsxwriter.Workbook(myOutputFile)
outSheet = outWorkbook.add_worksheet()

startTime = time.time()

DOITAGFOREXPORT = 'tablecell doi'
DOITAGFORORIGINAL ='tablecell msc_classes'

while i < BITISSATIRI:
    i += 1
    myLink = sheet.cell_value(i, 3)
    myLink = myLink[:7] + 'export.' + myLink[7:]
    resp = None

    while resp is None:
        try:
            resp = request.urlopen(myLink)

        except:
            print("Arxiv ACCESS DENIED: Bu nedenle program 20 dakika bekleyip tekrar baslayacak..")
            resp = None
            time.sleep(1200)
            pass

        else:
            # resp = request.urlopen('https://arxiv.org/abs/0802.1869')
            mySoup = BeautifulSoup(resp, "html.parser")

            myTitle = str(mySoup.find('h1', class_='title mathjax'))
            myTitle = myTitle[64:-5]  # 5. sütun

            myAuthor = mySoup.find('div', class_='authors')
            myAuthor = myAuthor.text[8:]  # 6. sütun

            submissionHistory = mySoup.find('div', class_='submission-history').text  # 9. sütun

            vbir = submissionHistory.find("[v1]")

            if submissionHistory.find("UTC") > 0:
                zamandilimi = submissionHistory.find("UTC")
            else:
                zamandilimi = submissionHistory.find("GMT")


            submissionYear = submissionHistory[zamandilimi - 14:zamandilimi - 10]  # 7. sütun

            submissionHistory = submissionHistory[vbir:]

            dateline = mySoup.find('div', class_='dateline').text

            sayi = dateline.find("Submitted on")
            try:
                submittedOn = dateline[sayi + 13:sayi + 24].replace(')', '')  # 8. sütun
            except:
                submittedOn = dateline[sayi + 13:sayi + 24]  # 8. sütun

            sayi = dateline.find("last revised")
            if sayi > 0:
                lastRevised = dateline[sayi + 13:sayi + 24]  # 10. sütun
            else:
                lastRevised = "N/A"

            myAbs = mySoup.find('blockquote', class_='abstract mathjax').text[11:]  # 11.Sütun
            #print(myAbs)

            myComments = mySoup.find('td', class_='tablecell comments mathjax')  # 12.Sütun

            if myComments is None:
                myComments = "N/A"
            else:
                myComments = myComments.text

            mySubjects = mySoup.find('td', class_='tablecell subjects').text  # 13.Sütun

            myJournal = mySoup.find('td', class_='tablecell jref')  # 14.Sütun
            if myJournal is None:
                myJournal = "N/A"
            else:
                myJournal = myJournal.text

            myDOI = mySoup.find('td', class_=DOITAGFOREXPORT)  # 15.Sütun
            if myDOI is None:
                myDOI = "N/A"
            else:
                myDOI = myDOI.text
            print(myDOI)

            myCite = mySoup.find('td', class_='tablecell arxivid')  # 16.Sütun
            if myCite is None:
                myCite = ""
            else:
                myCite = myCite.text

            myCiteTwo = mySoup.find('td', class_='tablecell arxividv')  # 16.Sütun
            if myCiteTwo is None:
                myCiteTwo = ""
            else:
                myCiteTwo = myCiteTwo.text

            CiteAs = myCite + myCiteTwo  # Sütun 16

            outSheet.write(i, 0, sheet.cell_value(i, 0))
            outSheet.write(i, 1, sheet.cell_value(i, 1))
            outSheet.write(i, 2, sheet.cell_value(i, 2))
            outSheet.write(i, 3, sheet.cell_value(i, 3))
            outSheet.write(i, 4, myTitle)  # 5
            outSheet.write(i, 5, myAuthor)  # 6
            outSheet.write(i, 6, submissionYear)  # 7
            outSheet.write(i, 7, submittedOn)  # 8
            outSheet.write(i, 8, submissionHistory)  # 9
            outSheet.write(i, 9, lastRevised)  # 10
            outSheet.write(i, 10, myAbs)  # 11
            outSheet.write(i, 11, myComments)  # 12
            outSheet.write(i, 12, mySubjects)  # 13
            outSheet.write(i, 13, myJournal)  # 14
            outSheet.write(i, 14, myDOI)  # 15
            outSheet.write(i, 15, CiteAs)  # 16
            print(i)
            time.sleep(2)


outWorkbook.close()
finishTime = time.time()
