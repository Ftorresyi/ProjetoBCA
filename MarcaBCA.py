#FUNÇÃO LÊ O BCA E MOSTRA O RESULTADO DA BUSCA NA TELA
#C:\Program Files\Python310\Lib\site-packages\PyPDF3

import PyPDF3
import fitz  #pip install PyMuPDF
import re
import requests


OMs=[
    'GAP GL','GRUPAMENTO DE APOIO DO GALEÃO','PAMA GL','PARQUE DE MATERIAL AERONÁUTICO DO GALEÃO',
    'BAGL','BASE AÉREA DO GALEÃO','CMRJ','COLÉGIO MILITAR DO RIO DE JANEIRO',
    '1 CJM','PRIMEIRA CIRCUNSCRIÇÃO JUDICIÁRIA MILITAR','CEMAL','CENTRO DE MEDICINA AEROESPACIAL',
    '2/2 GT','SEGUNDO ESQUADRÃO DO SEGUNDO GRUPO DE TRANSPORTE','CCA RJ','CENTRO DE COMPUTAÇÃO DA AERONÁUTICA DO RIO DE JANEIRO',
    'PAGL','PREFEITURA DE AERONÁUTICA DO GALEÃO','1 GCC','PRIMEIRO GRUPO DE COMUNICAÇÕES E CONTROLE',
    'MTAB','MISSÃO TÉCNICA AERONÁUTICA BRASILEIRA NA BOLÍVIA','DIRAP','DIRETORIA DE ADMINISTRAÇÃO DO PESSOAL',
    'DIRSA','DIRETORIA DE SAÚDE DA AERONÁUTICA','CGABEG','CASA GERONTOLÓGICA DE AERONÁUTICA BRIGADEIRO EDUARDO GOMES',
    'BAGL_ANTIGA','CBNB','COLEGIO BRIGADEIRO NEWTON BRAGA',
    'SERIPA III','TERCEIRO SERVIÇO REGIONAL DE INVESTIGAÇÃO E PREVENÇÃO DE ACIDENTES AERONÁUTICOS',
    'ESG','ESCOLA SUPERIOR DE GUERRA','PAMB RJ','PARQUE DE MATERIAL BÉLICO DA AERONÁUTICA DO RIO DE JANEIRO',
    'DTCEA-GL','DESTACAMENTO DE CONTROLE DO ESPAÇO AÉREO DO GALEÃO','1/2 GT','PRIMEIRO ESQUADRÃO DO SEGUNDO GRUPO DE TRANSPORTE',
    'BINFAE GL','BATALHÃO DE INFANTARIA DA AERONÁUTICA ESPECIAL DO GALEÃO',
    '1/1 GT','PRIMEIRO ESQUADRÃO DO PRIMEIRO GRUPO DE TRANSPORTE','LAQFA','LABORATÓRIO QUÍMICO-FARMACÊUTICO DA AERONÁUTICA',
    'CTLA','CENTRO DE TRANSPORTE LOGÍSTICO DA AERONÁUTICA','ALA 11','CIMAER','CENTRO INTEGRADO DE METEOROLOGIA AERONÁUTICA',
    'CAE','CENTRO DE AQUISIÇÕES ESPECÍFICAS','COPE-S','CENTRO DE OPERAÇÕES ESPACIAIS SECUNDÁRIO'
    'GSD-GL','GRUPO DE SEGURANÇA E DEFESA DO GALEÃO','HFAG', 'HOSPITAL DE FORÇA AÉREA DO GALEÃO']

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
    
  BcadoDia.save("bca_do_dia_marcado.pdf")


MarcaOMsApoiadas("bca_do_dia.pdf")


