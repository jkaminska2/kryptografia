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
    with open("plain.txt", "w") as w, open("crypto.txt", "r") as file1, open("key.txt", "r") as file2:
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

def caesar_cryptanalysis_brute_force():
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
    with open("crypto.txt", "r") as encrypt, open("plain.txt", "w") as decrypt, open("key.txt", "r") as key:
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
    with open("plain.txt", "r") as plain, open("key-found.txt", "w") as key, open("decrypt.txt", "w") as decrypt, open("crypto.txt", "r") as encrypt:
        text = plain.read()
        encrypted = encrypt.read()
        a = None
        b = None
        if len(text) < 2:
            raise Exception("Niewystarczajacy tekst jawny.")
        for i in range(len(text)):
            p = text[i]
            c = encrypted[i]
            if p.isalpha() and c.isalpha():
                if 65 <= ord(p) <= 90 and 65 <= ord(c) <= 90:
                    P = ord(p) - 65
                    C = ord(c) - 65
                else:
                    P = ord(p) - 97
                    C = ord(c) - 97
                break
        else:
            raise Exception("Brak liter w plain.")
        for j in range(i + 1, len(text)):
            p2 = text[j]
            c2 = encrypted[j]
            if p2.isalpha() and c2.isalpha():
                if 65 <= ord(p2) <= 90 and 65 <= ord(c2) <= 90:
                    P2 = ord(p2) - 65
                    C2 = ord(c2) - 65
                else:
                    P2 = ord(p2) - 97
                    C2 = ord(c2) - 97
                if P2 != P:
                    a = ((C - C2) * pow((P - P2), -1, 26)) % 26
                    b = (C - a * P) % 26
                    break
        if a is None:
            raise Exception("Brak dwoch roznych liter w plain.")
        for k in range(len(text)):
            p = text[k]
            c = encrypted[k]
            if p.isalpha() and c.isalpha():
                if 65 <= ord(p) <= 90:
                    Pk = ord(p) - 65
                else:
                    Pk = ord(p) - 97
                if 65 <= ord(c) <= 90:
                    Ck = ord(c) - 65
                else:
                    Ck = ord(c) - 97
                if (Ck - a * Pk) % 26 != b:
                    raise Exception("Niemozliwe jest odnalezienie klucza.")
        key.write(str(a) + " " + str(b))
        for char in encrypted:
            if 65 <= ord(char) <= 90:
                x = ((ord(char) - 65 - b) * pow(a, -1, 26)) % 26
                decrypt.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = ((ord(char) - 97 - b) * pow(a, -1, 26)) % 26
                decrypt.write(chr(x + 97))
            else:
                decrypt.write(char)

def affine_cryptanalysis_brute_force():
    with open("crypto.txt", "r") as encrypt, open("decrypt.txt", "w") as decrypt:
        text = encrypt.read()
        for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            for b in range(26):
                for char in text:
                    if 65 <= ord(char) <= 90:
                        x = ((ord(char) - 65 - b) * pow(a, -1, 26)) % 26
                        decrypt.write(chr(x + 65))
                    elif 97 <= ord(char) <= 122:
                        x = ((ord(char) - 97 - b) * pow(a, -1, 26)) % 26
                        decrypt.write(chr(x + 97))
                    else:
                        decrypt.write(char)
                decrypt.write("\n")

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
            caesar_cryptanalysis_brute_force()
    else:
        if option == "e":
            affine_encrypt()
        elif option == "d":
            affine_decrypt()
        elif option == "j":
            affine_cryptanalysis()
        else:
            affine_cryptanalysis_brute_force()

    print("Odpowiedzi znajduja sie w plikach.")

main()