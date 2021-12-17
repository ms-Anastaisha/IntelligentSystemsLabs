class ProductNode:
    def __init__(self, product, factNode):
        self.node = product
        self.childFactNodes = []
        self.parentFactNode = factNode

    @property
    def resolved(self):
        return len(self.childFactNodes) > 0 and all([node.resolved for node in self.childFactNodes])


class FactNode:
    def __init__(self, fact):
        self.node = fact
        self.childProductNodes = []
        self.parentProductNodes = []
        self.reasoning = []
        self.resFlag = False

    @property
    def resolved(self):
        return self.resFlag or (
                len(self.childProductNodes) > 0 and any([node.resolved for node in self.childProductNodes]))


class SolutionTree:
    def __init__(self, init_facts, final_fact, products, fact_explanations):
        self.root = FactNode(final_fact)
        self.products = products
        self.init_facts = init_facts
        self.fact_explanations = fact_explanations

    def resolve(self):
        treeFacts = {self.root}
        while len(treeFacts) > 0:
            fact = treeFacts.pop()
            for pname, pbody in self.products.items():
                if pbody[1] == fact.node:
                    productNode = ProductNode(pname, fact)
                    fact.childProductNodes.append(productNode)
                    for f in pbody[0]:
                        fnode = FactNode(f)
                        productNode.childFactNodes.append(fnode)
                        if f not in self.init_facts:
                            treeFacts.add(fnode)
                        else:
                            fnode.resFlag = True
        if self.root.resolved:
            return self._answer()
        return "unresolved"

    def _answer(self):
        answer = ""
        treeFacts = [self.root]
        while len(treeFacts) > 0:
            fact = treeFacts.pop(0)
            answer += 'Доказываемый факт: ' + self.fact_explanations[fact.node] + '\n <= Использованные факты: \n'
            if len(fact.childProductNodes) == 0:
                answer += "является стартовым\n"
            else:
                for product in fact.childProductNodes:
                    if product.resolved:
                        for i in range(len(product.childFactNodes)):
                            answer += self.fact_explanations[product.childFactNodes[i].node]
                            treeFacts.append(product.childFactNodes[i])
                            if i < len(product.childFactNodes) - 1:
                                answer += ', '
                        answer += ' (Продукция: ' + self.products[product.node][2] + ')\n\n'
                        break

        return answer
