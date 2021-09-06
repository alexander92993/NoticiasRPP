import requests
from lxml import html
import pandas as pd
import os

headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'"
}

dptos = ['loreto','madre-de-dios','san-martin','ancash','ica','huanuco','huancavelica','ucayali','cusco','apurimac','pasco','la-libertad','moquegua','tacna','tumbes','lambayeque','amazonas','cajamarca','lima','ayacucho','arequipa','callao','piura','junin','puno']

ruta_export = input('Ingrese la ruta donde se exportará: ')
os.chdir(ruta_export)

writer = pd.ExcelWriter('Noticias.xlsx', engine='openpyxl')

for departamento in dptos:
    url = 'https://rpp.pe/noticias/' + departamento
    r = requests.get(url,headers=headers)
    parse = html.fromstring(r.content)

    dpto = parse.xpath('//h1/text()')
    dpto2 = dpto[0]
    articulos = parse.xpath('.//article/div[@class = "inner-card"]/div[@class = "cont"]/h2/a/text()')
    links = parse.xpath('.//article/div[@class = "inner-card"]/div[@class = "cont"]/h2/a/@href')
    parrafos = parse.xpath('.//article/div[@class = "inner-card"]/div[@class = "cont"]//p')

    cont = len(articulos)
    r_dpto = [dpto2 for _ in range(cont)]

    x = 0
    parrafos2 = []
    for parrafo in parrafos:
        corregido = parrafo.text_content().replace(';', ',')
        parrafos2.append(corregido)
        #print(x,': ',corregido)
        x+=1
    #print(os.getcwd())

    df = pd.DataFrame(list(zip(r_dpto,articulos,parrafos2,links)), columns = ['departamento','articulos','parrafos','links'])
    #df.to_csv('noticias.csv',index=False,  sep = '|',encoding='utf-8-sig')
    df.to_excel(writer,index=False, sheet_name=dpto2)
    writer.save()
    print(dpto2)


