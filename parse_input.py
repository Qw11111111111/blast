from argparse import ArgumentParser
from Bio import SeqIO
from Bio.Seq import Seq
import random as rand

def parser():
    parser = ArgumentParser()
    parser.add_argument("sequence")
    parser.add_argument("database")
    parser.add_argument("-t", "--test", action="store_false", default=True)
    args = parser.parse_args()
    return args

class HandleInput:

    def __init__(self, args) -> None:
        self.file = args.sequence
        self.db = args.database
        self.test = False
        if args.test:
            self.test = True
        pass

    def parse_fasta(self):
        if self.test:
            return Seq("AAATTTCCCGGG")
        with open(self.file, "r") as f:
            seq = list(SeqIO.parse(f, "fasta"))

        return seq
    
    def parse_db(self):
        if self.test:
            return Seq(self.generate_random_sequence())
        else:
            with open(self.db, "r") as f:
                seq = list(SeqIO.parse(f, "fasta"))

        return seq

    def generate_random_sequence(self):
        seq = ""
        for _ in range(420):
            seq += rand.choice(["A", "T", "C", "G"])
        return seq