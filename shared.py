def between(text, begin, end):
    result = text.split(begin)[1]
    result = result.split(end)[0]

    return result