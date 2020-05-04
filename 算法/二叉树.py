# 二叉树代码实现

# add方法： 建一个队列，把父节点添加进去，
#           从队列里pop一个，
#           判断左子节点，如果为none，把需要添加的值赋给它，结束运行，如果有值，加入队列，当作父节点，等待pop，
#           判断右子节点，如果为none，把需要添加的值赋给它，结束运行，如果有值，加入队列，当作父节点，等待pop，
#           再pop一个


class Node():

    def __init__(self,item):
        self.node = item
        self.lchild = None
        self.rchild = None

class Tree():
    def __init__(self,item=None):
        if type(item) is int:
            item = Node(item)
        self.root = item

    def add(self,node):                                # 在树的末尾处添加一个
        if type(node) is int:
            node = Node(node)

        if self.root == None:
            self.root = node
            return
        queue = []                                     # 弄了个队列，很方便操作，很巧妙
        queue.append(self.root)
        while queue:
            snode = queue.pop(0)
            if snode.lchild == None:
                snode.lchild = node
                return
            else:
                queue.append(snode.lchild)
            if snode.rchild == None:
                snode.rchild = node
                return
            else:
                queue.append(snode.rchild)

    def breadth(self,node):                                # 广度优先
        if node == None:
            return
        print(node.node,end=' ')
        queue = []
        queue.append(self.root)
        while queue:
            snode = queue.pop(0)
            if snode.lchild:
                print(snode.lchild.node,end=' ')
                queue.append(snode.lchild)
            else:
                return
            if snode.rchild:
                print(snode.rchild.node,end=' ')
                queue.append(snode.rchild)
            else:
                return

    def preorder(self,node):                           # 先序
        if node == None:
            return
        else:
            print(node.node,end=' ')
            self.preorder(node.lchild)
            self.preorder(node.rchild)

    def inorder(self,node):                           # 中序
        if node == None:
            return
        else:
            self.inorder(node.lchild)
            print(node.node,end=' ')
            self.inorder(node.rchild)

    def postorder(self,node):                           # 后序
        if node == None:
            return
        else:
            self.postorder(node.lchild)
            self.postorder(node.rchild)
            print(node.node,end=' ')


    @property
    def querry(self):
        if self.root:
            queue = []
            queue.append(self.root)
            while queue:
                snode = queue.pop(0)
                if snode.lchild == None:
                    return snode
                else:
                    queue.append(snode.lchild)
                if snode.rchild == None:
                    return snode.lchild
                else:
                    queue.append(snode.rchild)







#
# node2 = Node(2)
# node3 = Node(3)
# node4 = Node(4)
# node5 = Node(5)

tree = Tree()
tree.add(0)
tree.add(1)
tree.add(2)
tree.add(3)
tree.add(4)
tree.add(5)
tree.add(6)
tree.add(7)
tree.add(8)
tree.add(9)

print(tree.querry.node)
tree.preorder(tree.root)
print('')
tree.inorder(tree.root)
print('')
tree.postorder(tree.root)
print('')
tree.breadth(tree.root)