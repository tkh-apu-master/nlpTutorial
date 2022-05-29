import nltk
import random

from nltk.corpus import names
from nltk.classify import apply_features
from nltk.corpus import movie_reviews

# Disable SSL checking
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ****

# Download datasets
nltk.download('names')
nltk.download('movie_reviews')

#
# Imported from: https://colab.research.google.com/drive/1wkRQtom3BqT3aOM1QaiAhHtzGy6l6T5t?usp=sharing#scrollTo=zAsg2QkkUzyE

labeled_names = []
featuresets = []
word_features = []


def gender_features(word):
    return {'last_letter': word[-1]}


def text_classification_one():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in
                                                                             names.words('female.txt')])

    random.shuffle(labeled_names)

    featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
    train_set, test_set = featuresets[500:], featuresets[:500]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("Neo is a", classifier.classify(gender_features('Neo')))
    print("Trinity is a", classifier.classify(gender_features('Trinity')))
    print("\nThe accuracy is equal to: ", nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)

    print(
        'This listing shows that the names in the training set that end in "a" are female 33 times more often than they are male, but names that end in "k" are male 32 times more often than they are female. These ratios are known as likelihood ratios, and can be useful for comparing different feature-outcome relationships. When working with large corpora, constructing a single list that contains the features of every instance can use up a large amount of memory. In these cases, use the function nltk.classify.apply_features, which returns an object that acts like a list but does not store all the feature sets in memory:')
    train_set = apply_features(gender_features, labeled_names[500:])
    test_set = apply_features(gender_features, labeled_names[:500])
    return classifier


def sentiment_analysis():
    print(
        'There are several examples of corpora where documents have been labelled with categories. Using these corpora, we can build classifiers that will automatically tag new documents with appropriate category labels. First, we construct a list of documents, labelled with the appropriate categories. For this example, we\'ve chosen the Movie Reviews Corpus, which categorizes each review as positive or negative.')
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]

    len(documents)

    for row in range(0, len(documents) - 1):
        print(documents[row][1])

    random.shuffle(documents)
    print(documents[1])

    print(
        'Next, we define a feature extractor for documents, so the classifier will know which aspects of the data it should pay attention to. For document topic identification, we can define a feature for each word, indicating whether the document contains that word. Remove print(documents[1]) and add the following lines to the code:')
    all_words = []
    for w in movie_reviews.words():
        wl = w.lower()
        all_words.append(wl)

    all_words = nltk.FreqDist(all_words)
    print(all_words.most_common(15))

    print('Remove print(all_words.most_common(15)) and add the following lines to the code:')
    print(all_words["good"])
    print(all_words["excellent"])

    print(
        'To limit the number of features that the classifier needs to process, we begin by constructing a list of the 3000 most frequent words in the overall corpus. We can then define a feature extractor that simply checks whether each of these words is present in a given document.')
    word_features = list(all_words)[:3000]

    print('You can test the feature extractor, by:')
    print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

    featureset = [(find_features(rev), category) for (rev, category) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    classifier.show_most_informative_features(5)

    print(
        'To check how reliable the resulting classifier is, we compute its accuracy on the test set. And once again, we can use show_most_informative_features() to find out which features the classifier found to be most informative.')
    print(nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)

    return classifier


def find_features(document):
    # We can then define a feature extractor that simply checks whether each of these words is present in a given document.
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


def question_one():
    return


def question_two():
    classifier = sentiment_analysis()
    classifier.show_most_informative_features(30)


# *********************PART TWO******************************************************************************

def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features


def sentiment_analysis2():
    featuresets = [(gender_features2(n), gender) for (n, gender) in labeled_names]
    train_set, test_set = featuresets[500:], featuresets[:500]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))

    train_names = labeled_names[1500:]  # 1500 and above for training
    devtest_names = labeled_names[500:1500]  # 500 to 1500 # for checking accuracy
    test_names = labeled_names[:500]  # 0 to 500 for testing

    train_set = [(gender_features2(n), gender) for (n, gender) in train_names]
    devtest_set = [(gender_features2(n), gender) for (n, gender) in devtest_names]
    test_set = [(gender_features2(n), gender) for (n, gender) in test_names]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, devtest_set))

    errors = []
    for (name, tag) in devtest_names:
        guess = classifier.classify(gender_features2(name))
        if guess != tag:
            errors.append((tag, guess, name))

    for (tag, guess, name) in sorted(errors):
        print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))


def gender_features3(word):
    return {'suffix1': word[-1:],
            'suffix2': word[-2:]}


def text_classification_two():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                     [(name, 'female') for name in names.words('female.txt')])

    random.shuffle(labeled_names)

    train_names = labeled_names[1500:]
    devtest_names = labeled_names[500:1500]
    test_names = labeled_names[:500]

    train_set = [(gender_features3(n), gender) for (n, gender) in train_names]
    devtest_set = [(gender_features3(n), gender) for (n, gender) in devtest_names]
    test_set = [(gender_features3(n), gender) for (n, gender) in test_names]

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("\nThe accuracy is: ", nltk.classify.accuracy(classifier, devtest_set) * 100, "%")

    errors = []
    prediction_list = []
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for (name, tag) in devtest_names:
        guess = classifier.classify(gender_features3(name))
        prediction_list.append((tag, guess, name))
        if guess == 'male':
            if tag == 'male':
                TP += 1
            else:
                FP += 1
        else:
            if tag == 'female':
                TN += 1
            else:
                FN += 1

        if guess != tag:
            errors.append((tag, guess, name))

    print('total number of test items: ', len(prediction_list))
    print('total number of errors: ', len(errors))

    print('TP: ', TP)
    print('FP: ', FP)
    print('TN: ', TN)
    print('FN: ', FN)

    def column(matrix, i):
        return [row[i] for row in matrix]

    cm = nltk.ConfusionMatrix(column(prediction_list, 0), column(prediction_list, 1))
    print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))


'''
1. Use any features you can think to build the best name gender classifier you can.
Begin by splitting the Names Corpus into three subsets: 500 words for the test set, 500 words for the dev-test set,
and the remaining 6900 words for the training set.
Then, starting with the example name gender classifier, make incremental improvements.
Use the dev-test set to check your progress.
Once you are satisfied with your classifier, check its final performance on the test set.
How does the performance on the test set compare to the performance on the dev-test set? Is this what you'd expect?

2. The synonyms strong and powerful pattern differently (try combining them with chip and sales).
What features are relevant in this distinction? Build a classifier that predicts when each word should be used.

'''


def question_one_part_two():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                     [(name, 'female') for name in names.words('female.txt')])

    random.shuffle(labeled_names)

    train_names = labeled_names[1000:7900]
    devtest_names = labeled_names[500:1000]
    test_names = labeled_names[:500]

    train_set = [(gender_features3(n), gender) for (n, gender) in train_names]
    devtest_set = [(gender_features3(n), gender) for (n, gender) in devtest_names]
    test_set = [(gender_features3(n), gender) for (n, gender) in test_names]

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("\nThe accuracy is: ", nltk.classify.accuracy(classifier, devtest_set) * 100, "%")

    errors = []
    prediction_list = []
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for (name, tag) in devtest_names:
        guess = classifier.classify(gender_features3(name))
        prediction_list.append((tag, guess, name))
        if guess == 'male':
            if tag == 'male':
                TP += 1
            else:
                FP += 1
        else:
            if tag == 'female':
                TN += 1
            else:
                FN += 1

        if guess != tag:
            errors.append((tag, guess, name))

    print('total number of test items: ', len(prediction_list))
    print('total number of errors: ', len(errors))

    print('TP: ', TP)
    print('FP: ', FP)
    print('TN: ', TN)
    print('FN: ', FN)

    def column(matrix, i):
        return [row[i] for row in matrix]

    cm = nltk.ConfusionMatrix(column(prediction_list, 0), column(prediction_list, 1))
    print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))


def question_two_part_two():
    return


if __name__ == '__main__':
    example = gender_features('Shrek')
    print('Shrek: ', example)
    text_classification_one()
    sentiment_analysis()
    question_one()
    question_two()

    gender_features2('John')
    text_classification_two()
    question_one_part_two()
    question_two_part_two()
