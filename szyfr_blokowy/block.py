# Autor: Joanna Kamińska

from PIL import Image
import hashlib # md5 only

def md5_block(block):
    block_bytes = bytes(block)
    h = hashlib.md5(block_bytes).digest()
    extended = (h * 4)
    return list(extended)

img = Image.open("plain.bmp").convert("L")
pixels = img.load()
block_size = 8
width, height = img.size
blocks_per_row = width // 8
blocks = []

for y in range(0, height, block_size):
    for x in range(0, width, block_size):
        block = []
        for j in range(block_size):
            for i in range(block_size):
                if x+i < width and y+j < height:
                    block.append(pixels[x+i, y+j])
        blocks.append(block)

output_img = Image.new("L", (width, height))
output_pixels = output_img.load()

cipher_blocks = []
for block in blocks:
    cipher_block = [0 if v < 128 else 255 for v in md5_block(block)]
    cipher_blocks.append(cipher_block)

for l in range(len(cipher_blocks)):
    block_x = (l % blocks_per_row) * 8
    block_y = (l // blocks_per_row) * 8
    index = 0
    for j in range(8):
        for i in range(8):
            if block_x + i < width and block_y + j < height:
                output_pixels[block_x + i, block_y + j] = cipher_blocks[l][index]
                index += 1

output_img.save("ecb_crypto.bmp")

output_img = Image.new("L", (width, height))
output_pixels = output_img.load()

IV = [i * 3 % 256 for i in range(64)]
cbc_cipher_blocks = []
prev = IV[:]

for block in blocks:
    xored = [(block[i] ^ prev[i]) for i in range(64)]
    cipher_block = md5_block(xored)
    cipher_block = [0 if v < 128 else 255 for v in cipher_block]
    cbc_cipher_blocks.append(cipher_block)
    prev = cipher_block[:]
for l in range(len(cbc_cipher_blocks)):
    block_x = (l % blocks_per_row) * 8
    block_y = (l // blocks_per_row) * 8
    index = 0
    for j in range(8):
        for i in range(8):
            if block_x + i < width and block_y + j < height:
                output_pixels[block_x + i, block_y + j] = cbc_cipher_blocks[l][index]
                index += 1
output_img.save("cbc_crypto.bmp")