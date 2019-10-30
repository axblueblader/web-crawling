from document import Document
import tokenizer

class InvertedIndex:
    def __init__(self):
        self.freq = 0
        self.postings = []

    def _increase_freq(self):
        self.freq += 1

    def add_new_posting(self,doc_id):
        if(doc_id in self.postings):
            return
        else:
            self.postings.append(doc_id)
            self._increase_freq()

def gen_inverted_idx(documents):
    inverted_idx = {}
    documents = sorted(documents, key = lambda x : x.id)
    for doc in documents:
        terms = tokenizer.tokenize(doc)
        for term in terms:
            if (not (term in inverted_idx)):
                inverted_idx[term] = InvertedIndex()
            inverted_idx[term].add_new_posting(doc.id)

    return inverted_idx

                

if __name__ == "__main__":
    result = gen_inverted_idx({Document(1,"abc xyz"),Document(2,"qwe abc xyz"),Document(3,"qwe"),Document(4,"xyz")})
    for item in result:
        print(item,result[item].freq,result[item].postings)