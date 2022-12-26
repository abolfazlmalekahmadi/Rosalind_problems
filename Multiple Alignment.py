
from itertools import product, combinations

import numpy as np

DATASET_FILE = 'rosalind_mult.txt'
PENALTY = -1


def _run():
    with open(DATASET_FILE) as f:
        proteins = _parse_fasta_lines(list(f))
        print(proteins)
    return _dp_alignment(proteins)


def _parse_fasta_lines(fasta_lines):
    proteins = []
    for line in fasta_lines:
        if line[0] == '>':
            proteins.append("")
        else:
            proteins[-1] += line.strip()

    return proteins


def _dp_alignment(proteins):
    table = np.zeros(tuple(len(p) + 1 for p in proteins)).astype(int)
    back_pointers, chars = {}, {}

    for index in _dp_bottom_up_indices(table.shape):
        
        cands_tab_idxs, curr_tab_idxs_subs = _calc_candidate_indices(index)

        cands_chars = _calc_candidate_chars(index, proteins, curr_tab_idxs_subs)
        scores = [_calc_score(c) for c in cands_chars]

        cands = zip(scores, cands_tab_idxs, cands_chars)
        cands = [(table[i] + s, i, c) for s, i, c in cands]
        max_ = max(cands, key=lambda x: x[0])

        table[index] = max_[0]
        back_pointers[index] = max_[1]
        chars[index] = max_[2]

    end_pos = tuple(x - 1 for x in table.shape)
    score = table[end_pos]
    alignment = _back_trace(end_pos, back_pointers, chars)
    return score, alignment


def _dp_bottom_up_indices(shape):
    indices = [i for i in np.ndindex(shape)]
    sorted_indices = sorted(indices, key=lambda t: _num_zeros(t), reverse=True)
   
    for index in sorted_indices[1:]:
        yield index
        print(index)


def _num_zeros(tuple_):
    return sum(1 if x == 0 else 0 for x in tuple_)


def _calc_candidate_indices(index):
    mask = tuple(1 if x != 0 else 0 for x in index)
    cand_idxs_subs = list(product((0, 1), repeat=len(index)))[1:]
    cand_idxs_subs = [x for x in cand_idxs_subs if _feasible_cand(x, mask)]

    cand_idxs = []
    for cand_idxs_sub in cand_idxs_subs:
        cand_idxs.append(tuple(x - y for x, y in zip(index, cand_idxs_sub)))
    return cand_idxs, cand_idxs_subs


def _feasible_cand(idx_sub, mask):
    return all(True if s == 0 else m == 1 for s, m in zip(idx_sub, mask))


def _calc_candidate_chars(index, proteins, indices_subs):
    chars = []
    for idxs, sub in zip([index] * len(indices_subs), indices_subs):
        char = ""
        for i, s, p in zip(idxs, sub, proteins):
            if s == 0:
                char += '-'
            else:
                char += p[i - 1]
        chars.append(char)
    return chars


def _calc_score(char):
    return sum(0 if c[0] == c[1] else PENALTY for c in combinations(char, 2))


def _back_trace(end_pos, back_pointers, chars):
    curr_pos, align_elems = end_pos, []

    while not sum(curr_pos) == 0:
        align_elems.append(chars[curr_pos])
        curr_pos = back_pointers[curr_pos]

    align_elems = reversed(align_elems)
    alignment = [''.join(a) for a in zip(*[ae for ae in align_elems])]
    return '\n'.join(alignment)


if __name__ == '__main__':
    score_, alignment_ = _run()
    print(score_)
    print(alignment_)
