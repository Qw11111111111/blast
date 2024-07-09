from search import ALign_seq
from parse_input import parser, HandleInput
from time import perf_counter

def main(args):
    handle = HandleInput(args)
    seq = handle.parse_fasta()
    database = handle.parse_db()
    n = args.n
    threshhold = args.Threshhold
    length = args.length
    searcher = ALign_seq(seq, database, length, threshhold, n)
    t1 = perf_counter()
    searcher.search()

    summary = searcher.summary()
    t2 = perf_counter()

    normal = t2 - t1
    if args.exhaustive:
        searcher_exhaustive = ALign_seq(seq, database, len(seq[0].seq), length, threshhold, n)
        t1 = perf_counter()
        searcher_exhaustive.search()

        summary2 = searcher_exhaustive.summary()
        t2 = perf_counter()
        exhaustive = t2 - t1

    #print(summary)
    #print(searcher.current_word)
    #print(searcher.current_word_start)
    if args.test:
        print("best hit: ", "\n", "\t", seq, "\n", "\t", database[list(summary[-1].keys())[0][1] - searcher.current_word_start: list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq)])
    else:
        print("best hit:")
        print(seq[0].seq)
        print(database[list(summary[-1].keys())[0][0]].seq[list(summary[-1].keys())[0][1] - searcher.current_word_start - 1:list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq[0].seq) - 1])
        print(f"similarity: {list(summary[-1].values())[0] / len(seq[0].seq) * 100:.3f}%")

        #print("actual best:")
        #print(database[0].seq[0:len(seq[0].seq)])
        #print(f"similarity: {get_similarity(database[0].seq[0:len(seq[0].seq)], seq[0].seq) / len(seq[0].seq) * 100:.3f}%")
        print(f"Blast: {normal:.3f}s")
        if args.exhaustive:
            print(f"exhaustive: {exhaustive:.3f}s")

            print("exhaustive sequence: ")
            print(database[list(summary2[-1].keys())[0][0]].seq[list(summary2[-1].keys())[0][1] - searcher_exhaustive.current_word_start:list(summary2[-1].keys())[0][1] - searcher_exhaustive.current_word_start + len(seq[0].seq)])

def get_similarity(seq1, seq2):
    n = 0
    for i, letter in enumerate(seq1):
        if letter == seq2[i]:
            n += 1

    return n

if __name__ == "__main__":
    args = parser()
    main(args)