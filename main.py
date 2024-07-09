from search import ALign_seq
from parse_input import parser, HandleInput

def main(args):
    handle = HandleInput(args)
    seq = handle.parse_fasta()
    database = handle.parse_db()
    searcher = ALign_seq(seq, database)
    searcher.search()

    summary = searcher.summary()
    print(database)

    print(summary)
    print("best hit: ", "\n", "\t", seq, "\n", "\t", database[list(summary[-1].keys())[0][1] - searcher.current_word_start: list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq)])
    

if __name__ == "__main__":
    args = parser()
    main(args)