import tokenizer
import inverted_idx

class BooleanModel:
    def __init__(self,docs):
        self.inverted_idx= inverted_idx.gen_inverted_idx(docs)

    operators = {
        "and": lambda a,b : set(a).intersection(set(b)),
        "or": lambda a,b : set(a).union(set(b)),
        "not": lambda a,b : set(a).difference(set(b)) 
        }

    def _evaluate(self,token,arg1,arg2):
        return self.operators[token](arg1,arg2)
        
    #simple parser
    def parse_query(self,query):
        tokens = tokenizer.tokenize_str(query)
        args = []
        ops = []
        for token in tokens:
            if (token in self.operators):
                ops.append(token)
            else:
                args.append(token)

        return args,ops

    def retrieve(self,query):
        args,ops = self.parse_query(query)
        if (len(args) == 0):
            return []

        result = []
        tmp = None

        if (len(ops) > 0 and ops[0] != "not"):
            tmp = args.pop(0)
    
        if (tmp in self.inverted_idx):
            result = self.inverted_idx[tmp].postings

        if (len(ops) > 0):
            for op in ops:
                tmp = args.pop(0)
                if (tmp in self.inverted_idx):
                    result = self._evaluate(op,result,self.inverted_idx[tmp].postings)
        else:
            for arg in args:
                if (arg in self.inverted_idx):
                    result = self._evaluate("or",result,self.inverted_idx[arg].postings)
        
        return list(result)




if __name__ == "__main__":
    model = BooleanModel({1:"abc xyz",2:"qwe abc xyz",3:"qwe",4:"xyz"})
    res = model.retrieve("abc OR xyz NOT qwe")
    print(res)