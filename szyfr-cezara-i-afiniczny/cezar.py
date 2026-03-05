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
            print()
        else:
            print()
    else:
        if option == "e":
            print()
        elif option == "d":
            print()
        elif option == "j":
            print()
        else:
            print()

print("Odpowiedzi znajduja sie w plikach.")

def caesar_encrypt():
    with open("crypto.txt", "a") as w, open("plain.txt", "r") as file1, open("key.txt", "r") as file2:
        text = file1.read()
        key = int(file2.read().split()[0]) % 26
        for char in text:
            if 65 <= ord(char) <= 90:
                x = ord(char) - 65 + key % 26
                w.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = ord(char) - 97 + key % 26
                w.write(chr(x + 97))
            else:
                w.write(char)

def caesar_decrypt():
    with open("decrypt.txt", "a") as w, open("crypto.txt", "r") as file1, open("key.txt", "r") as file2:
        text = file1.read()
        key = int(file2.read().split()[0]) % 26
        for char in text:
            if 65 <= ord(char) <= 90:
                x = ord(char) - 65 - key % 26
                w.write(chr(x + 65))
            elif 97 <= ord(char) <= 122:
                x = ord(char) - 97 - key % 26
                w.write(chr(x + 97))
            else:
                w.write(char)