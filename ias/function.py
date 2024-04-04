def preprocess_text(text):
    # Replace curly apostrophes with straight apostrophes
    return text.replace('’', "'")


def cmpInputArticle(input, article):
    input = preprocess_text(input.replace(' ', ''))
    article = preprocess_text(article.replace(' ', ''))
    if input == article:
        return True
    return False

def chkErrors(input, article):
    inputList = list(input.split())
    articleList = list(article.split())
    returnList = list()

    for index in range(len(articleList)):
        word = ""

        if index >= len(inputList):
            for i in range(len(articleList[index])):
                word += '@'
            print("word: " + word)

        else:
            for i in range(len(articleList[index])):
                if i >= len(inputList[index]):
                    word += '@'
                elif inputList[index][i] == "'" and articleList[index][i] == "’":
                    word += inputList[index][i]
                elif inputList[index][i] != articleList[index][i]:
                    word += '@'
                else:
                    word += inputList[index][i]

        returnList.append(word)
        print("returnList: " + str(returnList))

    return returnList




