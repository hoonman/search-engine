from .cli import ArgParser
from .tokenizer import Tokenizer

def main():
    parser = ArgParser()
    args = parser.parse()
    print("received filepath: ", parser.filepaths)
    filepaths = parser.filepaths
    tokenizer = Tokenizer(filepaths[0])
    tokenizer.tokenize()
    tokenizer.compute_word_frequencies()
    tokenizer.print_frequencies()

if __name__ == "__main__":
    main()
