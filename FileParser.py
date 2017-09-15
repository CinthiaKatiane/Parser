#!/usr/bin/python 
import ast
import os
import glob

# Aux Function to get the name of a node
class FunctionName():
    
    def get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        else:
            raise NotImplementedError("Could not extract call-name from node: " + str(node))

#Function to get the RFC Metric
class Metric_RFC(ast.NodeVisitor):

    def __init__(self):
        self.dict_rfc = {}
        self.rfc = 0

    def visit_ClassDef(self, node):
        self.rfc = 0
        super(Metric_RFC, self).generic_visit(node)
        self.dict_rfc[node.name] = self.rfc

    def visit_FunctionDef(self, node):
        self.rfc = self.rfc + 1
        super(Metric_RFC, self).generic_visit(node)

    def visit_Call(self,node):
        self.rfc = self.rfc + 1        
        super(Metric_RFC, self).generic_visit(node)
'''
#Function to get the NOC Metric
class Metric_NOC(ast.NodeVisitor):

    def __init__(self):
        self.noc = 0 
        self.list_noc = []

    def visit_ClassDef(self, node):
        self.noc = 0
        self.list_noc = node.name
        print self.list_noc
        if (issubclass(node.__class__ , ast.Bases)):
            print "subclass"
        else: 
            pass
        super(Metric_NOC, self).generic_visit(node)
'''
# -------------------------------------------------------------------------------------------- #
class FunctionDefVisitor(ast.NodeVisitor):
    def __init__(self):
        self.dictfun = {}

    def visit_FunctionDef(self, node):
        print("\tFunction '{0}' was defined.".format(node.name))
        super(FunctionDefVisitor, self).generic_visit(node)
        #print self.dictfun
        self.dictfun = {}

    def visit_Call(self,node):
        call_name = FunctionName().get_call_name(node)
        print(str("\t\t'{0}' was called.").format(call_name))
        self.dictfun[call_name] = self.dictfun.get(call_name , 0) + 1
        super(FunctionDefVisitor, self).generic_visit(node)


class MyCustomVisitor(ast.NodeVisitor):
    
    def __init__(self):
        self.counterTotal = 0 #Keeps the number of function calls
        self.counterDefinition = 0 #Keeps the number of defined functions in the file
        self.counterFunction = 0 #Keeps the number of function calls inside a defined function 
        self.dictdef = {}
        self.dictfun = {}

    # Aux function
    def get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        else:
            raise NotImplementedError("Could not extract call-name from node: " + str(node))

    def visit_Call(self, node):
        self.counterTotal = self.counterTotal + 1
        self.counterFunction = self.counterFunction + 1
        call_name = self.get_call_name(node)
        print(str("\t\t'{0}' was called.").format(call_name))
        self.dictfun[call_name] = self.dictfun.get(call_name , 0) + 1
        super(MyCustomVisitor, self).generic_visit(node)

    def visit_ClassDef(self, node):
        print("Class '{0}' was defined.".format(node.name))
        super(MyCustomVisitor, self).generic_visit(node)
    
    def visit_FunctionDef(self, node):
        self.dictdef[node.name] = self.dictfun
        self.counterFunction = 0 #Restart the counter to get de quantity in a specfic defined function
        self.counterDefinition = self.counterDefinition + 1
        print("\tFunction '{0}' was defined.".format(node.name))
        super(MyCustomVisitor, self).generic_visit(node)
        print("\tA total of {0} function calls were found in {1}.\n".format(visitor.counterFunction, node.name))
        print self.dictdef[node.name]     

if __name__ == "__main__":

    import sys
    input_path = []
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
        for root, dirs, files in os.walk("./"):
            file = glob.glob(root + '/*.py')
            if (len(file)is not 0) :
                input_path.append(file)
            else:
                pass
    else :
        input_path =  glob.glob('*/*.py')

    for f in input_path:
        for l in f:
            print("\nProcessing file: " + l)
            with open(l, "r") as input:

                # reads the content of this file
                file_str  = input.read()
                # parses the content of this file
                root = ast.parse(file_str)
                # visits the Abstract Syntax Tree
                #visitor = Metric_RFC()
                visitor = Metric_NOC()
                visitor.visit(root)
                #print visitor.dict_rfc