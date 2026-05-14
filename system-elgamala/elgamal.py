# Autor: Joanna Kaminska

import sys
import secrets
from math import gcd

ELGAMAL_FILE = "elgamal.txt"
PRIVATE_FILE = "private.txt"
PUBLIC_FILE = "public.txt"
PLAIN_FILE = "plain.txt"
CRYPTO_FILE = "crypto.txt"
DECRYPT_FILE = "decrypt.txt"
MESSAGE_FILE = "message.txt"
SIGNATURE_FILE = "signature.txt"
VERIFY_FILE = "verify.txt"

def read_two_ints_from_file(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 2:
        raise ValueError("Powinny być 2 linijki.")
    p = int(lines[0])
    g = int(lines[1])
    return p, g

def write_lines(filename, *values):
    with open(filename, "w") as f:
        for v in values:
            f.write(str(v) + "\n")

def modinv(a, m):
    a = a % m
    if a == 0:
        raise ZeroDivisionError("Nie ma inwersji.")
    lm, hm = 1, 0
    low, high = a, m
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % m

def gen_keys():
    p, g = read_two_ints_from_file(ELGAMAL_FILE)
    b = secrets.randbelow(p - 2) + 1
    beta = pow(g, b, p)
    write_lines(PRIVATE_FILE, p, g, b)
    write_lines(PUBLIC_FILE, p, g, beta)

def encrypt():
    with open(PUBLIC_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 3:
        raise ValueError("Powinny być 3 liczby.")
    p = int(lines[0])
    g = int(lines[1])
    beta = int(lines[2])

    with open(PLAIN_FILE, "r") as f:
        m = int(f.read().strip())

    if not (0 <= m < p):
        print("Error: m >= p", file=sys.stderr)
        sys.exit(1)

    k = secrets.randbelow(p - 2) + 1
    c1 = pow(g, k, p)
    c2 = (m * pow(beta, k, p)) % p
    write_lines(CRYPTO_FILE, c1, c2)

def decrypt():
    with open(PRIVATE_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 3:
        raise ValueError("Powinny być 3 liczby.")
    p = int(lines[0])
    g = int(lines[1])
    b = int(lines[2])

    with open(CRYPTO_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 2:
        raise ValueError("Powinny być 2 linijki.")
    c1 = int(lines[0])
    c2 = int(lines[1])

    s = pow(c1, b, p)
    s_inv = modinv(s, p)
    m = (c2 * s_inv) % p
    write_lines(DECRYPT_FILE, m)

def sign():
    with open(PRIVATE_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 3:
        raise ValueError("Powinny być 3 liczby.")
    p = int(lines[0])
    g = int(lines[1])
    b = int(lines[2])

    with open(MESSAGE_FILE, "r") as f:
        m = int(f.read().strip())

    if not (0 <= m < p):
        print("Error: m >= p", file=sys.stderr)
        sys.exit(1)

    phi = p - 1
    while True:
        k = secrets.randbelow(phi - 1) + 1
        if gcd(k, phi) == 1:
            break

    r = pow(g, k, p)
    k_inv = modinv(k, phi)
    x = ((m - b * r) * k_inv) % phi
    write_lines(SIGNATURE_FILE, r, x)

def verify():
    with open(PUBLIC_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 3:
        raise ValueError("Powinny być 3 liczby.")
    p = int(lines[0])
    g = int(lines[1])
    beta = int(lines[2])

    with open(MESSAGE_FILE, "r") as f:
        m = int(f.read().strip())

    with open(SIGNATURE_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if len(lines) < 2:
        raise ValueError("Powinny być 2 liczby.")
    r = int(lines[0])
    x = int(lines[1])

    left = pow(g, m, p)
    right = (pow(r, x, p) * pow(beta, r, p)) % p
    ok = (left == right)
    result = "T" if ok else "N"
    print(result)
    write_lines(VERIFY_FILE, result)

def main():
    if len(sys.argv) != 2:
        print("-k|-e|-d|-s|-v")
        sys.exit(1)

    opt = sys.argv[1]
    if opt == "-k":
        gen_keys()
    elif opt == "-e":
        encrypt()
    elif opt == "-d":
        decrypt()
    elif opt == "-s":
        sign()
    elif opt == "-v":
        verify()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()