import numpy as np



seq = {100: 70, 2: 30, 20: 20}

for item in seq.items():
    print(item)

print(np.argmin(list(seq.values())))
print(seq.items())

print(dict(sorted(seq.items(), key = lambda x: x[1])))
seq_iter = enumerate(seq.items())
seq_2 = dict(map(lambda x: x[1] if x[0] != 0 else (42, 42), seq_iter))
print(seq_2)
hits = {0: {1: 10, 3: 4}, 1: {}, 2: {1: 2}}
#for i, item in enumerate(hits.items()):
    #print(i, item)
    #print(dict(sorted(item[1].items(), key = lambda x: x[1])).items(), "wuhwu")

empty_list = []
seq = [list(map(lambda item: {(i, item[1][0]): item[1][1]}, enumerate(dict(sorted(subdict[1].items(), key = lambda x: x[1])).items()))) for i, subdict in enumerate(hits.items())]

for sublist in seq:
        empty_list += sublist

print(sorted(empty_list, key = lambda item: list(item.values())[0]))