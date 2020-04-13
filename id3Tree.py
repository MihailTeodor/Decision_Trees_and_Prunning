from node import Node
import math
import copy
global T


def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    '''

    allAttr = list(examples[0].keys())
    globals()['T'] = allAttr[len(allAttr) - 1]
    sub = {}
    last = len(allAttr) - 1  # index of target[Class]
    vals = [i[T] for i in examples]
    if not examples or len(allAttr) == 0:
        return Node(default)
    elif vals.count(vals[0]) == len(vals):
        return Node(vals[0])
    else:
        best = chooseAttr(allAttr, examples, allAttr[last])
        t = Node(best, {})
        best_v = values(examples, best)
        for v in best_v:
            if v == '?':
                v = mode(examples, best)
            new_ex = newExample(examples, best, v)
            subtree = ID3(new_ex, mode(new_ex, T))
            sub.update({v: subtree})
            t.setChild(sub)

        return t


def mode(examples, target):
    '''
    returns the most common value for the target attribute among the examples
    '''

    freq = {}
    if len(examples) != 0:
        for j in examples:
            if(j[target] in freq):
                freq[j[target]] += 1
            else:
                freq[j[target]] = 1

        return max(freq, key=freq.get)


def values(examples, best):
    '''
    returns a list with all the possible values for the best attribute among the examples
    '''
    vals = []
    for e in examples:
        if e[best] not in vals:
            vals.append(e[best])
    return vals


def newExample(examples, best, best_v):
    '''
    returns a list with examples removing best attribute with value best_v from all examples
    '''
    result = []

    for e in examples:
        if e[best] ==best_v:
            copy = e.copy()
            del copy[best]
            result.append(copy)

    return result


def chooseAttr(allAttr, examples, target):
    '''
    chooses the best attribute based on the maximum gain
    '''
    best = allAttr[0]
    maxgain = 0
    new = 0.0
    for a in allAttr:
        if a != target:
            new = gain(examples, allAttr, a, target)
            if new > maxgain:
                maxgain = new
                best = a
    return best


def gain(examples, allAttr, a, target):
    '''
    calculate the information gain for the attribute a
    '''
    valfreq = {}
    subs_ent = 0.0
    for entry in examples:
        if((entry[a]) in valfreq):
            valfreq[entry[a]] += 1.0
        else:
            valfreq[entry[a]] = 1.0
    for val in valfreq.keys():
        valprob = valfreq[val] / sum(valfreq.values())
        subs = [entry for entry in examples if entry[a] == val]
        subs_ent += valprob * entropy(subs, allAttr, target)
    return(entropy(examples, allAttr, target) - subs_ent)


def entropy(examples, attributes, target):
    valfreq = {}
    entrop = 0.0
    i = 0
    for entry in attributes:
        if(target == entry):
            break
        i += 1
    a = attributes[i]
    for entry in examples:
        if((entry[a]) in valfreq):
            valfreq[entry[a]] += 1.0
        else:
            valfreq[entry[a]] = 1.0
    for freq in valfreq.values():
        entrop += (-freq/len(examples)) * math.log(freq / len(examples), 2)
    return entrop


def _manage_prune(node, validation_set, grow_set, nr_pruned_nodes=0):
    '''The heavy implementation of prunning method'''
    pruned_nodes = False
    iteration = True
    tmp_best_tree = copy.deepcopy(node)
    best_tree = node
    best_performance = test(node, validation_set)
    while iteration:
        iteration = False
        new_tree = copy.deepcopy(tmp_best_tree)
        iteration = _prune(new_tree, tmp_best_tree, grow_set, iteration)
        if iteration:
            new_performance = test(new_tree, validation_set)
            if new_performance >= best_performance:
                best_tree = new_tree
                best_performance = new_performance
                pruned_nodes = True
    reset_tree(best_tree)
    if pruned_nodes:
        nr_pruned_nodes += 1
        best_tree, best_performance, nr_pruned = _manage_prune(best_tree, validation_set, grow_set)
        nr_pruned_nodes += nr_pruned
    return best_tree, best_performance, nr_pruned_nodes


def reset_tree(node):
    node.pruned = False
    for child in node.children.keys():
        reset_tree(node.children[child])


def _prune(node, original_node, examples, pruned):

    if len(node.children) == 0:
        return pruned
    if node.pruned == True:
        return pruned

    if len(examples) == 0:
        node.children = {}
        node.label = mode(examples, T)
        return pruned

    subsets = subset(examples, node.label)

    for child in node.children.keys():
        if pruned == True:
            node.seen = False
            return pruned
        if node.children[child].children != {} and node.children[child].pruned != True:
            node.seen = True
        if child in subsets.keys():
            pruned = _prune(node.children[child], original_node.children[child], subsets[child], pruned)
        else:
            pruned = _prune(node.children[child], original_node.children[child], {}, pruned)
    if node.seen:
        node.seen = False
        pruned = True
        return pruned

    node.children = {}
    ex_label = node.label
    node.label = mode(examples, T)
    original_node.pruned = True
    pruned = True
    return pruned

def manage_prune(node, validation_set, grow_set):
    '''The light implementation of prunning'''
    nr_pruned_nodes = 0
    iteration = True
    best_tree = node
    best_performance = test(node, validation_set)
    while iteration:
        iteration = False
        new_tree = copy.deepcopy(best_tree)
        iteration = prune(new_tree, best_tree, grow_set, iteration)
        new_performance = test(new_tree, validation_set)
        if iteration and new_performance >= best_performance:
            best_tree = new_tree
            best_performance = new_performance
            nr_pruned_nodes += 1
    return best_tree, best_performance, nr_pruned_nodes


def prune(node, original_node, examples, pruned):

    if len(node.children) == 0:
        return pruned
    if node.pruned == True:
        return pruned

    if len(examples) == 0:
        node.children = {}
        node.label = mode(examples, T)
        return pruned

    subsets = subset(examples, node.label)

    for child in node.children.keys():
        if pruned == True:
            node.seen = False
            return pruned
        if node.children[child].children != {} and node.children[child].pruned != True:
            node.seen = True
        if child in subsets.keys():
            pruned = prune(node.children[child], original_node.children[child], subsets[child], pruned)
        else:
            pruned = prune(node.children[child], original_node.children[child], {}, pruned)
    if node.seen:
        node.seen = False
        pruned = True
        return pruned

    node.children = {}
    ex_label = node.label
    node.label = mode(examples, T)
    node.pruned = True
    original_node.pruned = True
    pruned = True
    return pruned

def subset(examples, label):
    '''return a subset of examples split in base the label value'''
    subsets = {}

    for instance in examples:
        if not instance[label] in subsets.keys():
            subsets[instance[label]] = [instance]
        else:
            subsets[instance[label]].append(instance)

    return subsets


def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''

    correct = 0
    total = 0

    for instance in examples:
        total += 1
        label = evaluate(node, instance)
        if label == instance[T]:
            correct += 1

    return float(correct) / float(total)


def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the target class value that the tree
    assigns to the example.
    '''
    nextNode = node
    while nextNode.getChild() != {}:
        templ = nextNode.getLabel()
        tempc = nextNode.getChild()
        if (example[templ]) in tempc:
            nextNode = tempc[example[templ]]
        else:
            # for cases not found, assign the first branch
            nextNode = tempc[list(tempc.keys())[0]]
    return nextNode.getLabel()


def get_tree_info(node, num_nodes=1):
    '''
    Takes in a tree and returns the number of nodes and the depth of the tree
    '''
    max_depth = 0
    deeper = False
    for child in node.children.keys():
        if node.children[child].children != {}:
            deeper = True
            num_nodes += 1
            num_nodes, _max_depth = get_tree_info(node.children[child], num_nodes)
            if _max_depth > max_depth:
                max_depth = _max_depth
    if deeper:
        max_depth += 1
    return num_nodes, max_depth
