from cli import ArgParser
from tokenizer import Tokenizer

def main():
    parser = ArgParser()
    args = parser.parse()
    print("received filepath: ", parser.filepath)
    filepath = parser.filepath
    tokenizer = Tokenizer(filepath)
    tokenizer.tokenize()

if __name__ == "__main__":
    main()
