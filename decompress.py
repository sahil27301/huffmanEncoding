import json

from tkinter.filedialog import askopenfilename

import os

file_to_decompress = askopenfilename()
filename, file_extension = os.path.splitext(file_to_decompress)


with open(filename+'_dictionary.txt') as f: 
    data = f.read() 
# data = ",\n".join(data.split(', '))
data = data.replace('\'', '"').replace('"""', '"\'""')
data = json.loads(data)


def remove_padding(padded_encoded_text):

    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:] 
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text


def decode_text(encoded_text):
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if(current_code in data):
            character = data[current_code]
            decoded_text += character
            current_code = ""

    return decoded_text

# newfile = filename.replace("_compressed", "")
filename = filename[:filename.rfind("_compressed")]
with open(filename+'_compressed.bin', 'rb') as file, open(filename+'_decompressed.txt', 'w') as output:
    bit_string = ""
    # print(file.read())
    byte = file.read(1)
    while(byte):
        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits
        byte = file.read(1)
    # print(bit_string)
    encoded_text = remove_padding(bit_string)

    decompressed_text = decode_text(encoded_text)
    
    output.write(decompressed_text)
