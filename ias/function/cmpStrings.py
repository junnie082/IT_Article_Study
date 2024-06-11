import string


def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    return text

def cmpInputArticle(input_text, article_text):
    input_processed = preprocess_text(input_text)
    article_processed = preprocess_text(article_text)
    print(input_processed)
    print(article_processed)
    if input_processed == article_processed:
        print("TRUE!!")
        return True
    print("FALSE!!")
    return False

def cal_hit(input):
    input_processed = input.errCheckedStr.replace(' ', '')
    article_processed = preprocess_text(input.ai.engContent)
    at_count = input_processed.count("@")
    len_article = len(article_processed)
    print("at_count: " + str(at_count) + "len_article: " + str(len_article))
    return round((len_article - at_count) / len_article * 100, 2)


at_count = 0

def chkErrors(input, article):
    # Helper function to strip punctuation
    def strip_punctuation(word):
        return word.translate(str.maketrans('', '', string.punctuation))

    inputList = input.split()
    articleList = article.split()
    returnList = []
    global at_count  # Initialize counter for "@" characters

    for index in range(len(articleList)):
        articleWord = strip_punctuation(articleList[index])

        if index >= len(inputList):
            # If input is shorter than article, append @ for each character of the article word
            word = "@" * len(articleWord)
            at_count += len(word)  # Count the number of "@" added
            returnList.append(word)
        else:
            inputWord = strip_punctuation(inputList[index])

            # Check if the current word in input is non-alphabet
            if not inputWord.isalpha():
                word = "@" * len(articleWord)
                at_count += len(word)  # Count the number of "@" added
                returnList.append(word)
            elif inputWord == articleWord:
                returnList.append(articleList[index])  # Keep original punctuation
            else:
                word = ""
                for i, c in enumerate(articleWord):
                    if i >= len(inputWord) or c != inputWord[i]:
                        word += "@"
                        at_count += 1  # Count each "@" added
                    else:
                        word += c
                returnList.append(word + articleList[index][len(articleWord):])  # Append original punctuation

    return returnList, at_count  # Return the list and the count of "@"


# Example usage
input_text = "This is a sample input"
article_text = "This is a simple example article"
result, at_count = chkErrors(input_text, article_text)
print("Result:", result)
print("Number of '@' characters:", at_count)
