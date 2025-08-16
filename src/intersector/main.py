from .intersector import Intersector
from ..tokenizer.tokenizer import Tokenizer
from ..tokenizer.cli import ArgParser

def main():
    parser = ArgParser()

    parser.parse()
    print("received filepaths: ")
    # for the intersector, we only need two filepaths so we will assume that we received two and use the first two. if we don't have two, we will print exception

    if len(parser.filepaths) != 2:
        print("You must input two filepaths exactly to compute intersection !")
        return

    filepath1 = parser.filepaths[0]
    filepath2 = parser.filepaths[1]
    tokenizer1 = Tokenizer(filepath1)
    tokenizer2 = Tokenizer(filepath2)

    tokenizer1.tokenize()
    tokenizer1.compute_word_frequencies()
    tokenizer2.tokenize()
    tokenizer2.compute_word_frequencies()

    frequency_map1 = tokenizer1.get_frequency_map()
    frequency_map2 = tokenizer2.get_frequency_map()

    intersector = Intersector()
    intersection_length = intersector.compute_intersection(frequency_map1, frequency_map2)
    print(f"The intersection length was: {intersection_length}")



if __name__ == "__main__":
    main()