import hashlib

def generate_hashes():
    try:
        with open("personal.txt", "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku personal.txt")
        return

    algorithms = [
        ('md5', hashlib.md5),
        ('sha1', hashlib.sha1),
        ('sha224', hashlib.sha224),
        ('sha256', hashlib.sha256),
        ('sha384', hashlib.sha384),
        ('sha512', hashlib.sha512),
        ('blake2b', hashlib.blake2b)
    ]

    with open("hash.txt", "w") as out:
        for name, func in algorithms:
            h = func(data).hexdigest()
            out.write(f"{h}  {"personal.txt"}\n") # hash[spacja][spacja]nazwa_pliku

    print("Plik hash.txt wygenerowany")

if __name__ == "__main__":
    generate_hashes()