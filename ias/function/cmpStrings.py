def preprocess_text(text):
    # Replace curly apostrophes with straight apostrophes
    text = text.replace('’', "'")
    # Remove commas
    text = text.replace(',', '')
    return text


def cmpInputArticle(input, article):
    input = preprocess_text(input.replace(' ', ''))
    article = preprocess_text(article.replace(' ', ''))
    if input == article:
        return True
    return False

def chkErrors(input, article):
    inputList = input.split()
    articleList = article.split()
    returnList = []


    for index in range(len(articleList)):
        if index >= len(inputList):
            word = ""
            for _ in range(len(articleList[index])):
                word += "@"
            returnList.append(word)
        elif inputList[index] == articleList[index]:
            returnList.append(articleList[index])
        else:
            word = ""
            for i, c in enumerate(articleList[index]):
                if i >= len(inputList[index]) or c != inputList[index][i]:
                    word += "@"
                else:
                    word += c
            returnList.append(word)

    return returnList
