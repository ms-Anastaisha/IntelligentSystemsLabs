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
        self.resolved = False

    def __hash__(self):
        return hash(self.node)

    def __eq__(self, other):
        return isinstance(other, FactNode) and self.node == other.node

    @property
    def isResolved(self):
        return self.resolved or (
                len(self.childProductNodes) > 0 and any([node.resolved for node in self.childProductNodes]))


class SolutionTree:
    def __init__(self, init_facts, final_fact, products):
        self.root = FactNode(final_fact)
        self.products = products
        self.init_facts = init_facts

    def resolve(self):
        treeFacts = {self.root}
        visited = set()
        while len(treeFacts) > 0:
            fact = treeFacts.pop()
            visited.add(fact)
            for pname, pbody in self.products.items():
                if pbody[1] == fact.node:
                    productNode = ProductNode(pname, fact)
                    fact.childProductNodes.append(productNode)
                    for f in pbody[0]:
                        if fact in visited: continue
                        fnode = FactNode(f)
                        productNode.childFactNodes.append(fnode)
                        if f not in self.init_facts:
                            treeFacts.add(fnode)
                        else:
                            fnode.resolved = True
        if self.root.isResolved:
            return self._answer()
        return "unresolved"

    def _answer(self):
        answer = ""
        treeFacts = [self.root]
        while len(treeFacts) > 0:
            fact = treeFacts.pop(0)
            answer += fact.node + ' <= '
            if len(fact.childProductNodes) == 0:
                answer += "initial\n"
            else:
                for product in fact.childProductNodes:
                    if product.resolved:
                        for i in range(len(product.childFactNodes)):
                            answer += product.childFactNodes[i].node
                            treeFacts.append(product.childFactNodes[i])
                            if i < len(product.childFactNodes) - 1:
                                answer += ','
                        answer += '(' + product.node + ')\n'
                        break

        return answer
