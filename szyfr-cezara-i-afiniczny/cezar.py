def main():
    cipher = ""
    while cipher not in ["c", "a"]:
        print("Wybierz szyfr:")
        print("c - szyfr Cezara")
        print("a - szyfr afiniczny")
        cipher = input()
        if cipher not in ["c", "a"]:
            print("Niepoprawny wybór szyfru.")

    option = ""
    while option not in ["e", "d", "j", "k"]:
        print("Wybierz opcje:")
        print("e - szyfrowanie")
        print("d - odszyfrowywanie")
        print("j - kryptoanaliza z tekstem jawnym")
        print("k - kryptoanaliza wyłącznie w oparciu o kryptogram")
        option = input()
        if option not in ["e", "d", "j", "k"]:
            print("Niepoprawny wybór opcji.")

    if cipher == "c":
        if option == "e":
            caesar_encrypt()
        elif option == "d":
            caesar_decrypt()
        elif option == "j":
            caesar_cryptanalysis()
        else:
            caesar_cryptanalysis_without()
    else:
        if option == "e":
            affine_encrypt()
        elif option == "d":
            affine_decrypt()
        elif option == "j":
            print()
        else:
            print()

    print("Odpowiedzi znajduja sie w plikach.")

def nwd(x, y):
    while y != 0:
        temp = y
        y = x % y
        x = temp
    return x

def caesar_encrypt():
    with open("crypto.txt", "w") as w, open("plain.txt", "r") as file1, open("key.txt", "r") as file2:
        text = file1.read()
        key = int(file2.read().split()[0]) % 26
        for char in text:
            if 65 <= ord(char) <= 90:
                x = (ord(char) - 65 + key) % 26
                w.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = (ord(char) - 97 + key) % 26
                w.write(chr(x + 97))
            else:
                w.write(char)

def caesar_decrypt():
    with open("decrypt.txt", "w") as w, open("crypto.txt", "r") as file1, open("key.txt", "r") as file2:
        text = file1.read()
        key = int(file2.read().split()[0]) % 26
        for char in text:
            if 65 <= ord(char) <= 90:
                x = (ord(char) - 65 - key) % 26
                w.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = (ord(char) - 97 - key) % 26
                w.write(chr(x + 97))
            else:
                w.write(char)

def caesar_cryptanalysis():
    with open("extra.txt", "r") as extra, open("decrypt.txt", "w") as decrypt, open("key-found.txt", "w") as key, open("crypto.txt", "r") as encrypted:
        text = extra.read()
        crypto = encrypted.read()
        k = 0
        for i, (char1, char2) in enumerate(zip(text, crypto)):
            if i != 0:
                if  (65 <= ord(char1) <= 90 or 97 <= ord(char1) <= 122) and (ord(char1) - ord(char2)) % 26 != k:
                  raise Exception("Niemozliwe jest odnalezienie klucza.")
            else:
                if 65 <= ord(char1) <= 90 or 97 <= ord(char1) <= 122:
                    k = (ord(char1) - ord(char2)) % 26
        for char in crypto:
            if 65 <= ord(char) <= 90:
                x = (ord(char) - 65 - k) % 26
                decrypt.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = (ord(char) - 97 - k) % 26
                decrypt.write(chr(x + 97))
            else:
                decrypt.write(char)
        key.write(str(k))

def caesar_cryptanalysis_without():
    with open("crypto.txt", "r") as encrypted, open("decrypt.txt", "w") as decrypt:
        crypto = encrypted.read()
        for i in range(25):
            for char in crypto:
                if 65 <= ord(char) <= 90:
                    x = (ord(char) - 65 - i) % 26
                    decrypt.write(chr(x + 65))
                elif 97 <= ord(char) <= 122:
                    x = (ord(char) - 97 - i) % 26
                    decrypt.write(chr(x + 97))
                else:
                    decrypt.write(char)
            decrypt.write("\n")

def affine_encrypt():
    with open("crypto.txt", "w") as encrypt, open("plain.txt", "r") as plain, open("key.txt", "r") as key:
        text = plain.read()
        a_str, b_str = key.read().split()
        a = int(a_str)
        b = int(b_str) % 26
        if nwd(a, 26) != 1:
            raise Exception("Bledny klucz.")
        for char in text:
            if 65 <= ord(char) <= 90:
                x = ((ord(char) - 65) * a + b) % 26
                encrypt.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = ((ord(char) - 97) * a + b) % 26
                encrypt.write(chr(x + 97))
            else:
                encrypt.write(char)

def affine_decrypt():
    with open("crypto.txt", "r") as encrypt, open("decrypt.txt", "w") as decrypt, open("key.txt", "r") as key:
        text = encrypt.read()
        a_str, b_str = key.read().split()
        a = int(a_str)
        b = int(b_str) % 26
        if nwd(a, 26) != 1:
            raise Exception("Bledny klucz.")
        for char in text:
            if 65 <= ord(char) <= 90:
                x = ((ord(char) - 65 - b) * pow(a, -1, 26)) % 26
                decrypt.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = ((ord(char) - 97 - b) * pow(a, -1, 26)) % 26
                decrypt.write(chr(x + 97))
            else:
                decrypt.write(char)

def affine_cryptanalysis():
    with open("plain.txt", "r") as plain, open("key-found.txt", "w") as key, open("decrypt", "w") as decrypt, open("crypto.txt", "r") as encrypt:
        text = plain.read()
        encrypted = encrypt.read()
