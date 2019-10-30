from document import Document

def tokenize(doc):
    tokens = set()
    for token in doc.content.lower().split():
        tokens.add(token)

    return tokens


if __name__ == "__main__":
    tokens = tokenize(Document(1,"abc xyz"))
    print("Tokens set: ",tokens)