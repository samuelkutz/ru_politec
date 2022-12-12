#obs: the comments are meant for PT-BR readers! 
#xpath é tipo um path de arquivos só que para tags html
import requests
from lxml import html, etree
from datetime import date

#puxando as infos do site (web scraping yay)
url = 'https://pra.ufpr.br/ru/ru-centro-politecnico/'
page = requests.get(url, headers={"User-Agent" : 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)'})
tree = html.fromstring(page.content, parser=etree.HTMLParser(encoding="utf-8"))

#funcao para pegar a lista de itens do menu, dado o xpath do mesmo e tal
def clear_texts_from(xpath) -> list:
  """
  cleans the text data scrapped from RU
  """
  dirty_texts = [x.strip(" ") for x in tree.xpath(xpath)]
  clean_texts = []
  
  for item in dirty_texts:
    if item != '': 
      clean_texts.append(item)
      
  return clean_texts

#PROBLEMA: AS VEZES ELES MUDAM O XPATH disso POR MOTIVOS???????
#string no formato "%DAYOFWEEK%: dd/mm/yy", tirada do site do RU
day1 = ''.join(str(x) for x in clear_texts_from('//*[@id="post"]/div[2]/p[4]/strong/text()'))
day2 = ''.join(str(x) for x in clear_texts_from('//*[@id="post"]/div[2]/p[5]/strong/text()'))
  
#funcao para formatar uma lista de itens do menu em uma unica string
def format_menu(cafe=None, almoco=None, jantar=None) -> str:
  """
  USE OPTIONAL ARGS!!!
  """
  
  #nao liga pra isso, é uma boa prática de uns ngc la q eu quis testar
  #-----------------#
  if cafe is None:
    cafe = []

  if almoco is None:
    almoco = []
  
  if jantar is None:
    jantar = []
  #-----------------#

  #creio q nem precise explicar oq acontece aq (demorei mt pra deixar "entendivel")
  cardapio = ""
  if cafe:  
    cardapio += "Café: "
    for item in cafe:
      cardapio += f"\n  • {item}"
  
  if almoco:  
    cardapio += "Almoço: "
    for item in almoco:
      cardapio += f"\n  • {item}"

  if jantar:  
    cardapio += "Jantar: " 
    for item in jantar: 
      cardapio += f"\n  • {item}"

  return cardapio


#funcoes para pegar menu especifico
def menu_cafe(dia=None) -> str:
  """
  retorna uma string formatadinha com as informações do cafe
  """
  global day1
  global day2
  
  if dia == None:  
    today = date.today()
    dia = today.strftime("%d/%m/%y")

  #note que há diferenca entre os xpaths dos menus esta       no     figure[i]    e    no  tr[i] q é cafe, almoco, jantar         
  if dia in day1:
    return format_menu(cafe=clear_texts_from('//*[@id="post"]/div[2]/figure[2]/table/tbody/tr[2]/td/text()'))

  elif dia in day2:
    return format_menu(cafe=clear_texts_from('//*[@id="post"]/div[2]/figure[3]/table/tbody/tr[2]/td/text()')) 


def menu_almoco(dia=None) -> str:
  """
  retorna uma string formatadinha com as informações do almoco
  """
  global day1
  global day2

  if dia == None:  
    today = date.today()
    dia = today.strftime("%d/%m/%y")

  if dia in day1:
    return format_menu(almoco=clear_texts_from('//*[@id="post"]/div[2]/figure[2]/table/tbody/tr[4]/td/text()'))

  elif dia in day2:
    return format_menu(almoco=clear_texts_from('//*[@id="post"]/div[2]/figure[3]/table/tbody/tr[4]/td/text()'))


def menu_jantar(dia=None) -> str:
  """
  retorna uma string formatadinha com as informações do almoco
  """
  global day1
  global day2

  if dia == None:
    today = date.today()
    dia = today.strftime("%d/%m/%y")

  if dia in day1:
    return format_menu(jantar=clear_texts_from('//*[@id="post"]/div[2]/figure[2]/table/tbody/tr[6]/td/text()'))

  elif dia in day2:
    return format_menu(jantar=clear_texts_from('//*[@id="post"]/div[2]/figure[3]/table/tbody/tr[6]/td/text()'))


#checa se o dia dado tem RU
#se nao for dado o dia, checa o dia atual (de acordo com UTC)
def is_ru_open(dia=None) -> bool:
  """
  retorna se hj tem ou nao RU
  """
  global day1
  global day2
  
  if dia == None:  
    today = date.today()
    dia = today.strftime("%d/%m/%y")

  if dia in day1:
    return True
    
  elif dia in day2:
    return True

  else:
    return False

#sim eu precisei disso, acredita?
def today_is() -> str:
  """
  retorna o dia que é hj
  """
  global day1
  global day2

  today = date.today()
  dia = today.strftime("%d/%m/%y")
  
  if dia in day1:
    return day1

  elif dia in day2:
    return day2

  else:
    return dia