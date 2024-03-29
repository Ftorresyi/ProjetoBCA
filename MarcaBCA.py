#FUNÇÃO LÊ O BCA E MARCA AS OM'S APOIADAS E PRINCIPAIS MATÉRIAS DE LEITURA

#ATENTAR PARA O DETALHE DE QUE FOI USADA A VERSÃO PyMuPDF==1.18.19 PARA QUE O FITZ FUNCIONASSE CORRETAMENTE
#POIS A FUNÇÃO HIGHLIGHT NÃO FUNCIONA CORRETAMENTE NA VERSÃO ATUAL (PyMuPDF==1.20)

#Instalar os requisitos:
#$ pip install PyMuPDF==1.18.19

from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz
from datetime import date
#import PyPDF3
from unidecode import unidecode

data_atual = str(date.today())

nBCA=input('Digite o número do BCA que será lido: ')
#dataBCA=input('Digite a data do BCA: ')

#LISTA DAS PALAVRAS QUE PRECISAM SER BUSCADAS NO PDF "bcadodia.PDF com seus padrões"
lista_padroes=[
    '1|2(:?.{0,3})1|2(:?.{0,3})GT', 'PRIMEIRO DO SEGUNDO GRUPO DE TRANSPORTE', 
    'PRIMEIRO DO PRIMEIRO GRUPO DE TRANSPORTE', 'SEGUNDO DO SEGUNDO GRUPO DE TRANSPORTE',
    '1(?:.{0,2})GCC', 'PRIMEIRO GRUPO DE COMUNICA??ES E CONTROLE',
    '1(?:.{0,2})CJM/gi', 'PRIMEIRA CIRCUNSCRI??O JUDICI?RIA MILITAR',
    'ALA(?:.{0,2})11', 'BASE A?REA DO GALE?O',
    'GAP(?:.{0,2})GL', 'GRUPAMENTO DE APOIO DO GALE?O',
    'PAMA(?:.{0,2})GL', 'PARQUE DE MATERIAL AERON?UTICO DO GALE?O',  
    'BAGL', 'BASE A?REA DO GALEAO', 'BAGL?ANTIGA'
    'CMRJ','COL?GIO MILITAR DO RIO DE JANEIRO',
    '1(?:.{0,2})CJM', 'PRIMEIRA CIRCUNSCRI??O JUDICI?RIA MILITAR',
    'CTLA','CENTRO DE TRANSPORTE LOG?STICO DA AERON??TICA',
    'CEMAL','CENTRO DE MEDICINA AEROESPACIAL',
    'BINFAE GL','BINFAE-GL','BATALHÃO DE INFANTARIA DA AERONÁUTICA ESPECIAL DO GALEÃO','BINFAEGL',
    'CCA RJ','CENTRO DE COMPUTAÇÃO DA AERONÁUTICA DO RIO DE JANEIRO','CCARJ',    
    'PAGL','PREFEITURA DE AERONÁUTICA DO GALEÃO',
    '3 ETA','3° ETA','TERCEIRO ETA','3ETA','3°ETA'
    'GOP GL','GOP-GL', 'GRUPO OPERACIONAL DO GALEÃO','GOPGL','GOPGL',
    'GLOG GL','GLOG-GL','GRUPO LOGÍSTICO DO GALEÃO', 'GLOGGL',
    'MTAB','MISSÃO TÉCNICA AERONÁUTICA BRASILEIRA NA BOLÍVIA',
    'DIRAP','DIRETORIA DE ADMINISTRAÇÃO DO PESSOAL',
    'DIRSA','DIRETORIA DE SAÚDE DA AERONÁUTICA',
    'CGABEG','CENTRO GERONTOLÓGICO DE AERONÁUTICA BRIGADEIRO EDUARDO GOMES',
    'CBNB','COLEGIO BRIGADEIRO NEWTON BRAGA',
    'SERIPA III','TERCEIRO SERVIÇO REGIONAL DE INVESTIGAÇÃO E PREVENÇÃO DE ACIDENTES AERONÁUTICOS','SERIPAIII',
    'ESG','ESCOLA SUPERIOR DE GUERRA',
    'PAMB RJ','PAMB-RJ','PARQUE DE MATERIAL BÉLICO DA AERONÁUTICA DO RIO DE JANEIRO','PAMBRJ',
    'DTCEA-GL','DTCEA GL','DESTACAMENTO DE CONTROLE DO ESPAÇO AÉREO DO GALEÃO','DTCEAGL',    
    'LAQFA','LABORATÓRIO QUÍMICO-FARMACÊUTICO DA AERONÁUTICA',    
    'CIMAER','CENTRO INTEGRADO DE METEOROLOGIA DA AERONÁUTICA',
    'CAE','CENTRO DE AQUISIÇÕES ESPEC?FICAS',
    'COPE-S','CENTRO DE OPERAÇÕES ESPACIAIS SECUNDÁRIO', 'COPE S',
    'GSD-GL','GRUPO DE SEGURAN?A E DEFESA DO GALE?O','GSDGL',
    'HFAG', 'HOSPITAL DE FORÇA A?REA DO GALE?O'
    
    ]  

OMs = [re.compile(padrao, re.IGNORECASE | re.DOTALL | re.MULTILINE ) for padrao in lista_padroes]

#LISTA DAS PALAVRAS QUE DEVERÃO SER DESMARCADAS:
PalavrasChave=[' PORTARIA DIRAP ', ' DA PORTARIA ','PORTARIA DIRAP N', 'PORTARIA DIRAP N°', 'SUBDIRETOR INTERINO DE PESSOAL MILITAR DA DIRAP', 
'SUBDIRETOR INTERINO DE PESSOAL CIVIL DA DIRAP', ' NOTA DIRAP ', ' PORTARIA  DIRAP ','^PORTARIA DIRAP Nº']

sumannot = 0
def MarcaOMsApoiadas(*args):
  BcadoDia = fitz.open(*args)
  #sumannot = 0
  global sumannot
  for page in BcadoDia: #loop para busca pagina a pagina dentro do BcadoDia
    for i in OMs:   #loop busca OM por OM da lista OMs em cada pagina do BcadoDia
      #text_instances = page.search_for(i.upper())  # text_instances recebe a busca da lista de OMs em todas as paginas
      text_instances = re.findall(i)
      if text_instances != []:  #Se a lista de OMs nao for vazia    
        for inst in text_instances: #Percorre a lista de palavras achadas uma a uma 
          highlight = page.addHighlightAnnot(inst) #marca a palavra da lista de achadas
          print('Foi encontrada a palavra: ', highlight) #imprime a palavra marcada que eh um objeto da classe Fitz
          sumannot = sumannot + 1
  print('Foram encontradas: ', sumannot, ' anotações no total')
  BcadoDia.save("bca_do_dia_marcado.pdf")
        
       
#by: ALAN KLINGER =================================================================================
#o jeito mais fácil foi fazer uma função semelhante a sua
#OBS: Isso está desmarcando os (DIRAP), não sei se era esse o objetivo
nannot=0
def removeHighlightv2(pdf_marcado, palavras_para_desmarcar):
  BcadoDia = fitz.open(pdf_marcado)
  #nannot=0
  global nannot
  for page in BcadoDia:
    #procuro pelas palavras que devem ser desmarcadas
    for palavra in palavras_para_desmarcar:
      text_instances = page.search_for(palavra)
      if len(text_instances) > 0: #é melhor comparar assim
      #se tiver encontrado algo, significa que provavelmente nessa pagina há alguma coisa que
      # foi marcada e não deveria ter sido marcada e agora será desmarcada
        for inst in text_instances:
          #para cada palavra que foi marcada, irei buscar todas as anotacoes
          #e verificar se há intercessão entre a anotação e aquilo que não deveria estar anotado
          for annot in page.annots():
            if (inst.intersect(annot.rect)):
              #print("Remove anotacao ", palavra ," pg", page.number)
              page.delete_annot(annot)
              nannot=nannot+1
  print('Foram removidas ', nannot, ' anotações')
  BcadoDia.save("Bca-"+nBCA+"_Marcado-"+data_atual+".pdf")
  
pdfmarcado=MarcaOMsApoiadas(input("Digite o nome do arquivo BCA que será lido, sem a extensão: ")+".pdf")
removeHighlightv2('bca_do_dia_marcado.pdf', PalavrasChave)
print('O Total de palavras encontradas para transcrição são: ', sumannot-nannot)
os.remove("bca_do_dia_marcado.pdf")


""" #FUNÇÃO ALTERNATIVA PARA BUSCAR PALAVRAS EM UM PDF. USA A LIB PYPDF3
#ESSA LIB POSSIU OUTRAS FUNCIONALIDADES PARA SEREM IMPLEMENTADAS FUTURAMENTE
#PORÉM, ELA NÃO FOI USADA, POIS NÃO POSSUI A FUNÇÃO HIGHLIGHT, POR ISSO USEI O FITZ PARA ESSE PROJETO

def BuscaOMsApoiadas(*args):
  BcadoDia = open(*args, 'rb')
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
    j=j+1 """