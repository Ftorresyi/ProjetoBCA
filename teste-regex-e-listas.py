#Este código abre o arquivo PDF, 
# compila a lista de padrões em uma lista de padrões compilados, 
# e então itera por todas as páginas do PDF procurando cada padrão compilado na página atual. 
#Se um padrão for encontrado, ele será impresso na tela.

import re
import fitz
from unidecode import unidecode
import os
import glob

# Obtenha o caminho da pasta atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Encontre todos os arquivos PDF na pasta e seus subdiretórios
pdf_files = glob.glob(os.path.join(current_dir, '**/*.pdf'), recursive=True)

# Lista de padrões em expressões regulares
lista_padroes=[
    '1|2(:?.{0,3})1|2(:?.{0,3})GT', 'PRIMEIRO DO SEGUNDO GRUPO DE TRANSPORTE', 
    'PRIMEIRO DO PRIMEIRO GRUPO DE TRANSPORTE', 'SEGUNDO DO SEGUNDO GRUPO DE TRANSPORTE',
    '1(?:.{0,2})GCC', 'PRIMEIRO GRUPO DE COMUNICAÇÕES E CONTROLE',
    '1(?:.{0,2})CJM/gi', 'PRIMEIRA CIRCUNSCRIÇÃO JUDICIÁRIA MILITAR',
    'ALA(?:.{0,2})11', 'BASE AÉREA DO GALEÃO',
    'GAP(?:.{0,2})GL', 'GRUPAMENTO DE APOIO DO GALEÃO',
    'PAMA(?:.{0,2})GL', 'PARQUE DE MATERIAL AERONÁUTICO DO GALEÃO',  
    'BAGL', 'BASE AÉREA DO GALEÃO', 'BAGL(?:.)ANTIGA',
    'CMRJ','COLÉGIO MILITAR DO RIO DE JANEIRO',
    '1(?:.{0,2})CJM', 'PRIMEIRA CIRCUNSCRIÇÃO JUDICIÁRIA MILITAR',
    'CTLA','CENTRO DE TRANSPORTE LOGÍSTICO DA AERONÁUTICA',
    'CEMAL','CENTRO DE MEDICINA AEROESPACIAL']

#Remove os acentos do padrão:
patterns = [unidecode(padrao) for padrao in lista_padroes]

#Compilando os padrões:
patterns = [re.compile(padrao, re.IGNORECASE | re.DOTALL | re.MULTILINE ) for padrao in lista_padroes]

#Inicializa a variável que conta os matches:
sumannot = 0

# Itere sobre a lista de arquivos PDF e abra cada um deles
for pdf_file in pdf_files:
    with fitz.open(pdf_file) as doc:
        # Faça algo com o arquivo PDF, por exemplo, extrair texto
            

        # Percorrer as páginas do PDF
        for page in doc:
            #page = pdf_file[i]
            text = page.getText()

            # Remova os acentos do texto
            pdf_file = unidecode(pdf_file)

            # Procurar correspondências de padrões em expressões regulares no texto da página
            for pattern in patterns:
                matches = pattern.findall(text)
                #pdf_file.search_for(matches)
                if matches != []:
                    for inst in matches: #Percorre a lista de palavras achadas uma a uma 
                        highlight = page.add_highlight_annot(inst) #marca a palavra da lista de achadas
                        print('Foi encontrada a palavra: ', highlight) #imprime a palavra marcada que eh um objeto da classe Fitz
                        sumannot = sumannot + 1
                        print('Foram encontradas: ', sumannot, ' anotações no total')
                        doc.save("bca_do_dia_marcado.pdf")
                        #print("Página: ", page)
                        #print("Padrão:", pattern.pattern)
                        #print("Correspondências:", matches)


#Sem a flag re.MULTILINE, a busca re.findall irá encontrar todas as ocorrências do padrão 
# procurado no texto, mas considerando que a string inteira é uma única linha. 
# Isso significa que, se você procura por um padrão que começa com o início da string (^) 
# e termina com o final da string ($), somente será encontrado o primeiro e o último padrão no texto.
#Se você adicionar a flag re.MULTILINE, 
# a busca irá considerar a string inteira como múltiplas linhas, 
# e o início da string (^) e o final da string ($ ) corresponderão ao início 
# e fim de cada linha, respectivamente. Dessa forma, a busca irá encontrar todas as ocorrências 
# do padrão procurado em cada linha.


