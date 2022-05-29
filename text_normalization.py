import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from urllib.request import urlopen

# Disable SSL checking
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download datasets
nltk.download('punkt')
nltk.download('wordnet')


def stemmers_and_lemmitizers():
    print('Stemmer use the simple following code to implement porter stemmer.')

    ps = PorterStemmer()

    example_words = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]

    for w in example_words:
        print(ps.stem(w))

    print(
        ' You can use this algorithm combining with a tokenization code in order to stem the words in a sentence, as below:')

    new_text = """It is very important to be pythonly while you are pythoning
            with python. All pythoners have pythoned poorly at least once."""

    words = word_tokenize(new_text)

    for w in words:
        print(ps.stem(w))

    print(
        'NLTK includes several off-the-shelf stemmers, and if you ever need a stemmer you should use one of these in preference to crafting your own using regular expressions, since these handle a wide range of irregular cases. The Porter and Lancaster stemmers follow their own rules for stripping affixes. Observe that the Porter stemmer correctly handles the word lying (mapping it to lie), while the Lancaster stemmer does not.')
    raw = """DENNIS: Listen, strange women lying in ponds distributing swords
        is no basis for a system of government.  Supreme executive power derives from
        a mandate from the masses, not from some farcical aquatic ceremony."""

    tokens = word_tokenize(raw)

    porter = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()

    print([porter.stem(t) for t in tokens])
    print("\n")
    print([lancaster.stem(t) for t in tokens])

    print(
        'The WordNet lemmatizer only removes affixes if the resulting word is in its dictionary. This additional checking process makes the lemmatizer slower than the above stemmers. Notice that it doesn\'t handle lying, but it converts women to woman.')

    raw = """DENNIS: Listen, strange women lying in ponds distributing swords
        is no basis for a system of government.  Supreme executive power derives from
        a mandate from the masses, not from some farcical aquatic ceremony."""

    tokens = word_tokenize(raw)

    wnl = nltk.WordNetLemmatizer()
    print([wnl.lemmatize(t) for t in tokens])


# The WordNet lemmatizer is a good choice if you want to compile the vocabulary of some texts and want a list of valid lemmas (or lexicon headwords).
def generate_ngrams(text, WordsToCombine):
    words = text.split()
    output = []
    for i in range(len(words) - WordsToCombine + 1):
        output.append(words[i:i + WordsToCombine])
    return output


def ngram_test():
    # Calling the function
    generate_ngrams(text='this is a very good book to study', WordsToCombine=3)

    # Or by NLTK:

    # NLTK function to generate ngrams
    sample_text = 'this is a very good book to study'
    ngram_list = ngrams(sequence=nltk.word_tokenize(sample_text), n=3)
    for grams in ngram_list:
        print(grams)


'''

Exercises
1.      For the following cases, use the Porter Stemmer to normalize some tokenized text, calling the stemmer on each word. Do the same thing with the Lancaster Stemmer and see if you observe any differences.

a)     Capture the text that a user inputs.

b)     Read the text from a local file.

c)     Read the book “King Edward III by Shakespeare” from free online books in Project Gutenberg

d)     Read the html format of “CHAPTER VII. THE HOUSE IN SOHO” of the book “THE SECRET ADVERSARY by Agatha Christie” from free online books in Project Gutenberg

'''


def stemming(raw):
    print('stemming()')
    tokens = word_tokenize(raw)

    porter = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()

    print([porter.stem(t) for t in tokens])
    print("\n")
    print([lancaster.stem(t) for t in tokens])


def question_one():
    # A. User input
    stemming("""DENNIS: Listen, strange women lying in ponds distributing swords
        is no basis for a system of government.  Supreme executive power derives from
        a mandate from the masses, not from some farcical aquatic ceremony.""")

    # B. From file
    # test_file_for_stemming.txt
    with open('test_file_for_stemming.txt', 'r') as f:
        text = f.read()
        stemming(text)

    # C. From online txt file
    print('From book online in txt file format')
    r = urlopen("https://www.gutenberg.org/cache/epub/1770/pg1770.txt")
    print('r: ', r.read())
    for line in r.read():
        print('line: ', line)
        stemming(line)

    # D. From a book chapter in a website in HTML format
    r2 = urlopen("https://www.owleyes.org/text/the-secret-adversary/read/chapter-vii-the-house-in-soho")
    for line in r2:
        stemming(line)


if __name__ == '__main__':
    stemmers_and_lemmitizers()
    ngram_test()
    question_one()
