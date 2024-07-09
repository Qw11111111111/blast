from Bio.Seq import Seq
import random as rand
import numpy as np

class ALign_seq:

    def __init__(self, query: Seq, db: Seq, word_len: int = 10, hit_threshhold: int = 1, n_hits: int = 40) -> None:
        self.query = query[0].seq
        self.db = db
        self.hits = {i:{} for i in range(len(self.db))}
        self.n_hits = n_hits
        self.threshhold = hit_threshhold
        self.word_len = word_len
        self.current_word = Seq("")
        self.current_word_start = 0
        self.total_seeds = 0
        self.current_min = (0, 0, len(self.query) + 1)

    def set_seeds(self):
        self.get_word()
        for i, record in enumerate(self.db):
            record = record.seq
            for j in range(self.current_word_start, len(record), 1):
                if (score := self.get_matches(record[j:j + len(self.current_word)])) > self.threshhold:
                    self.seed_match(score, j, i)

    def search(self):
        self.set_seeds()
        self.current_word = self.query
        print(self.hits)
        for i, record in enumerate(self.db):
            record = record.seq         #record[i][j - self.current_word_start: j - self.current_word_start + len(self.query)]
            self.hits[i] = {j: self.get_matches(record[j - self.current_word_start: j - self.current_word_start + len(self.query)]) for j in self.hits[i].keys()}#dict(map(lambda item: (item[0], self.get_matches(record[item[0]]))))
  
    def seed_match(self, score: int, index: int, record: int):
        if self.total_seeds == self.n_hits:
            if score <= self.current_min[2]:
                return
            self.hits[self.current_min[0]].pop(self.current_min[1])
            #min_arg = np.argmin(list(self.hits[record].values()))
            #iterator = enumerate(self.hits[record].items())
            #self.hits[record] = dict(map(lambda item: item[1] if item[0] != min_arg else (index, score)), iterator)
            self.hits[record][index] = score
        else:
            self.hits[record][index] = score
            self.total_seeds += 1
            if score < self.current_min[1]:
                self.current_min = (record, index, score)


    def get_matches(self, seq): 
        n = 0
        for i, letter in enumerate(seq):
            if letter == self.current_word[i]:
                n += 1
        return n

    def summary(self):
        print(self.hits, "unsorted")
        empty_list = []
        seq = [list(map(lambda item: {(i, item[1][0]): item[1][1]}, enumerate(dict(sorted(subdict[1].items(), key = lambda x: x[1])).items()))) for i, subdict in enumerate(self.hits.items())]

        for sublist in seq:
                empty_list += sublist

        empty_list = sorted(empty_list, key = lambda item: list(item.values())[0])
        print(empty_list, "sorted")
        return empty_list

    def get_word(self):
        seed = rand.randint(0, len(self.query) - self.word_len - 1)
        self.current_word = self.query[seed:seed + self.word_len]
        self.current_word_start = seed
        print(self.current_word)
        print(self.current_word_start)
        print(self.query[seed:])
    
    def extend_word(self):
        if self.current_word > 0:
            self.current_word_start -= 1
            self.current_word = self.query[self.current_word_start] + self.current_word
        elif len(self.current_word) < len(self.query):
            self.current_word += self.query(len(self.current_word))
        else:
            #unreachable
            pass