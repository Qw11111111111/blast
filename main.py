from search import AlignSeq
from parse_input import parser, HandleInput
from time import perf_counter

def main(args):
    handle = HandleInput(args)
    seq = handle.parse_fasta()
    database = handle.parse_db()
    n = args.n
    threshhold = args.Threshhold
    length = args.length
    searcher = AlignSeq(seq, database, length, threshhold, n)
    t1 = perf_counter()
    res = searcher.search()
    if not res:
        print("no match found")
        return
    summary = searcher.summary()
    t2 = perf_counter()

    normal = t2 - t1
    if args.exhaustive:
        searcher_exhaustive = AlignSeq(seq, database, length, threshhold, n)
        t1 = perf_counter()
        res = searcher_exhaustive.search()
        if not res:
            print("no match found")
            return

        summary2 = searcher_exhaustive.summary()
        t2 = perf_counter()
        exhaustive = t2 - t1

    if args.test:
        print("best hit: ", "\n", "\t", seq, "\n", "\t", database[list(summary[-1].keys())[0][1] - searcher.current_word_start: list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq)])
    else:
        print("best hit:")
        print(f"Query:  {seq[0].seq}")
        print(f"DB_Seq: {summary.best_sequence}")
        print(f"Similarity: {summary.similarity:.3f}%")
        #print(database[list(summary[-1].keys())[0][0]].seq[list(summary[-1].keys())[0][1] - searcher.current_word_start - 1:list(summary[-1].keys())[0][1] - searcher.current_word_start + len(seq[0].seq) - 1])
        #print(f"similarity: {list(summary[-1].values())[0] / len(seq[0].seq) * 100:.3f}%")


        print(f"Blast: {normal:.3f}s")
        if args.exhaustive:
            print(f"exhaustive: {exhaustive:.3f}s")

            print("exhaustive sequence: ")
            print(f"Query:  {seq[0].seq}")
            print(f"DB_Seq: {summary2.best_sequence}")
            print(f"Similarity: {summary2.similarity:.3f}%")
            #print(database[list(summary2[-1].keys())[0][0]].seq[list(summary2[-1].keys())[0][1] - searcher_exhaustive.current_word_start:list(summary2[-1].keys())[0][1] - searcher_exhaustive.current_word_start + len(seq[0].seq)])

def get_similarity(seq1, seq2):
    n = 0
    for i, letter in enumerate(seq1):
        if letter == seq2[i]:
            n += 1

    return n

if __name__ == "__main__":
    args = parser()
    main(args)