from math import log, exp
from collections import defaultdict, Counter
from zipfile import ZipFile
import re

kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"

kWORDS = re.compile("[a-z]{1,}")
kREP = set(["Bush", "GWBush", "Eisenhower", "Ford", "Nixon", "Reagan"])
kDEM = set(["Carter", "Clinton", "Truman", "Johnson", "Kennedy"])

class OutOfVocab(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

def sentences_from_zipfile(zip_file, filter_presidents):
    """
    Given a zip file, yield an iterator over the lines in each file in the
    zip file.
    """
    with ZipFile(zip_file) as z:
        for ii in z.namelist():
            try:
                pres = ii.replace(".txt", "").replace("state_union/", "").split("-")[1]
            except IndexError:
                continue

            if pres in filter_presidents:
                for jj in z.read(ii).decode(errors='replace').split("\n")[3:]:
                    yield jj.lower()

def tokenize(sentence):
    """
    Given a sentence, return a list of all the words in the sentence.
    """
    words =[]
    
    wordList = re.sub("[^a-zA-Z]", " ",  sentence).split()
    for word in wordList:
        words.append(word.lower())  
    
    #print(sentence)
    #print(words)
    #print("=====================================================================")
    return words

def bigrams(sentence):
    """
    Given a sentence, generate all bigrams in the sentence.
    """
    #sentence = "thank you, god bless you, and god bless america."
    # sentenceList = tokenize(sentence)
    # #print(sentenceList)
    # #print(len(sentence))
    # bigrams = []

    # for word in sentenceList:
    #     count = 0
    #     for letter in word:
    #         #print(word)
    #         if count != (len(word)-1):
    #             bigram = word[count]
    #             bigram = bigram + word[count+1]
    #             #print(word[count])
    #             #print(word[count+1])
    #             #print(bigram)
    #             bigrams.append(bigram)
    #         count += 1
    #     #print('=====')
    # #print(bigrams)
    # return bigrams
    for ii, ww in enumerate(sentence[:-1]):
        yield ww, sentence[ii + 1]

class BigramLanguageModel:

    def __init__(self):
        self._vocab = set([kSTART, kEND])
        
        # Add your code here!
        # Bigram counts
        #print(Counter(bigrams(self)))
        #self._bigram_count = bigrams(self)
        self._obs_counts = defaultdict(Counter)
        self._contextCount = {}
        self._vocab_final = False

    def train_seen(self, word):
        """
        Tells the language model that a word has been seen.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        # Add your code here!

        self._vocab.add(word)
        #print(self._vocab)


    def generate(self, context):
        """
        Given the previous word of a context, generate a next word from its
        conditional language model probability.  
        """

        # Add your code here.  Make sure to the account for the case
        # of a context you haven't seen before and Don't forget the
        # smoothing "+1" term while sampling.

        # Your code here

        #im a bit lost on this one
        return "the"
            
    def sample(self, sample_size):
        """
        Generate an English-like string from a language model of a specified
        length (plus start and end tags).
        """

        # You should not need to modify this function
        yield kSTART
        next = kSTART
        for ii in range(sample_size):
            next = self.generate(next)
            if next == kEND:
                break
            else:
                yield next
        yield kEND
            
    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added
        """
        
        # you should not need to modify this function
        
        self._vocab_final = True

    def tokenize_and_censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or testing.
        Prefix the sentence with <s>, generate the words in the
        sentence, and end the sentence with </s>.
        """

        # you should not need to modify this function
        
        yield kSTART
        for ii in tokenize(sentence):
            if ii not in self._vocab:
                raise OutOfVocab(ii)
            yield ii
        yield kEND

    def vocab(self):
        """
        Returns the language model's vocabulary
        """

        assert self._vocab_final, "Vocab not finalized"
        return list(sorted(self._vocab))
        
    def laplace(self, context, word):
        """
        Return the log probability (base e) of a word given its context
        """

        assert context in self._vocab, "%s not in vocab" % context
        assert word in self._vocab, "%s not in vocab" % word

        # Add your code here
        # print(context)
        # print("-----")
        # print(word)
        #val = (self._contextCount[(context, word)] + 1)/len(self._vocab)
        if self._contextCount.has_key((context, word)):
            val = (self._contextCount[(context, word)] + 1)/len(self._vocab)
        else:
            val = (0 + 1)/len(self._vocab)

        totalCounts = 0
        #print('lkasdflkhsdalfjjjjjk;jadskjfklsdajflk')
        for key, value in self._contextCount.items():
            if key[0] == context:
                totalCounts += value

        val = val + totalCounts
        return log(val)

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.
        for context, word in bigrams(list(self.tokenize_and_censor(sentence))):
            # print("****")
            # print(context)
            # print(word)
            # print("****")
            

            assert word in self._vocab, "%s not in vocab" % word

            if self._contextCount.has_key((context, word)):
                self._contextCount[(context, word)] += 1
            else:
                # if str(context) != '<s>':
                #     if str(context) != '</s>':
                #         if str(word) != '<s>':
                #             if str(word) != '</s>':
                self._contextCount[(context, word)] = 1

        #print(self._contextCount)
                

    def log_likelihood(self, sentence):
        """
        Compute the log likelihood of a sentence, divided by the number of
        tokens in the sentence.
        """

        #print(list(self.tokenize_and_censor(sentence))) #tokens
        #print(bigrams(list(self.tokenize_and_censor(sentence))))
        #print('test')
        logLike = 0
        for context, word in bigrams(list(self.tokenize_and_censor(sentence))):
            # print(context)
            # print("-----")
            # print(word)
            logLike = logLike + self.laplace(context,word)

        logLike = logLike/len(list(self.tokenize_and_censor(sentence)))
        
        return logLike


if __name__ == "__main__":

    prevWords = []

    for sent in sentences_from_zipfile("../data/state_union.zip", kREP):
            for ww in bigrams(sent):
                prevWords.append(ww)
    #print(set(prevWords))

    obamaWords = []
    for sent in sentences_from_zipfile("../data/2016-obama.txt.zip", "obama"):
            for ww in bigrams(sent):
                obamaWords.append(ww)
    #print(set(obamaWords))

    print(set(obamaWords)-set(prevWords))

    dem_lm = BigramLanguageModel()
    rep_lm = BigramLanguageModel()

    for target, pres, name in [(dem_lm, kDEM, "D"), (rep_lm, kREP, "R")]:
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            for ww in tokenize(sent):
                target.train_seen(ww)
                
        print("Done looking at %s words, finalizing vocabulary" % name)
        target.finalize()
        
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            target.add_train(sent)
    
        print("Trained language model for %s" % name)

    with open("../data/2016-obama.txt") as infile:
        print("REP\t\tDEM\t\tSentence\n" + "=" * 80)
        for ii in infile:
            if len(ii) < 15: # Ignore short sentences
                continue
            try:
                dem_score = dem_lm.log_likelihood(ii)
                rep_score = rep_lm.log_likelihood(ii)

                print("%f\t%f\t%s" % (dem_score, rep_score, ii.strip()))
            except OutOfVocab:
                None


            
            
