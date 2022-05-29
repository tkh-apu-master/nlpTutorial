import re

# Minimal Edit Distance (MED) is a measure of the number of operations required to transform one string into another.
# Initialization of MED
first = 'execution'
second = 'intention'
cost = 2


def edit_distance():
    n = len(first)  # column
    m = len(second)  # row

    # Python list comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
    # Initialize Matrix in Python: https://www.geeksforgeeks.org/initialize-matrix-in-python/
    matrix = [[x + y for x in range(m + 1)] for y in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # column i row j

            if first[i - 1] == second[j - 1]:  # Similar
                cost2 = 0
            else:
                cost2 = cost

            left_side = matrix[i - 1][j]
            bottom_side = matrix[i][j - 1]
            diagonal_side = matrix[i - 1][j - 1]

            matrix[i][j] = min(left_side + 1, bottom_side + 1, diagonal_side + cost2)

    response = matrix[n - 1][m - 1]

    return response, matrix


# https://docs.google.com/document/d/1GbR6HftTPwJ5YhdjCkQWWjyvpq6cCoz7wf0f7dTsP30/edit
def backtrace(matrix):
    # print('matrix: ', matrix)
    backtrack = []

    # pointers. But array index starts at 0.
    x = len(matrix) - 1
    y = len(matrix[0]) - 1

    for i in reversed(range(len(matrix) + 1)):
        # print('index: ', i)
        current = matrix[x][y]
        left_side = matrix[x - 1][y]
        bottom_side = matrix[x][y - 1]
        diagonal_side = matrix[x - 1][y - 1]
        # print('current: ', current)
        # print('left_side: ', left_side)
        # print('bottom_side: ', bottom_side)
        # print('diagonal_side: ', diagonal_side)

        if current == 1 and bottom_side == 0:
            backtrack.append('d')
            y = y - 1

        if left_side == bottom_side:
            if current == diagonal_side:
                backtrack.append(' ')
            elif current == diagonal_side + cost:
                backtrack.append('s')
            # Move Diagonally
            x = x - 1
            y = y - 1
        else:
            if current == diagonal_side:
                lowest_value = min(diagonal_side + cost, left_side + 1)
                if lowest_value == left_side + 1 and first[x - 1] != second[y - 1]:
                    backtrack.append('i')
                    x = x - 1
                else:
                    backtrack.append(' ')
                    x = x - 1
                    y = y - 1

        # print('backtrack: ', backtrack)

    return backtrack


# End of MED implementation**************************************************************************************

# NLP Homework
# Regex

# https://colab.research.google.com/drive/1Pf1n48GvvQ-DA9hiBCxL9Q-UFp3NR55E#scrollTo=XGnRKzIfs2du

# In the W3C Date Time Format, dates are represented like this: 2009-12-31. Replace the ? in the following Python 
# code with a regular expression, in order to convert the string '2009-12-31' to a list of integers [2009, 12, 
# 31]: [int(n) for n in re.findall(?, '2009-12-31')] 
def regex_question_one(date_string):
    # Reference: https://stackoverflow.com/a/2841557
    # \d is a digit
    # + means one or more times
    # d+ means 1 or more digits
    return [int(n) for n in re.findall('\d+', date_string)]


# Are you able to write a regular expression to tokenize text in such a way that the word don't is tokenized into do 
# and n't? Explain why this regular expression won't work: «n't|\w+». 
def regex_question_two():
    # reads in a text
    # f = open('corpus.txt')
    # raw = f.read()
    matches = re.findall(r'\b(do)(n\'t)', 'don\'t')

    # The correct regular expression: \b(do)(n\'t)
    # Expected output: ['do', 'n't']

    # \w is any word character
    # + means one or more times
    # \w+ means 1 or more word characters

    # Question: Why n't|\w+ is not working?
    # Answer: Because single quote is not escaped, we need to escape n\'t|\w+.

    return matches


# Try to write code to convert text into hAck3r, using regular expressions and substitution,
# where e → 3, i → 1, o → 0, l → |, s → 5, . → 5w33t!, ate → 8.
# Normalize the text to lowercase before converting it. Add more substitutions of your own.
# Now try to map s to two different values: $ for word-initial s, and 5 for word-internal s.
def regex_question_third(text):
    """converts a text to hacker"""
    new_text = []

    # initial pass substitutes 8 for ate.
    pattern = re.compile(r'ate')
    text = pattern.sub('8', text)

    # regex that searches through the text to find instances of the letters to be converted.
    pattern = re.compile(r'[eiols]|\.')

    # converts all the letters
    for w in text:
        if re.search(pattern, w):
            if w == 'e':
                w = '3'
            elif w == 'i':
                w = '1'
            elif w == 'o':
                w = '0'
            elif w == 's':
                w = '5'
            elif w == 'l':
                w = '|'
            elif w == '.':
                w = '5w33t!'
        new_text.extend(w)
    new_text = ''.join(new_text)

    # regex searching for word initial s.
    pattern = re.compile(r'\b5')
    new_text = pattern.sub('$', new_text)

    return new_text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    array = regex_question_one('2009-12-31') # --> ['2009', '12', '31'] -> [2009, 12, 31]
    print(array)

    matches = regex_question_two()
    print(matches)

    text = regex_question_third('hacker')
    print(text)
    text2 = regex_question_third('hate')
    print(text2)
    text3 = regex_question_third('sweet')
    print(text3)
    text4 = regex_question_third('...')
    print(text4)

    med, matrix2 = edit_distance()
    print(med)
    result = backtrace(matrix2)
    print(result)
