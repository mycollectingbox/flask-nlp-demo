from collections import defaultdict, Counter



special_symbol_start = '<s>'
special_symbol_end = '</s>'

class UnigramModel:
    '''
    http://www.phontron.com/slides/nlp-programming-en-01-unigramlm.pdf
    '''
    
    def __init__(self):
        self.word_count_dict = Counter()
        self.vocab_size = 0
        self.model_finish = False

    def train(self, training_list, total_vocabulary_size):
        # append </s> symbol
        for i in range(len(training_list)):
            training_list[i].append(special_symbol_end)
        # calculate ML estimate
        self.word_count_dict = Counter()
        for i, example in enumerate(training_list):
            for word in example:
                self.word_count_dict[word] += 1
        self.total_word_count = sum(self.word_count_dict.values())
        self.vocab_size = total_vocabulary_size
        self.model_finish = True
        
    def get_smooth_prob(self, word):
        '''
        (1 - lambda) * P_ML + lambda / vocab_size,
        where lambda is the unknown word probability
        '''
        return 0.95 * self.get_MaimumLikelihoodProb(word) + 0.05 / self.vocab_size

    def get_MaimumLikelihoodProb(self, word):
        if not self.model_finish:
            raise NotImplementedError("don't use this function before training.")

        return self.word_count_dict[word]/self.total_word_count


class BigramModel:
    '''
    http://www.phontron.com/slides/nlp-programming-en-02-bigramlm.pdf
    '''

    def __init__(self, previous_word_count =None, two_word_count= None):
        if previous_word_count == None:
            self.previous_word_count = Counter()
            self.two_word_count = defaultdict(Counter)
            self.model_finish = False
        else:
            self.previous_word_count = previous_word_count
            self.two_word_count = two_word_count
            self.model_finish = True

    def train(self, training_list, totla_voc_size):
        self.unigram_model = UnigramModel()
        self.unigram_model.train(training_list, totla_voc_size)

        # append </s> symbol
        for i in range(len(training_list)):
            training_list[i].append(special_symbol_end)

        # calculate ML estimate
        self.two_word_count = defaultdict(Counter)
        self.previous_word_count = Counter()
        self.unique_dict = defaultdict(set)
        # each example is ['ㄅㄞˊ', 'ㄏㄜˊ',　'ㄍㄨㄥ', '</s>']
        for i, example in enumerate(training_list):
            for j in range(len(example) - 1):
                self.previous_word_count[example[j]] += 1
                self.two_word_count[example[j]][example[j+1]] += 1
                self.unique_dict[example[j]].add(example[j+1])
        
        self.model_finish = True

    def get_MaimumLikelihoodProb(self, prevWord, nowWord):
        if not self.model_finish:
            raise NotImplementedError("don't use this function before training.")

        if self.previous_word_count[prevWord] == 0:
            return 0
        else:
            return self.two_word_count[prevWord][nowWord]/self.previous_word_count[prevWord]


    def lambda_value(self, previous_word):
        denominator = len(self.unique_dict[previous_word]) + self.previous_word_count[previous_word]
        if denominator == 0:
            return 0
        else:
            return self.previous_word_count[previous_word]/denominator

    def get_smooth_prob(self, prevWord, nowWord):

        return self.lambda_value(prevWord) * self.get_MaimumLikelihoodProb(prevWord, nowWord) + (1 - self.lambda_value(prevWord)) * self.unigram_model.get_smooth_prob(nowWord)

    def get_joint_prob(self, sequence):
        '''
        計算 sequence的bigram機率\n
        sequence: list of items
        '''
        total_prob = self.unigram_model.get_smooth_prob(sequence[0])
        for i in range(1, len(sequence)):
            total_prob *= self.get_smooth_prob(sequence[i-1], sequence[i])

        return total_prob

import pickle
def get_load_model(pklFilePath, module_path = './model'):

    import sys
    sys.path.append(module_path)

    with open(pklFilePath, 'rb') as sr:
        foreign_lm = pickle.load(sr)
    return foreign_lm