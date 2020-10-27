from tkinter.filedialog import askopenfilename

# To print tables
from tabulate import tabulate

import os

# Recursive function to get height of a node, height of leaves is 0
def height(node):

    if not node:
        return -1

    return 1 + max(height(node.left), height(node.right))

def is_leaf(node):
    return not node.left and not node.right

#Recursive function to print left subtree, right subtree and the node itself

# We will figure out 2 lines at a time, one line for the actual node, and the other one for the connection('/' or '\')

def _build_tree_string(root, curr_index):
    # For a None node, return empty representation, 0 width, height and start
    if root is None:
        return [], 0, 0, 0
    

    line1 = []
    line2 = []

    # The node representation is just the number at that node
    node_repr = str(root.value)

    # If it is a leaf node, also add the corresponding letter, which is mapped in the nodeToLetter dictionary
    if is_leaf(root):
        node_repr+='('+nodeToLetter[root]+')'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_tree_string(root.left, 2 * curr_index + 1)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_tree_string(root.right, 2 * curr_index + 2)


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


# The node class, used to build the tree
class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        lines = _build_tree_string(self, 0)[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))


# string = input("Enter the string: ")

file_to_compress = askopenfilename()
# print(filename)
filename, file_extension = os.path.splitext(file_to_compress)
output_path = filename + ".bin"

with open(filename+'.txt', 'r+') as file:
    string = file.read()
    string = string.rstrip()


# Dictionary to map the frequency of each character
dictionary = {}

# If the letter exists in the dictionary, increase it's count by one.
# If it does not exist, it will raise a KeyError
for letter in string:
    try:
        dictionary[letter] += 1
    except KeyError:
        dictionary[letter] = 1

# Make a list of all the letter and their frequency, so theycan be sorted easily
array = []
for key, value in dictionary.items():
    array.append([key, value])

# First, try sorting on the basis of the frequency, in ascending order.
# If the frequecy is the same, give preference to whatever came first in the input, i.e., whatever has a lower index in 'string'
array.sort(key = lambda x:[x[1], string.find(x[0])])

# Show the sorted array of characters and their frequency
print()
print(tabulate(array, headers = ["Letter", "Frequency"], tablefmt = "pretty"))

# Now, we need to make a node out of each letter.
# We can store all these nodes in an array (arrayOfNodes)
# Since only the frequency is being stored in the node, 
# we need to create another dictionary to map each node to the letter
# to remember which node corresponds to which letter. 
# We do this using the nodeToLetter dictionary.
arrayOfNodes = []
nodeToLetter = {}

# For every letter, frequency pair in array, we create a node from the frequency,
# and then map the newly created node to the corresponding letter using the dictionary
for x in array:
    arrayOfNodes.append(Node(x[1]))
    nodeToLetter[arrayOfNodes[-1]] = x[0]

# Main logic, keep merging the nodes with lowest frequencies till you a single tree.

while len(arrayOfNodes) > 1:

    # Initially, arrayOfNodes has the same order as array, so it is sorted
    # create a new node by taking the sum of the 2 smallest nodes
    newNode = Node(arrayOfNodes[0].value + arrayOfNodes[1].value)

    # Assign these two nodes as the left and right child of the new node respectively,
    #  after removing them from arrayOfNodes 
    newNode.left = arrayOfNodes.pop(0)
    newNode.right = arrayOfNodes.pop(0)

    # Add the newNode to the end of arrayOfNodes
    arrayOfNodes.append(newNode)

    # Display the newly created node
    print(newNode)

    # Now, we need to sort the array again, since the newNode needs to be adjusted
    # First, we will sort omn the basis of the node value (frequency)
    # If the node value is the same, we will give priority to whatever was merged earlier
    # Since merging increases the height, we can simply select the one with the greater height first
    arrayOfNodes.sort(key = lambda x:[x.value, -height(x)])

# Finally, we need to map the new Huffman encoded representation to each letter
# That can be done in the encodedDictionary dictionary
encodedDictionary={}

#variable to store the final length of the huffman encoded string
final_size=0

# Following is a recursive function to get the path of each leaf (1s and 0s)
# We will start with an empty string, and keep adding 1 or 0 depending on whether we go left or right.
# Once we reach a leaf node, we can assign whatever is stored in the string and map it to the respective letter

def traverse(_str, node):

    # We will be modifying the final size variable here, so we declare it as a global variable
    global final_size

    # If we hit a leaf node, 
    if not node.left and not node.right:

        # We now need to map the string to the letter
        # We can get the letter asssociated with the string using the nodeToLetter dictionary we created earlier
        # We will store this relation in the encodedDictionary dicionary
        encodedDictionary[nodeToLetter[node]] = _str

        # Each number takes 1 bit
        # The number of bits contributed by this particular string will be 
        # the frequency of that string(letter) multiplied by the length of the string
        final_size += len(_str)*dictionary[nodeToLetter[node]]

    # If a left subtree exists, add 0 to the current string and proceed
    if node.left:
        traverse(_str+'0', node.left)

     # If a right subtree exists, add 1 to the current string and proceed
    if node.right:
        traverse(_str+'1', node.right)

# Call the traverse function on the root, and start with an empty string
traverse('', arrayOfNodes[0])


# Handling the case where the input is only one character
if len(encodedDictionary) == 1:
    for key in encodedDictionary.keys():
        encodedDictionary[key] = '1'
        final_size = 1


print()

# Now that we have the encodedDictionary, we can print the encoded representation of each character
# We need to convert a dictionary to a list to properly use tabulate
encodedDictionaryData = [[k,v] for k,v in encodedDictionary.items()]
print(tabulate(encodedDictionaryData, headers = ["Letter", "Coded Representation"], tablefmt = "pretty"))

# For the initial size, each char has 8 bit representation in ascii,
# so just multiply the string length by 8

initial_size=8*len(string)

print()

print(f'Initial size = {initial_size} bits.')

print()

print(f'Final size = {final_size} bits.')

print()

print ('The encoded string is: ')

print()

# Encoding the string using the dictionary
compressed_binary = ''
for letter in string:
    print(encodedDictionary[letter], end='')
    compressed_binary += encodedDictionary[letter]

print('\n')

# Displaying the compression ratio
print(f'The compression ratio is {round(initial_size/final_size, 3)}')

def pad_string(string):
    extra_padding = 8 - len(string) % 8
    for i in range(extra_padding):
        string += "0"

    padded_info = "{0:08b}".format(extra_padding)
    string = padded_info + string
    return string

def get_byte_array(string):
    b = bytearray()
    for i in range(0, len(string), 8):
        byte = string[i:i+8]
        b.append(int(byte, 2))
    return b

with open(filename+'_compressed.bin', 'wb+') as output:
    padded_string = pad_string(compressed_binary)
    byte_array = get_byte_array(padded_string)
    output.write(bytes(byte_array))


reversedDictionary = {}
for key, value in encodedDictionary.items():
    reversedDictionary[value] = key
with open(filename+'_compressed_dictionary.txt', 'w') as file:
    print(reversedDictionary, file=file)

