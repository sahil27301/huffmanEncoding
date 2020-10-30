from tkinter.filedialog import askopenfilename

import os

file_to_decompress = askopenfilename()
filename, file_extension = os.path.splitext(file_to_decompress)


def remove_padding(padded_encoded_text):

    # The length of the padding is stored in the first 8 bits
    padded_info = padded_encoded_text[:8]
    # Convert it to decimal
    extra_padding = int(padded_info, 2)

    # Remove the first 8 bits
    padded_encoded_text = padded_encoded_text[8:] 

    # Take the string upto the padding
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text


def decode_text(encoded_text, data):

    current_code = ""
    decoded_text = ""

    for bit in encoded_text:

        # Add bit by bit and build the current code
        current_code += bit

        # If the current code matches a dictionary key, decode it
        if(current_code in data):

            character = data[current_code]

            # Add the character to the message string
            decoded_text += character

            # Reset the current_code to empty
            current_code = ""

    return decoded_text

def get_dictionary(bit_string):

    # The dictionary length is stored in the first 32 bits
    dict_length = int(bit_string[:32], 2)

    # Remove the first 32 bits
    bit_string = bit_string[32:]

    # Get the dictionary by taking the first dict_length characters
    dictionary = bit_string[:dict_length]

    #Get the message by taking the rest of the characters
    bit_string = bit_string[dict_length:]

    #Now, we have to decode the dictionary
    dictionary_string = ''

    for i in range(0, len(dictionary), 8):
        dictionary_string += chr(int(dictionary[i:i+8],2))
    
    # Eval evaluates a string as code
    dictionary = eval(dictionary_string)

    return dictionary, bit_string


filename = filename[:filename.rfind("_compressed")]
with open(filename+'_compressed.bin', 'rb') as file, open(filename+'_decompressed.txt', 'w') as output:
    bit_string = ""

    byte = file.read(1)
    while(byte):
        # ord -> ascii
        byte = ord(byte)
        # convert the ascii to binary, rempve the '0b', and pad to 8 bits
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits
        byte = file.read(1)


    dictionary, bit_string = get_dictionary(bit_string)

    encoded_text = remove_padding(bit_string)

    decompressed_text = decode_text(encoded_text, dictionary)
    
    output.write(decompressed_text)
