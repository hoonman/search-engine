# Search Engine

## Tokenizer
Responsible for taking a sample file (HTML, PDF, docx, etc), parse it, and produce a frequency map of all the tokens. 
First, we unicode-normalize the token using NFKC form by default. If stripping accents is required by the user, we will use NFKD to decompose, strip the accents and recompose again.
We then use casefold to lowercase the token so that it covers for other language types.
Finally, we will filter out any punctuations that remain at the start or end of a token. 
