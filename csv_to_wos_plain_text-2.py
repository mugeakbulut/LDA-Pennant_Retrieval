import pandas as pd

#naber = pd.read_csv("/Users/mugeakbulut/Desktop/WOSAGOREDUZENLENMIS_v.csv", low_memory=False)  #input file (as CSV) path
naber = pd.read_excel("/Users/mugeakbulut/Desktop/MUGE.xlsx")  #input file (as CSV) path
naber = naber.replace(r'\n', '\n   ', regex=True)

anaString = "FN Clarivate Analytics Web of Science\nVR 1.0\n"

for i in range(len(naber)):
    for a in range(len(naber.columns)):
        deger = str(naber.iloc[i, a])
        sutunismi = str(naber.columns[a])
        yazilacak = sutunismi + " " + deger + "\n"
        anaString = anaString + yazilacak
    anaString = anaString + "ER \n\n"

print(anaString)
text_file = open("/Users/mugeakbulut/Desktop/Outputtt.txt", "w")  #output filey path
text_file.write(anaString)
text_file.close()
