from pprint import pprint

from shared import *


WIKI_LINK_PREFIX = '[['
WIKI_LINK_SUFFIX = ']]'


#------------------------------------------------------------------------------#
#                               PARSE SECTION                                  #
#------------------------------------------------------------------------------#

def parse_text(text):
    table_lines = []
    for line_text in text.split('\n'):
##        print(line_text)
        line_info = parse_list_line(line_text)
        table_line = make_table_line(line_info)
        table_lines.append(table_line)

    return '\n'.join(table_lines)

def parse_number_year(number_year_chunk):
    number_begin_separator = '*第'
    number_end_separator = '回（'
    number = between(number_year_chunk,
                                  number_begin_separator,
                                  number_end_separator)

    year_begin_separator = '（[['
    year_end_separator = '年]]）'
    year = between(number_year_chunk,
                                year_begin_separator,
                                year_end_separator)

    return number, year

def parse_author_title(author_title_chunk):
    items_separator = '・'
    books = 0
    authors = []
    titles = []
    
    for item in author_title_chunk.split(items_separator):
##        print(item)
        author, title = item.split(' 『')
        title = title.strip().rstrip('』')

        authors.append(author)
        titles.append(title)
        
        books += 1

    return books, authors, titles

def parse_list_line(list_line_text):
    line_info = {
        'no_prize': False,
        'books': 1,
        'number': '0',
        'year': '1990',
        'authors': [],
        'titles': []
    }
    main_separator = ' - '
    no_prize = '該当なし'
    
    number_year_chunk, author_title_chunk = list_line_text.split(main_separator)

    number, year = parse_number_year(number_year_chunk)
    line_info['number'], line_info['year'] = number, year

    if (no_prize in author_title_chunk):
        line_info['no_prize'] = True
    else:
##        print(author_title_chunk)
        books, authors, titles = parse_author_title(author_title_chunk)

        line_info['books'] = books
        line_info['authors'] = authors
        line_info['titles'] = titles

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

list_text = """*第1回（[[1949年]]） - [[井伏鱒二]] 『本日休診』他
*第2回（[[1950年]]） - [[宇野浩二]] 『思ひ川』
*第3回（[[1951年]]） - [[大岡昇平]] 『[[野火 (小説)|野火]]』
*第4回（[[1952年]]） - [[阿川弘之]] 『春の城』
*第5回（[[1953年]]） - 該当なし
*第6回（[[1954年]]） - [[佐藤春夫]] 『[[与謝野晶子|晶子]]曼陀羅』
*第7回（[[1955年]]） - [[里見とん|里見弴]] 『恋ごころ』 ・ [[幸田文]] 『黒い裾』
*第8回（[[1956年]]） - [[三島由紀夫]] 『[[金閣寺 (小説)|金閣寺]]』 ・ [[久保田万太郎]] 『三の酉』
*第9回（[[1957年]]） - [[室生犀星]] 『杏っ子』 ・ [[野上弥生子]] 『[[迷路 (野上弥生子の小説)|迷路]]』
*第10回（[[1958年]]） - 該当なし"""

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

