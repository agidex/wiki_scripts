import codecs

PRINT_NONE = True

LINK_PREFIX = 'https://fantlab.ru'

FILE_PATH = "e:/komatsu_sakyo.htm"

enries_list = []

book_dict = {
    'original_name': '',
    'russian_name': '',
    'romaji_name': '',
    'year':0,
    'type':''
    }

def between(text, begin, end):
    result = text.split(begin)[1]
    result = result.split(end)[0]

    return result


def parse_entry(entry):
    book = {
        'ru_name': None,
        'jp_name': '',
        'romaji_name': '',
        'link': '',
        'year':0,
        'type':''
        }
    
    title_chunk_begin = '<div class="title">'
    title_chunk_end = '</div>'
    title_chunk = between(entry, title_chunk_begin, title_chunk_end)

    title_link_begin = '<a href='
    title_link_end = '</a>'
    title_link = between(title_chunk, title_link_begin, title_link_end)
    
    link = between(title_chunk, '"', '"')
    book['link'] = LINK_PREFIX + link

    titles_string = title_link.split('>')[1]
    title_separator = ' / '
    titles = titles_string.split(title_separator)

    if (len(titles) == 3):
        book['ru_name'],  book['jp_name'], book['romaji_name'] = titles
    elif (len(titles) == 2):
        book['jp_name'], book['romaji_name'] = titles
        
    
    year_chunk_begin = '<div class="plus">'
    year_chunk_end = '</div>'

    year_chunk = between(entry, year_chunk_begin, year_chunk_end).strip()
    
    year_separator = ', '
    year_type = year_chunk.split(year_separator)
    if (len(year_type) == 2):
        book['year'], book['type'] = year_type
        book['year'] = int(book['year'])
    else:
        book['type'], = year_type
    
    return book

    
def parse_file(file_path):
    with codecs.open(file_path, encoding='utf-8') as file_handler:
        file_text = file_handler.read()

        # main separator (located at the end of each entry)
        separator_main = '<div class="one-line-spaced"><div class="line"></div></div>'
        # 
        separator_2 = '<div class="search-block works">'

        enries_list = file_text.split(separator_main)
        
        # delete last item
        enries_list.pop()

        # fix up first item
        zero_item = enries_list[0]
        zero_item = zero_item.split(separator_2)[-1]
        enries_list[0] = zero_item

    return enries_list

def make_table(books, book_type):
    
    books_by_type = list(filter(lambda book: book['type'] == book_type, books))
    books_by_type.sort(key = lambda book: book['year'])
    
    text_list = []
    text_list.append('{| class="wikitable"')
    text_list.append('|+')
    text_list.append('|-')
    text_list.append('! №')
    text_list.append('! Год')
    text_list.append('! Название')
    text_list.append('! Оригинальное название')
    text_list.append('! Примечания')
    text_list.append('|-')

    i = 0
    for book in books_by_type:
        i += 1
        text_list.append('| %s' % i)
        text_list.append('| %s' % book['year'])
        if (PRINT_NONE):
            text_list.append('| %s' % book['ru_name'])
        else:
            text_list.append('| %s' % book['ru_name'] if book['ru_name'] else '| ')
        text_list.append('| %s<br>%s' % (book['jp_name'], book['romaji_name']))
        text_list.append('| <ref>%s</ref>' % book['link'])
        text_list.append('|-')

    text_list.append('|}')

    return '\n'.join(text_list)

def process_file(file_path):
    entries = parse_file(file_path)
    books = []
    for e in entries:
        books.append(parse_entry(e))

    listtype = 'роман'
    listtype = 'повесть'
    listtype = 'рассказ'
    table_text = make_table(books, listtype)
    print(table_text)

if __name__ == '__main__':
    process_file(FILE_PATH)


















