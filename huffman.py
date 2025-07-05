import heapq
import os
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    freq = Counter(text)
    heap = [Node(ch, freq[ch]) for ch in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)
        merged = Node(None, l.freq + r.freq)
        merged.left = l
        merged.right = r
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def encode_text(text, codebook):
    return ''.join(codebook[ch] for ch in text)

def pad_encoded(encoded):
    extra = 8 - len(encoded) % 8
    encoded += '0' * extra
    return "{0:08b}".format(extra) + encoded  

def binary_to_bytes(binary):
    return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))

def compress_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    root = build_tree(text)
    codebook = generate_codes(root)
    encoded = encode_text(text, codebook)
    padded = pad_encoded(encoded)
    byte_data = binary_to_bytes(padded)

    with open(output_path, 'wb') as f:
        f.write((str(codebook) + '\n').encode('utf-8'))
        f.write(byte_data)

    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    return original_size, compressed_size

def remove_padding(padded_binary):
    extra = int(padded_binary[:8], 2)
    return padded_binary[8:-extra] if extra > 0 else padded_binary[8:]

def decode_text(binary, codebook):
    reversed_codebook = {v: k for k, v in codebook.items()}
    current = ''
    decoded = ''
    for bit in binary:
        current += bit
        if current in reversed_codebook:
            decoded += reversed_codebook[current]
            current = ''
    return decoded

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        lines = f.readlines()

    codebook = eval(lines[0].decode('utf-8').strip())  
    byte_data = b''.join(lines[1:])
    binary = ''.join(f'{byte:08b}' for byte in byte_data)
    unpadded = remove_padding(binary)
    decoded = decode_text(unpadded, codebook)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decoded)
