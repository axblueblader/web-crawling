import math
import tokenizer
import inverted_idx

#Smooth scaling
def calculate(inverted_idx,documents):
    idf = {}
    doc_no = len(documents)
    for term in inverted_idx:
        idf[term] = 1 + math.log(doc_no/(1 + len(inverted_idx[term].postings)))
    return idf

if __name__ == "__main__":
    docs = {
        "0": "abc alo ola 456 zzz ola",
        "1": "alo ola 321 123",
        "2": "hello 123 456 123",
        "3": "hello alo ola abc 123 456 zzz",
        "4": "123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123"
    }
    inv_idx = inverted_idx.gen_inverted_idx(docs)

    res = calculate(inv_idx,docs)
    print(res)