# Autor: Joanna Kamińska

import hashlib

PERSONAL = "personal.txt"
PERSONAL2 = "personal_.txt"
DIFFFILE = "diff.txt"
LECTURE = "hash-.pdf"

HASH_FUNCS = [
    ("md5sum", hashlib.md5, 128),
    ("sha1sum", hashlib.sha1, 160),
    ("sha224sum", hashlib.sha224, 224),
    ("sha256sum", hashlib.sha256, 256),
    ("sha384sum", hashlib.sha384, 384),
    ("sha512sum", hashlib.sha512, 512),
    ("b2sum", hashlib.blake2b, 512),
]

def read_file(path):
    with open(path, "rb") as f:
        return f.read()

def compute_hash(func, data):
    return func(data).hexdigest()

def bit_diff(hex1, hex2):
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    return sum(bin(x ^ y).count("1") for x, y in zip(b1, b2))

def main():
    lecture = read_file(LECTURE)
    p1 = read_file(PERSONAL)
    p2 = read_file(PERSONAL2)

    with open(DIFFFILE, "w", encoding="utf-8") as out:
        for name, func, bits in HASH_FUNCS:
            out.write(f"cat hash-.pdf personal.txt | {name}\n")
            out.write(f"cat hash-.pdf personal_.txt | {name}\n")

            h1 = compute_hash(func, lecture + p1)
            h2 = compute_hash(func, lecture + p2)

            out.write(h1 + "\n")
            out.write(h2 + "\n")

            diff = bit_diff(h1, h2)
            percent = round(diff / bits * 100)

            out.write(
                f"Liczba różniących się bitów: {diff} z {bits}, procentowo: {percent}%.\n\n"
            )

if __name__ == "__main__":
    main()