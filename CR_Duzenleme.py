import pandas as pd


#iSearch direct citations (txt) dosyasını CiteSpace formatına sokabilmek için hazırlanmıştır.
#WoS CR alanı şeklinde yapılandırmaktadır
#Orijinal dosyada 308bin tekil citing var. Uzun sürüyor. 


inputAdress = 'C:\citations.txt'  #txt file'ın okunacağı adres

outputAdress = 'C:\son\sonartik.csv'  # Oluşturacak CSV file'ın adresi ve ismi 

ProcessAll = False    #Tüm veri işlenmek istenirse True yapılmalı. Aşağıdaki deneme yapılmak istenirse False
ProcessUntill = 100   #ProcessAll değişkeni True ise çalışmayasın. False ise burda verilen sayıya kadar veriyi işlesin.

df = pd.read_csv(inputAdress)
column_names = ["citingDoc", "citedDoc"]

myOutput = pd.DataFrame(columns = column_names)

deneme = df[df['citingDoc'] == "PN018453"]
first_column = df.iloc[:, 0]

myUniques = first_column.drop_duplicates(keep="first", inplace=False)
print(str(len(myUniques)) + " adet eşsiz citingDoc girdisi bulunmakta")
i=0
for unique in myUniques:
    deneme = df[df['citingDoc'] == unique]
    unifiedCited = deneme["citedDoc"].str.cat(sep = "; ")
    newRow = {'citingDoc': unique, 'citedDoc': unifiedCited}
    myOutput = myOutput.append(newRow, ignore_index=True)
    i += 1
    print(str(i) + ". CitingDoc verisi işlendi")
    if ProcessAll:
        continue
    elif i == ProcessUntill:
        break


myOutput.to_csv(outputAdress, index = False, header=True)
print("Veee bitti...")
