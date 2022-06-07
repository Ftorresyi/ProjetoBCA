#FUNÇÃO LÊ O BCA E MOSTRA O RESULTADO DA BUSCA NA TELA

import PyPDF3
import fitz  #pip install PyMuPDF
import re
import requests


OMs=[
    'GAP GL','PAMA GL','BAGL','CMRJ','1 CJM',
    'CEMAL','2/2 GT','CCA RJ','PAGL','1 GCC',
    'MTAB','DIRAP','DIRSA','CGABEG','BAGL_ANTIGA',
    'CBNB','SERIPA III','ESG','PAMB RJ','DTCEA-GL',
    '1/2 GT','BINFAE GL','1/1 GT','LAQFA','CTLA','GAP GL',
    'DT-INFRA RJ','ALA 11','CIMAER','CAE','COPE-S','GSD-GL',
    'MTAB-BOLIVIA','HFAG']
#print('O numero de OMs Apoiadas é: ', len(OMs))


def BuscaOMsApoiadas():
  BcadoDia = open('/content/drive/MyDrive/BCA/bca_do_dia.pdf', 'rb')
  leitura = PyPDF3.PdfFileReader(BcadoDia)

  ltotal = leitura.getNumPages()
  print('O numero de paginas do BCA do DIA é: ',ltotal)

  j=0
  while j < ltotal:
    i=0
    pagina = leitura.getPage(j) #Obtem a página atual do PDF
    materia = pagina.extractText() #Extrai o texto da página atual
    numPage=leitura.getPageNumber(pagina) #Obtem o numero da página atual
    m = materia  
    while i < len(OMs):
      OM_procurada = re.findall(OMs[i],m)
      if OM_procurada != []:
        print('A OM Apoiada: ',set(OM_procurada),'foi encontrada ',len(OM_procurada),' vez(es)', 'na página', numPage+1)
        BuscaResult = f'''
        OM Apoiada: {OM_procurada}
        Página Encontrada: {numPage+1}'''
        #texto_dinamico_teste['text'] = BuscaResult #Receberá o print da execução da função BuscaOMsApoiadas para mostrar o resultado em outra função ou botão do TKINTER
      i=i+1      
    j=j+1


def MarcaOMsApoiadas(*args):
  BcadoDia = fitz.open(*args)
  
  for page in BcadoDia: #loop para busca pagina a pagina dentro do BcadoDia
    for i in OMs:   #loop busca OM por OM da lista OMs em cada pagina do BcadoDia
      text_instances = page.search_for(i)  # text_instances recebe a busca da lista de OMs em todas as paginas  
      if text_instances != []:  #Se a lista de OMs nao for vazia    
        for j in text_instances: #Percorre a lista de palavras achadas uma a uma 
          highlight = page.add_highlight_annot(j) #marca a palavra da lista de achadas
          print('Foi encontrada a palavra: ', highlight) #imprime a palavra marcada que eh um objeto da classe Fitz
    
  BcadoDia.save("/content/drive/MyDrive/BCA/BcaMarcado.pdf")   


MarcaOMsApoiadas("/content/drive/MyDrive/BCA/bca_do_dia.pdf")


