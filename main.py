from search import ALign_seq
from parse_input import parser, HandleInput

def main(args):
    handle = HandleInput(args)
    seq = handle.parse_fasta()
    database = handle.parse_db()
    searcher = ALign_seq(seq, database) 
    searcher.search()

    summary = searcher.summary()

    print(summary)
    print(searcher.current_word)
    print(searcher.current_word_start)
    if args.test:
        print("best hit: ", "\n", "\t", seq, "\n", "\t", database[list(summary[-1].keys())[0][1] - searcher.current_word_start: list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq)])
    else:
        print("best hit:")
        print(seq[0].seq)
        print(database[list(summary[-1].keys())[0][0]].seq[list(summary[-1].keys())[0][1] - searcher.current_word_start:list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq[0].seq)])

        print("actual best:")
        print(database[0].seq[0:len(seq[0].seq)])

if __name__ == "__main__":
    args = parser()
    main(args)