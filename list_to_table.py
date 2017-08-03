from pprint import pprint
import re

from shared import *


WIKI_LINK_PREFIX = '[['
WIKI_LINK_SUFFIX = ']]'


#------------------------------------------------------------------------------#
#                               PARSE SECTION                                  #
#------------------------------------------------------------------------------#

def parse_text(text):
    table_lines = []
    for line_text in text.split('\n'):
        print(line_text)
        line_info = parse_list_line(line_text)
        table_line = make_table_line(line_info)
        table_lines.append(table_line)

    return '\n'.join(table_lines)

def parse_list_line(list_line_text):
    line_info = {
        'no_prize': False,
        'books': 1,
        'number': '0',
        'year': '1990',
        'authors': [],
        'titles': []
    }

    number_year_re_str = '\*第(\d+?)回[ ]*?（\[\[(\d{4})年\]\]）'
    author_title_re_str = '[ ・](?:(\[\[.*?\]\])[ ]『(.*?)』)'
    no_prize_re_str = '.*?該当なし'
    
    number_year_re = re.compile(number_year_re_str)
    author_title_re = re.compile(author_title_re_str)
    no_prize_re = re.compile(no_prize_re_str)

    number, year = number_year_re.findall(list_line_text)[0]
    line_info['number'] = number
    line_info['year'] = year
    
    if (no_prize_re.match(list_line_text)):
        line_info['no_prize'] = True

    books = 0
    for author, title in author_title_re.findall(list_line_text):
        books += 1
        line_info['authors'].append(author)
        line_info['titles'].append(title)
        
    line_info['books'] = books

    return line_info
    
#------------------------------------------------------------------------------#
#                                MAKE SECTION                                  #
#------------------------------------------------------------------------------#

def is_one_link(link_text):
    if (link_text.startswith(WIKI_LINK_PREFIX)):
        if (link_text.endswith(WIKI_LINK_SUFFIX)):
            if (link_text.count(WIKI_LINK_PREFIX) == 1):
                if (link_text.count(WIKI_LINK_SUFFIX) == 1):
                    return True
    return False

## make
## 'damn lol blyat fuck go away'
## from
## '[[damn]] [[lol (shit)|lol]] blyat [[lol (fuck)|fuck]] [[go]] [[Нахуй - это туда!|away]]'

def cleanup_inner_link(text):
    if (WIKI_LINK_PREFIX in text):
        if (WIKI_LINK_SUFFIX in text):
            begin = text.index(WIKI_LINK_PREFIX)
            end = text.index(WIKI_LINK_SUFFIX)
            sep = '|'
            if (sep in text[begin:end]):
                sep_pos = text.index(sep)
                return text[:begin] + text[sep_pos+len(sep):end] + cleanup_inner_link(text[end+len(WIKI_LINK_SUFFIX):])
            else:
                return text[:begin] + text[begin + len(WIKI_LINK_PREFIX):end] + cleanup_inner_link(text[end+len(WIKI_LINK_SUFFIX):])
    else:
        return text
    

def analyze_wikilink(link_text):
    link_info = {
        'redlink' : False,
        'label' : '',
        'link' : ''
        }

    if (is_one_link(link_text)):
        link = link_text.lstrip(WIKI_LINK_PREFIX)
        link = link.rstrip(WIKI_LINK_SUFFIX)

        # label check
        label_separator = '|'
        if (label_separator in link):
            link_url, link_label = link.split(label_separator)
            link_info['link'] = link_url
            link_info['label'] = link_label
        else:
            link_info['link'] = link
    else:
        link = cleanup_inner_link(link_text)
        link_info['redlink'] = True
        link_info['link'] = link
    
    return link_info


def make_author_link(author_text):
    link_info = analyze_wikilink(author_text)
    
    if not link_info['redlink']:
        link_text = '{{нп3|||ja|%s}}' % link_info['link']
    else:
        link_text = '%s' % link_info['link']
        
    return link_text
        

def make_title_link(title_text):
    link_info = analyze_wikilink(title_text)
    
    if not link_info['redlink']:
        link_text = "''{{нп3|||ja|%s}}'' ({{lang-ja|%s}})" % (link_info['link'],
                                                            link_info['label']
                                                            )
    else:
        link_text = "'''' ({{lang-ja|%s}})" % (link_info['link'])
        
    return link_text

def make_table_line(line_info):
    cell_text = []

    rowspan = ''
    if line_info['books'] > 1:
        rowspan = 'rowspan="%s" | ' % line_info['books']

    number_line = '| %s%s' % (rowspan, line_info['number'])
    cell_text.append(number_line)

    year_line = '| %s%s' % (rowspan, line_info['year'])
    cell_text.append(year_line)

    if line_info['no_prize']:
        cell_text.append('| colspan="3" | премия не присуждалась')
        cell_text.append('|-')
    else:
        for i in range(line_info['books']):
            
            curr_author = line_info['authors'][i]
            author_line = '| %s' % (make_author_link(curr_author))
            cell_text.append(author_line)

            curr_title = line_info['titles'][i]
            title_line = '| %s' % (make_title_link(curr_title))
            cell_text.append(title_line)

            cell_text.append('| ')
            
            cell_text.append('|-')
  
    return '\n'.join(cell_text)
        
#------------------------------------------------------------------------------#
#                              LAUNCH SECTION                                  #
#------------------------------------------------------------------------------#

list_text = """*第11回（[[1959年]]） - [[正宗白鳥]] 『今年の秋』 ・ [[中野重治]] 『梨の花』
*第12回（[[1960年]]） - [[外村繁]] 『澪標』
*第13回（[[1961年]]） - 該当なし
*第14回（[[1962年]]） - [[安部公房]] 『[[砂の女]]』
*第15回（[[1963年]]） - [[井上靖]] 『風濤』
*第16回（[[1964年]]） - [[上林暁]] 『白い屋形船』
*第17回（[[1965年]]） - [[庄野潤三]] 『夕べの雲』
*第18回（[[1966年]]） - [[丹羽文雄]] 『一路』
*第19回（[[1967年]]） - [[網野菊]] 『一期一会』
*第20回（[[1968年]]） - [[河野多惠子]] 『不意の声』 ・ [[瀧井孝作]] 『野趣』"""

def cleanup(text):
    if (WIKI_LINK_PREFIX in text):
        if (WIKI_LINK_SUFFIX in text):
            begin = text.index(WIKI_LINK_PREFIX)
            end = text.index(WIKI_LINK_SUFFIX)
            sep = '|'
            if (sep in text[begin:end]):
                sep_pos = text.index(sep)
                print(begin, sep_pos, end)
                return text[:begin] + text[sep_pos+len(sep):end] + cleanup(text[end+len(WIKI_LINK_SUFFIX):])
            else:
                return text[:begin] + text[begin + len(WIKI_LINK_PREFIX):end] + cleanup(text[end+len(WIKI_LINK_SUFFIX):])
    else:
        return text


##t = cleanup('[[damn]] [[lol (shit)|lol]] blyat [[lol (fuck)|fuck]] [[go]] [[Нахуй - это туда!|away]]')
##print(t)
    
table_text = parse_text(list_text)
print(table_text)

