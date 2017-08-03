def between(text, begin, end):
    result = text.split(begin)[1]
    result = result.split(end)[0]

    return result

def transmut(inp):
	name_surname = between(inp, '{{jl|', '}}')
	name, surname = name_surname.split('|')
	return '{{нп3|%s, %s|%s %s|ja|}}' % (surname, name, name, surname)

l1 = ['{{jl|Кадзуко|Саэгуса}}',
    '{{jl|Кадзуэ|Мацубара}}',
    '{{jl|Миёси|Энацу}}',
    '{{jl|Фусако|Хонда}}',
    '{{jl|Момоко|Хироцу}}',
    '{{jl|Акико|Эсаси}}',
    '{{jl|Рин|Исигаки}}',
    '{{jl|Сэй|Ёсино}}',
    '{{jl|Ая|Итиносэ}}',
    '{{jl|Ясуко|Киги}}',
    '{{jl|Момоко|Такэда}}']

tr = {}
for item in l1:
    tr[item] = t(item)

text = """"""

for item in l1:
    text = text.replace(item, tr[item])

with open('e:/file.txt', 'w', encoding='utf-8') as fh:
     fh.write(text)