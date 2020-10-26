# Recursive function to get height of a node, height of leaves is 0

def height(node):

    if not node:
        return -1

    return 1 + max(height(node.left), height(node.right))

def is_leaf(node):
    return not node.left and not node.right

#Recursive function to print left subtree, right subtree and the node itself

def _build_tree_string(root, curr_index, delimiter='-'):
    # For a None node, return empty representation, 0 width, height and start
    if root is None:
        return [], 0, 0, 0
    

    line1 = []
    line2 = []

    node_repr = str(root.val)

    if is_leaf(root):
        node_repr+='('+nodeToLetter[root]+')'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_tree_string(root.left, 2 * curr_index + 1, delimiter)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_tree_string(root.right, 2 * curr_index + 2, delimiter)


    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


class Node():
    def __init__(self, value, left=None, right=None):
        self.value = self.val = value
        self.left = left
        self.right = right

    def __str__(self):
        lines = _build_tree_string(self, 0, '-')[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))


string = input("Enter the string: ")


dictionary = {}


for letter in string:
    try:
        dictionary[letter] += 1
    except:
        dictionary[letter] = 1


array = []
for key, value in dictionary.items():
    array.append([key, value])

array.sort(key = lambda x:[x[1], string.find(x[0])])

print(array)

# arrayOfNodes = [Node(x[1]) for x in array]
arrayOfNodes = []
nodeToLetter = {}

for x in array:
    arrayOfNodes.append(Node(x[1]))
    nodeToLetter[arrayOfNodes[-1]] = x[0]

while len(arrayOfNodes) > 1:
    newNode = Node(arrayOfNodes[0].value + arrayOfNodes[1].value)
    newNode.left = arrayOfNodes.pop(0)
    newNode.right = arrayOfNodes.pop(0)
    arrayOfNodes.append(newNode)
    print(newNode)
    arrayOfNodes.sort(key = lambda x:[x.value, -height(x)])

encodedDictionary={}

final_size=0
def traverse(_str, node):
    global final_size
    if not node.left and not node.right:
        # print(nodeToLetter[node]+' = '+_str)
        encodedDictionary[nodeToLetter[node]] = _str
        # Frequency * length
        final_size += len(_str)*dictionary[nodeToLetter[node]]
    if node.left:
        traverse(_str+'0', node.left)
    if node.right:
        traverse(_str+'1', node.right)

traverse('', arrayOfNodes[0])

for key, value in encodedDictionary.items():
    print(key + ' = ' + value)

#Initial size

initial_size=8*len(string)

print()

print(f'Initial size = {initial_size} bits.')

# For each letter
final_size += 8 * len(dictionary)

# For frequency
final_size += sum(dictionary.values())

print()

print(f'Final size = {final_size} bits.')

print()

print(f'We saved {initial_size-final_size} bits for you' if initial_size>final_size else 'HUFFMAN NOT OPTIMAL :(')

print()

print ('The encoded string is: ')

print()

for i in string:
    print(encodedDictionary[i], end='')