"""
    Ternary Search Tree implementation
    Special thanks to
    https://github.com/minyoon0205/autocomplete
    https://www.cs.upc.edu/~ps/downloads/tst/tst.html
    https://www.youtube.com/watch?v=CIGyewO7868
"""

class Ternary_Tree:
    """
        Tree Node for the ternary tree
    """
    class Tree_Node:
        def __init__(self, label="", isEnd=True):
            self.label = label
            self.left, self.mid, self.right = None,None,None
            self.isEnd = isEnd

    # Constructor
    def __init__(self):
        # create a dummy node for root
        self.root = None 

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
        if self.root == None:
            self.root=root_node

    
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
    tt.add_word('BCD')
    tt.add_word('ABCD')
    tt.add_word('banana')
    tt.add_word('baby')
    tt.add_word('ant')
    tt.print_tree()
