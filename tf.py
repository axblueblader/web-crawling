import math
import tokenizer
import inverted_idx

#Sublinear TF scaling
def calculate(inverted_idx,documents):
    tf = {}
    terms_in_doc = {}
    for doc_id in documents:
        terms_in_doc[doc_id] = tokenizer.tokenize_str(documents[doc_id])

    for term in inverted_idx:
        tf[term] = {}
        for doc_id in documents:
            tf[term][doc_id] = 0
            for t in terms_in_doc[doc_id]:
                if (t == term):
                    tf[term][doc_id] += 1
    for term in tf:
        for doc_id in tf[term]:
            if (tf[term][doc_id] >0):
                tf[term][doc_id] = 1 + math.log10(tf[term][doc_id])
    return tf

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
