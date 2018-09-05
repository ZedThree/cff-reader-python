from . import reader

if __name__ == "__main__":
    cfffile = reader.reader(from_filename="./CITATION.cff")
    print(cfffile.cffyaml)
