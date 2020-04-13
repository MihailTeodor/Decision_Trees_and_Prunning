class Node:
  """ seen and pruned attributes are used in the prunning routine"""

  def __init__(self, label, children=None, seen=False, pruned=False):
        self.label = label
        self.children = {} if children == None else children
        self.seen = seen
        self.pruned = pruned

  def __str__(self):
        return str(self.label)

  def setLabel(self, label):
        self.label = label

  def setChild(self, children):
        if (isinstance(children, dict)):
            self.children = children

  def getLabel(self):
        return self.label

  def getChild(self):
        return self.children
