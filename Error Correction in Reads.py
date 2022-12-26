from typing import List, Tuple
from collections import Counter

def load_fasta(filepath: str, is_dict: bool = False):
    name_list, seq_list = [], []
    with open(filepath, 'r') as fasta:
        while True:
            line = fasta.readline()
            if not line:
                break
            data = line.strip()
            if data.startswith('>'):
                name_list.append(data[1:])
                line = fasta.readline().strip()
                seq_list.append(line)
            else:
                seq_list[len(seq_list) - 1] += line.strip()
    print(f"Load {len(seq_list)} fasta seqs from {filepath}")
    if is_dict:
        fasta_dict = {}
        # name_list, seq_list = load_fasta(filepath)
        for i, name in enumerate(name_list):
            fasta_dict[name] = seq_list[i]
        return fasta_dict
    else:
        return name_list, seq_list

def reverse_complement(seq: str, t: str = 'DNA') -> str:
    comp_dict = {}
    if t == 'DNA' or 'dna':
        comp_dict = {
            'A': 'T',
            'T': 'A',
            'C': 'G',
            'G': 'C'
        }
    elif t == 'RNA' or 'rna':
        comp_dict = {
            'A': 'U',
            'U': 'A',
            'C': 'G',
            'G': 'C'
        }
    else:
        print(f'Wrong type {t} for sequence to complement')
        exit(1)

    seq = seq.upper()  # dict is for upper case
    reverse_seq = seq[::-1]
    res = [comp_dict[n] for n in reverse_seq]

    return list_2_str(res, sep='')

def list_2_str(x: list, sep: str = ' '):
    return sep.join([str(item) for item in x])

def hamming_distance(s1: str, s2: str):
    if len(s1) != len(s2):
        raise ValueError("Not the same length!")

    return sum(es1 != es2 for es1, es2 in zip(s1, s2))


def load_data(filepath: str):
    return load_fasta(filepath)[1]


def seqs_expansion(seqs: str):
    expand_seqs = []
    for seq in seqs:
        expand_seqs.append(seq)
        expand_seqs.append(reverse_complement(seq))
    return expand_seqs


def correct_incorrect(counts, orig_seqs):
    correct = []
    incorrect = []
    for s in counts:
        if counts[s] >= 2:
            correct.append(s)
        elif s in orig_seqs:
            incorrect.append(s)
    return correct, incorrect


def error_correction(corrs: list, incorrs: list):
    correct_tuples = []
    for s1 in incorrs:
        for s2 in corrs:
            if hamming_distance(s1, s2) == 1:
                correct_tuples.append((s1, s2))
    return correct_tuples


def save_corrections(filepath: str, corrections: List[Tuple]):
    out = open(filepath, 'w')
    for s1, s2 in corrections:
        out.write(f"{s1}->{s2}\n")
    out.close()
    print(f"Save result to {filepath}.")


if __name__ == '__main__':
    path = "rosalind_corr.txt"
    outpath = "datasets/034.corr.out"
    
    seqs = load_data(path)
    expand_seqs = seqs_expansion(seqs)
    counter = Counter(expand_seqs)
    corr_seqs, incorr_seqs = correct_incorrect(counter, seqs)
    corrections = error_correction(corr_seqs, incorr_seqs)
    
    save_corrections(outpath, corrections)