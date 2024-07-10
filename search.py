from Bio.Seq import Seq
import random as rand
from tqdm import tqdm


class Summary:
    
    def __init__(self, summary_dict, word_start: int, query, db) -> None:
        self._summary_dict = summary_dict
        self.query = query
        self._word_start = word_start
        self.database = db
        self._generate_summary()

    def _generate_summary(self):
        best_index = list(self._summary_dict[-1].keys())[0]  
        self.best_sequence = self.database[best_index[0]].seq[best_index[1] - self._word_start:best_index[1] + len(self.query) - self._word_start]
        self.similarity = list(self._summary_dict[-1].values())[0] / len(self.query) * 100

class AlignSeq:

    def __init__(self, query: Seq, db: Seq, word_len: int = 5, hit_threshhold: int = 3, n_hits: int = 20) -> None:
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
        for i, record in enumerate(self.db):
            record = record.seq
            for j in tqdm(range(self.current_word_start, len(record) - (len(self.query) - (self.current_word_start + len(self.current_word))), 1)):
                if (score := self.get_matches(record[j:j + len(self.current_word)])) > self.threshhold:
                    self.seed_match(score, j, i)

    def search(self):
        self.get_word()
        continue_till_found = False
        while True:
            self.set_seeds()
            if sum([len(hits) for hits in self.hits.values()]) == 0:
                if not len(self.current_word) == len(self.query):
                    print("\n   no seeds found, retrying with higher word length    \n")
                else: 
                    print("\n   no seeds found, retrying with lower threshhold    \n")
                if len(self.current_word) == len(self.query) and not continue_till_found:
                    continue_till_found = bool(str(input("\n  maximum length reached. No seeds could be placed. Continue with lower threshhold    \n  [Y]/[N]    \n")) in ["Y", "y"])
                    if not continue_till_found:
                        return False
                    else:
                        self.threshhold -= 1
                elif continue_till_found:
                    self.threshhold -= 1
            else:
                break
            self.extend_word()

        self.current_word = self.query
        for i, record in enumerate(self.db):
            record = record.seq
            self.hits[i] = {j: self.get_matches(record[j - self.current_word_start: j + len(self.query) - self.current_word_start]) for j in self.hits[i].keys()}
        return True
  
    def seed_match(self, score: int, index: int, record: int):
        if self.total_seeds == self.n_hits:
            if score <= self.current_min[2]:
                return
            self.hits[self.current_min[0]].pop(self.current_min[1])
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

    def summary(self) -> Summary:
        empty_list = []
        seq = [list(map(lambda item: {(i, item[1][0]): item[1][1]}, enumerate(dict(sorted(subdict[1].items(), key = lambda x: x[1])).items()))) for i, subdict in enumerate(self.hits.items())]

        for sublist in seq:
                empty_list += sublist

        empty_list = sorted(empty_list, key = lambda item: list(item.values())[0])
        return Summary(empty_list, self.current_word_start, self.query, self.db)

    def get_word(self):
        try:
            seed = rand.randint(0, len(self.query) - self.word_len - 1)
        except:
            seed = 0
        self.current_word = self.query[seed:seed + self.word_len]
        self.current_word_start = seed
    
    def extend_word(self):
        if self.current_word_start > 0:
            self.current_word_start -= 1
            self.current_word = self.query[self.current_word_start] + self.current_word
            self.word_len += 1
        elif len(self.current_word) < len(self.query):
            self.current_word += self.query[len(self.current_word)]
            self.word_len += 1
        else:
            pass
