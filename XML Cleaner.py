from bs4 import BeautifulSoup
import re
import os

path = r"C:\\Users\\ryjar_000\Downloads\Raw XMLs"

s = ""
i = 0

for filename in os.listdir(path):

    soup = BeautifulSoup(open(str(path + r"\\" + filename), encoding='ascii',errors="ignore"), "lxml")
    
    [tag.extract() for tag in soup.findAll(['title','siteinfo', 'ns', 'id', 'parentid', 'timestamp', 'contributor', 'comment', 'model', 'format', 'sha1'])]
    soup = soup.get_text()
    
    soup = re.sub(r'\<\!\-\-(.*?)(.|\n)*?\-\-\>'
                  '|\&nbsp\;', " ",soup)
    
    soup = re.sub(r'\&ndash\;', "-",soup)
    
    soup = re.sub(r'\{\{(I|i)nfobox(.*?)(.|\n)*?\}\}'
                  '|\[\[(I|i)mage\:[^)]*\]\]'
                  '|\[\[(F|f)ile\:(.*?)(.|\n)*?\]\]'
                  '|\'\'\''
                  '|\{\{(.*?)(.|\n)*?\}\}'
                  '|\=\=?\=?( +)?(R|r)eference[^~]*.*'
                  '|\=\=?\=?( +)?(R|r)eferences[^~]*.*'
                  '|\=\=?\=?( +)?(E|e)xternal link[^~]*.*'
                  '|\=\=?\=?( +)?(E|e)xternal links[^~]*.*'
                  '|\<ref(.*?)>((.|\n)*?\<\/ref\>)?'
                  '|\<gallery(.*?)>(.|\n)*?\<\/gallery\>'
                  '|\<blockquote(.*?)>(.|\n)*?\<\/blockquote\>'
                  '|\<small(.*?)>(.|\n)*?\<\/small\>'
                  '|\{\{ISBN[^)]*\}\}'
                  '|\{\{HTTP[^)]*\}\}'
                  '|<\/?code>'
                  '|\[http(.*?)(.|\n)*?\]'
                  '|\[\[[A-Za-z0-9\s\~\!\@\#\$\%\^\&\*\(\)\_\+\{\}\|\:\\\"\<\>\?\,\-\']+\|'
                  '|\=\=?\=?( +)?See also[^)]*\]\]'
                  '|\=\=\=?'
                  '|\*'
                  '|\#'
                  '|( +)\;( +)'
                  , " ", soup)
    
    soup = re.sub(r'\|(.*?)(.|\n)*?\}', " ",soup)

    soup = re.sub(r'\[\[\:.*\|(.*)\]\].?', r"\1",soup)
    
    soup = re.sub(r'{{.*}}'
                  '|\[\['
                  '|\]\]'
                  '|}|}'
                  '|\{'
                  , '',soup)
    
    soup = re.sub(r'\-\-\>', "-",soup)
    soup = re.sub(r'\[\'', ' ', soup)
    soup = re.sub(r'\'\'', '"', soup)
    soup = re.sub(r'\.(?! )', '. ', soup)
    soup = re.sub(r'<\/?(.*?)>', ' ', soup)
    soup = re.sub(r'\:(?! )', ': ', soup)

    soup = soup.strip().replace('\n','')

    print(soup)

    with open(r"C:\\Users\\ryjar_000\Desktop\Scripts\Clean\\" + str(i) + ".txt", "w", encoding='ascii') as output:
        output.write(str(soup))
        i+=1