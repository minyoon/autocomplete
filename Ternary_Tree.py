#!/usr/bin/env python
"""
    Ternary Search Tree implementation
    https://github.com/minyoon0205/autocomplete
    Special thanks to
    https://www.cs.upc.edu/~ps/downloads/tst/tst.html
    https://www.youtube.com/watch?v=CIGyewO7868
"""
__author__ = "Minyoon Jung"
__credits__ = ["Igor Ostrovsky"]

__maintainer__ = "Minyoon Jung"

class Ternary_Tree:
    """
        Tree Node for the ternary tree
    """
    class Tree_Node:
        def __init__(self, label="", isEnd=False):
            self.label = label
            self.left, self.mid, self.right = None,None,None
            self.isEnd = isEnd


    """
        Basic constructor
    """
    def __init__(self):
        # serves up as root node
        self.root = None 


    """
        Helper method for adding a word
        which recursively travels down the tree
    """
    def add(self, s, pos, node):
        if node==None:
            node = self.Tree_Node(s[pos], False)
        if s[pos] < node.label:
            node.left = self.add(s, pos, node.left)
        elif s[pos] > node.label:
            node.right = self.add(s, pos, node.right)
        else:
            if pos+1 == len(s):
                node.isEnd = True
            else:
                node.mid = self.add(s, pos+1, node.mid)
        return node

    """
        Add a word into the tree
    """
    def add_word(self, word):
        assert word not in [None, ""]
        """
            Convert the word into the capital letters
        """
        word = word.upper()
        root_node=self.add(word, 0, self.root)
        # assign it to root, if not initialized
        if self.root == None:
            self.root=root_node

    """
        checks if the input word is used to build the tree
        It has to be the exact original word used for the construction
    """
    def contains(self, word):
        if word == None or word == "":
            return False
        word = word.upper()
        pos = 0 # position of a char
        node = self.root # cursor
        while node!=None:
            if node.label > word[pos]:
                node = node.left
            elif node.label < word[pos]:
                node = node.right
            else:
                pos+=1
                if pos == len(word):
                    return node.isEnd
                node = node.mid
        return False

    """
        Autofills the given prefix
        Assumes the prefix is already found in the list
    """
    def autofill(self, pref):
        pref = pref.upper()
        node = self.root 
        # nodes that is lexicographically greater than or equal to
        # need this to backtrack
        stack = []
        print_set = []
        pos = 0
        if len(pref)>0:
            while node!=None and pos<len(pref):
                # add right child up
                stack+=[(node.right, pref[:pos])]
                # add mid child, with additional character label
                stack+=[(node.mid, pref[:pos+1])]
                # left child is not needed, because it's lexicographically smaller than the input
                if node.label > pref[pos]:
                    node = node.left
                elif node.label < pref[pos]:
                    node = node.right
                else: # in this case, we found a match, so we dont need to backtrack to this point again
                    # thus, pop the stack by one
                    stack=stack[:-1] 
                    pos+=1
                    node = node.mid
            print_set += [pref]
        num_suggestion = 5 # number of suggestions
        stack+=[(node, pref)] # add the subtree to be searched
        print_set += self.root_to_leaves(node, stack, num_suggestion)
        return print_set


    """
        return all the root to leaves path
        limit the number by 'num'
    """
    def root_to_leaves(self, root, stack, num=5):
        new_visited = []
        print_set = []
        while stack and len(print_set)<num:
            node, label = stack.pop()
            if node!=None and node not in new_visited: 
                new_visited.append(node)
                stack += [(node.right, label)]
                stack += [(node.mid, label+node.label)]
                stack += [(node.left, label)]
                if node.isEnd:
                    label += node.label
                    print_set+=[label]
        return print_set

    
    """
        prints the tree in pre-order
    """
    def print_tree(self):
        self.print_tree_helper(self.root,0, 'ROOT')

    def print_tree_helper(self, node, depth=0, ori=''):
        if node!=None:
            print '\t'*depth+str(node.label) + ' at '+ori
            self.print_tree_helper(node.right, depth+1,'right')
            self.print_tree_helper(node.mid, depth+1, 'mid')
            self.print_tree_helper(node.left, depth+1, 'left')
        

if __name__=="__main__":
    tt = Ternary_Tree()
    tt.add_word('ABBA')
    tt.add_word('ABCD')
    tt.add_word('AB')
    tt.add_word('ant')
    tt.add_word('BCD')
    tt.add_word('banana')
    tt.add_word('baby')
    assert tt.contains('an') == False
    assert tt.contains('ant') == True
    assert tt.contains('abc') == False
    assert tt.contains('ab') == True
    tt.autofill('AB')
    tt.autofill('')
    tt.print_tree()
