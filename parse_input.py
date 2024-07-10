from argparse import ArgumentParser
from Bio import SeqIO
from Bio.Seq import Seq
import random as rand

def parser():
    parser = ArgumentParser()
    parser.add_argument("sequence")
    parser.add_argument("database")
    parser.add_argument("-e", "--exhaustive", action="store_true", default=False)
    parser.add_argument("-l", "--length", action="store", type=int, default=10, help="the length of the word durign search")
    parser.add_argument("-T", "--Threshhold", action="store", type=int, default=10, help="the threshhold for sequences to be accepted")
    parser.add_argument("-n", action="store", type=int, default=100, help="number of postions stored")
    args = parser.parse_args()
    return args

class HandleInput:

    def __init__(self, args) -> None:
        self.file = args.sequence
        self.db = args.database

    def parse_fasta(self):
        with open(self.file, "r") as f:
            seq = list(SeqIO.parse(f, "fasta"))
        return seq
    
    def parse_db(self):
        with open(self.db, "r") as f:
            seq = list(SeqIO.parse(f, "fasta"))
        return seq

    def generate_random_sequence(self):
        seq = ""
        for _ in range(420):
            seq += rand.choice(["A", "T", "C", "G"])
        return seq