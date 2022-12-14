#FUNÇÃO LÊ O BCA E MARCA AS OM'S APOIADAS E PRINCIPAIS MATÉRIAS DE LEITURA

#Instalar os requisitos:
#$ pip install PyMuPDF==1.18.9

from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz
from datetime import date


data_atual = str(date.today())

#FUNÇÃO ALTERNATIVA PARA BUSCAR PALAVRAS EM UM PDF. USA A LIB PYPDF3
#ESSA LIB POSSIU OUTRAS FUNCIONALIDADES PARA SEREM IMPLEMENTADAS FUTURAMENTE
#PORÉM, ELA NÃO FOI USADA, POIS NÃO POSSUI A FUNÇÃO HIGHLIGHT, POR ISSO USEI O FITZ PARA ESSE PROJETO
#ATENTAR PARA O DETALHE DE QUE FOI USADA A VERSÃO PyMuPDF==1.18.9 PARA QUE O FITZ FUNCIONASSE CORRETAMENTE
#POIS A FUNÇÃO HIGHLIGHT NÃO FUNCIONA CORRETAMENTE NA VERSÃO ATUAL (PyMuPDF==1.20)
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
    j=j+1

nBCA=input('Digite o número do BCA que será lido: ')
#dataBCA=input('Digite a data do BCA: ')

#LISTA DAS PALAVRAS QUE PRECISAM SER BUSCADAS NO PDF "bcadodia.PDF"
OMs=[
    'GAP GL','GRUPAMENTO DE APOIO DO GALEÃO','PAMA GL','PARQUE DE MATERIAL AERONÁUTICO DO GALEÃO',
    'BAGL','BASE AÉREA DO GALEÃO','CMRJ','COLÉGIO MILITAR DO RIO DE JANEIRO',
    '1 CJM','PRIMEIRA CIRCUNSCRIÇÃO JUDICIÁRIA MILITAR',' CEMAL','CENTRO DE MEDICINA AEROESPACIAL',
    ' 2/2 GT','SEGUNDO ESQUADRÃO DO SEGUNDO GRUPO DE TRANSPORTE','CCA RJ','CENTRO DE COMPUTAÇÃO DA AERONÁUTICA DO RIO DE JANEIRO',
    'PAGL','PREFEITURA DE AERONÁUTICA DO GALEÃO',' 1 GCC','PRIMEIRO GRUPO DE COMUNICAÇÕES E CONTROLE',
    'MTAB','MISSÃO TÉCNICA AERONÁUTICA BRASILEIRA NA BOLÍVIA','DIRAP','DIRETORIA DE ADMINISTRAÇÃO DO PESSOAL',
    ' DIRSA ','DIRETORIA DE SAÚDE DA AERONÁUTICA','CGABEG','CASA GERONTOLÓGICA DE AERONÁUTICA BRIGADEIRO EDUARDO GOMES',
    'BAGL_ANTIGA','CBNB','COLEGIO BRIGADEIRO NEWTON BRAGA',
    'SERIPA III','TERCEIRO SERVIÇO REGIONAL DE INVESTIGAÇÃO E PREVENÇÃO DE ACIDENTES AERONÁUTICOS',
    ' ESG ','ESCOLA SUPERIOR DE GUERRA','PAMB RJ','PARQUE DE MATERIAL BÉLICO DA AERONÁUTICA DO RIO DE JANEIRO',
    'DTCEA-GL','DESTACAMENTO DE CONTROLE DO ESPAÇO AÉREO DO GALEÃO',' 1/2 GT','PRIMEIRO ESQUADRÃO DO SEGUNDO GRUPO DE TRANSPORTE',
    'BINFAE GL','BATALHÃO DE INFANTARIA DA AERONÁUTICA ESPECIAL DO GALEÃO',
    ' 1/1 GT','PRIMEIRO ESQUADRÃO DO PRIMEIRO GRUPO DE TRANSPORTE','LAQFA','LABORATÓRIO QUÍMICO-FARMACÊUTICO DA AERONÁUTICA',
    'CTLA','CENTRO DE TRANSPORTE LOGÍSTICO DA AERONÁUTICA','ALA 11','CIMAER','CENTRO INTEGRADO DE METEOROLOGIA AERONÁUTICA',
    ' CAE ','CENTRO DE AQUISIÇÕES ESPECÍFICAS','COPE-S','CENTRO DE OPERAÇÕES ESPACIAIS SECUNDÁRIO'
    'GSD-GL','GRUPO DE SEGURANÇA E DEFESA DO GALEÃO','HFAG', 'HOSPITAL DE FORÇA AÉREA DO GALEÃO', 'MOVIMENTAÇÃO', 'PROMOÇÃO']

#LISTA DAS PALAVRAS QUE DEVERÃO SER DESMARCADAS:
PalavrasChave=[' PORTARIA DIRAP ', ' da PORTARIA ', '\tPortaria Dirap n', '\nPortaria DIRAP n°', 'Subdiretor Interino de Pessoal Militar da Dirap']

def MarcaOMsApoiadas(*args):
  BcadoDia = fitz.open(*args)
  
  for page in BcadoDia: #loop para busca pagina a pagina dentro do BcadoDia
    for i in OMs:   #loop busca OM por OM da lista OMs em cada pagina do BcadoDia
      text_instances = page.search_for(i)  # text_instances recebe a busca da lista de OMs em todas as paginas  
      if text_instances != []:  #Se a lista de OMs nao for vazia    
        for inst in text_instances: #Percorre a lista de palavras achadas uma a uma 
          highlight = page.addHighlightAnnot(inst) #marca a palavra da lista de achadas
          print('Foi encontrada a palavra: ', highlight) #imprime a palavra marcada que eh um objeto da classe Fitz
    
  BcadoDia.save("bca_do_dia_marcado.pdf")
        
       
#by: ALAN KLINGER =================================================================================
#o jeito mais fácil foi fazer uma função semelhante a sua
#OBS: Isso está desmarcando os (DIRAP), não sei se era esse o objetivo
def removeHighlightv2(pdf_marcado, palavras_para_desmarcar):
  BcadoDia = fitz.open(pdf_marcado)
  nannot=0
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
              print("Remove anotacao ", palavra ," pg", page.number)
              page.delete_annot(annot)
              nannot=nannot+1
  print('Foram removidas ', nannot, ' anotações')
  BcadoDia.save("Bca-"+nBCA+"_Marcado-"+data_atual+".pdf")
  


pdfmarcado=MarcaOMsApoiadas(input("Digite o nome do arquivo BCA que será lido, sem a extensão: ")+".pdf")
removeHighlightv2('bca_do_dia_marcado.pdf', PalavrasChave)
os.remove("bca_do_dia_marcado.pdf")