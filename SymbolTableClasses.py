class STNode:
    """
    self.parent: Node, parent of this node
    self.symbols: symbols is a dictionary with the following structure Key(= the identifier): list=[Type, const (bool),declarator node]
    self.scopename: name of scope
    """

    def __init__(self, scopename, parent=None):
        self.scopename = scopename
        self.parent = parent
        self.symbols = {"printf":["None", True, None],"scanf":["None", True, None]}
        self.fct_declarations = {"None": ["None", list]}


class STFunction(STNode):
    def __init__(self, scopename, parent=None, returntype=""):
        super().__init__(scopename, parent)
        self.type = returntype
        self.got_returntype = False
        self.types = []


class STifstatement(STNode):
    def __init__(self, scopename, parent=None):
        super().__init__(scopename, parent)


class STwhilestatement(STNode):
    def __init__(self, scopename, parent=None):
        super().__init__(scopename, parent)


class STforloop(STNode):
    def __init__(self, scopename, parent=None):
        super().__init__(scopename, parent)
