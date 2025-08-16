import argparse

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="main.py",
            description="Runs the tokenizer with a filepath as argument."
        )
        self._setup_args()
        self._args = None

    def _setup_args(self):
        self.parser.add_argument(
            "--filepath",
            "-f",
            type=str,
            required=True,
            nargs="+",
            help="Path to the file to tokenize (ex. /path/to/file.txt)"
        )

    def parse(self, argv = None):
        self._args = self.parser.parse_args(argv)
        return self._args

    @property
    def filepaths(self):
        if self._args is None:
            raise RuntimeError("Arguments not parsed yet. Call .parse() first.")
        return self._args.filepath