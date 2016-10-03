from collections import Counter
from zipfile import ZipFile
import re
import zipfile

kWORDS = re.compile("[a-z]{4,}")

def text_from_zipfile(zip_file):
    """
    Given a zip file, yield an iterator over the text in each file in the
    zip file.
    """
    # Modify this function
    files = {}
    #zipVar = zipfile.ZipFile(zip_file)
    with zipfile.ZipFile(zip_file) as zippedFile:
        for name in zippedFile.namelist():
            #print(name)
            if name != "state_union/README":
                if name != "state_union/":
                    #files[name] = zippedFile.read(name)
                    bytesObj = zippedFile.read(name)
                    #stringFormat = str(bytesObj)[2:-1]
                    stringFormat = bytesObj.decode('UTF-8')
                    # print("======")
                    # print(stringFormat)
                    # print("======")
                    #bytesObj.encode('utf-8').strip()
                    #string = str(bytesObj,'utf-8')
                    #files[name] = str(bytesObj)
                    yield stringFormat
    
    #print(type(files['state_union/1945-Truman.txt']))
    #return ["nope"]

def words(text):
    """
    Return all words in a string, where a word is four or more contiguous
    characters in the range a-z or A-Z.  The resulting words should be
    lower case.
    """
    # s = """Return all words in a string, where a word is four or more contiguous
    # characters in the range a-z or A-Z.  The resulting words should be
    # lower case."""
    #print(text)
    # removedText = re.compile("(\w[\w']*\w|\w)") 
    # text = removedText.findall(text)
    #text = "Yes, we can certainly find real words, Frank!"
    passedWords =[]
    #tempList = text.split()
    wordList = re.sub("[^a-zA-Z]", " ",  text).split()
    for word in wordList:
        if len(word) > 3:
            passedWords.append(word)
    # for word in tempList:
    #     for char in word:
    #         if char == '''/''':

    #     print(word)
    #     passedWord = ""
    #     for char in word:
    #         if char in '''!,.?":';0123456789''':
    #             #print(char)
    #             char = ""
    #         if char == '(':
    #             char = ""
    #         if char == '-':
    #             char = ""
    #             break
    #         print(char)
    #         passedWord += char
    #     if len(passedWord) > 3:
    #         # for char in word:
    #         #     if char in '''!,.?":';0123456789''':
    #         #         char = ""
    #         #print(passedWord)
    #         passedWords.append(passedWord)

    text = passedWords
    text = [x.lower() for x in text]
    #print(text)
    #shortword = re.compile(r'\W*\b\w{1,3}\b')    
    #shortword.sub('', text)
    #text = [x for x in text if len(x) > 4] #remove words < 4 letters

    #print(text)
    
    # Modify this function
    return text

def accumulate_counts(words, total=Counter()):
    """
    Take an iterator over words, add the sum to the total, and return the
    total.

    @words An iterable object that contains the words in a document
    @total The total counter we should add the counts to
    """
    assert isinstance(total, Counter)
    # print(Counter(["a", "b", "c", "c"]))
    count = 0
    for word in words:
        count += 1
        total[word] +=1
    #print(count)
    #total += count
    #total = Counter(words)
    # Modify this function    
    return total

if __name__ == "__main__":
    # You should not need to modify this part of the code
    total = Counter()
    for tt in text_from_zipfile("../data/state_union.zip"):
        prevPres = set(words(tt))
        #print(prevPres)
        total = accumulate_counts(words(tt), total)
    for tt in text_from_zipfile("../data/2016-obama.zip"):
        obamaPres = set(words(tt))

    print(obamaPres-prevPres)
        
        #total = accumulate_counts(words(tt), total)

    for ii, cc in total.most_common(100):
        print("%s\t%i" % (ii, cc))
