# Autor: Joanna Kaminska

import sys

args = sys.argv[1:]
mode = None

def xor(x, y):
    res = ""
    for i in range(len(x)):
        if (x[i] == "0" and y[i] == "0") or (x[i] == "1" and y[i] == "1"):
            res += "0"
        else:
            res += "1"
    return res

def text_preparation():
    with open("orig.txt", "r") as orig, open("plain.txt", "w") as plain, open("key.txt", "r") as key:
        text = orig.read()
        while len(text) > 0:
            if len(text) <= 64:
                plain.write(text + (64 - len(text)) * " ")
                text = ""
            else:
                plain.write(text[:64] + "\n")
                text = text[64:]

bin_value = format(int("A", 16), "08b")

def encrypt():
    with open("plain.txt", "r") as plain, open("key.txt" ,"r") as key, open("crypto.txt", "w") as crypto:
        lines = plain.read().split("\n")
        k = key.read()
        key_array = [format(b, '08b') for b in bytearray(k, 'utf-8')]
        for line in lines:
            array = [format(b, '08b') for b in bytearray(line, 'utf-8')]
            for i in range(len(array)):
                xor_var = xor(array[i], key_array[i])
                crypto.write(hex(int(xor_var, 2))[2:] + " ")
            crypto.write("\n")

def cryptanalysis():
    with open("crypto.txt", "r") as crypto, open("decrypt.txt", "w") as decrypt:
        raw = crypto.read().strip().split("\n")
        lines = [line.split() for line in raw]
        decrypted = []
        for i in range(len(lines)):
            new_list = []
            for j in range(len(lines[i])):
                lines[i][j] = format(int(lines[i][j], 16), "08b")
                new_list.append("_")
            decrypted.append(new_list)
        for column in range(len(lines[0])):
            found = False
            for row1 in range(len(lines)):
                for row2 in range(row1 + 1, len(lines)):
                    xor_var = xor(lines[row1][column], lines[row2][column])
                    if xor_var[:2] == "01":
                        key1 = xor(lines[row1][column], "00100000")
                        key2 = xor(lines[row2][column], "00100000")
                        test1 = []
                        test2 = []
                        for new_row in range(len(lines)):
                            test_var1 = xor(lines[new_row][column], key1)
                            test1.append(test_var1)
                            test_var2 = xor(lines[new_row][column], key2)
                            test2.append(test_var2)
                        score = []
                        for test in [test1, test2]:
                            ok = 0
                            for t in test:
                                val = int(t, 2)
                                if val == 32 or 64 <= val <= 126:
                                    ok += 1
                            score.append(ok)
                        test = test1 if score[0] >= score[1] else test2
                        correct_fr = 0
                        total = 0
                        for i in range(len(test)):
                            for k in range(i + 1, len(test)):
                                x_plain = xor(test[i], test[k])
                                x_cypher = xor(lines[i][column], lines[k][column])
                                total += 1
                                if x_plain == x_cypher:
                                    correct_fr += 1
                        if correct_fr >= total * 0.7:
                            for r in range(len(lines)):
                                val = int(test[r], 2)
                                if val == 32 or 64 <= val <= 126:
                                    decrypted[r][column] = chr(val)
                            found = True
                            break
                if found:
                    break
        for line in decrypted:
            for word in line:
                decrypt.write(word)
            decrypt.write("\n")

def main():
    if "-p" in args:
        text_preparation()
    elif "-e" in args:
        encrypt()
    elif "-k" in args:
        cryptanalysis()
    print("Odpowiedzi znajduja sie w plikach.")

main()