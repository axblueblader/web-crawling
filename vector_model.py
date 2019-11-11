import tokenizer
import inverted_idx
import tf
import idf
import scraper
from numpy import dot
from numpy.linalg import norm
from numpy import reshape
import numpy as np

def cosine(vector1, vector2):
        return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

def list_to_dict(lst): 
    res_dct = { i : lst[i] for i in range(0, len(lst) ) }
    return res_dct 

class VectorModel:
    def __init__(self,docs):
        self.inverted_idx = inverted_idx.gen_inverted_idx(docs)
        self.docs = docs
        self._convert_to_vectors()

    def _convert_to_vectors(self):
        tf_vector = []
        idf_vector = []
        tf_dict = tf.calculate(self.inverted_idx,self.docs)
        idf_dict = idf.calculate(self.inverted_idx,self.docs)
        sorted_term = sorted(self.inverted_idx)
        # print(sorted_term)
        for term in sorted_term:
            tf_vector.append(list(tf_dict[term].values()))
            idf_vector.append(idf_dict[term])
        # print("TF: ",(tf_vector))
        # print("IDF: ",(idf_vector))
        # print('doc vector', (np.array(tf_vector) * np.array(idf_vector)[:, np.newaxis]))
        # self.doc_vectors = reshape(tf_vector,(len(self.docs),len(sorted_term))) * idf_vector
        self.doc_vectors = (np.array(tf_vector) * np.array(idf_vector)[:, np.newaxis]).T
        # print(self.doc_vectors)

    def retrieve(self,query):
        query_vector = []
        terms = tokenizer.termize_doc(query)
        all_zero = True
        for t in sorted(self.inverted_idx):
            if (t in terms):
                query_vector.append(1)
                all_zero = False
            else:
                query_vector.append(0)
        if (all_zero == True):
            result = [0] * len(self.docs)
        else:
            result = [cosine(query_vector,doc_vector) for doc_vector in self.doc_vectors]
        res_dict = list_to_dict(result)
        result = scraper.sorted_descending(res_dict)
        print("Top 5 results: ",[item[0] for item in result][:5])
        return result

if __name__ == "__main__":
    docs = docs = {
        "0": "abc alo ola 456 zzz ola all",
        "1": "alo ola 321 123 all",
        "2": "hello 123 456 123 all",
        "3": "hello alo ola abc 123 456 zzz all",
        "4": "123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 123 all"
    }
    model = VectorModel(docs)
    res = model.retrieve("123")
    print(res)