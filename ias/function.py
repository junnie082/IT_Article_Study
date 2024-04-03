def cmpArticleInput(input, article):
    input = input.replace(' ','')
    article = article.replace(' ','')
    if input == article:
        return True
    return False

