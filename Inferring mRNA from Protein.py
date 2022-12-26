from collections import Counter
from functools import reduce
from operator import mul


RNA_CODON_MAP = {
	"UUU": 'F', "UUC": 'F', 
    "UUA": 'L',    "UUG": 'L',
	"UCU": 'S', "UCC": 'S', "UCA": 'S',    "UCG": 'S',
	"UAU": 'Y', "UAC": 'Y', 
    "UAA": 'Stop', "UAG": 'Stop',"UGA": 'Stop',
	"UGU": 'C', "UGC": 'C',  "UGG": 'W',
	"CUU": 'L', "CUC": 'L', "CUA": 'L',    "CUG": 'L',
	"CCU": 'P', "CCC": 'P', "CCA": 'P',    "CCG": 'P',
	"CAU": 'H', "CAC": 'H', 
    "CAA": 'Q',    "CAG": 'Q',
	"CGU": 'R', "CGC": 'R', "CGA": 'R',    "CGG": 'R',
	"AUU": 'I', "AUC": 'I', "AUA": 'I',    "AUG": 'M',
	"ACU": 'T', "ACC": 'T', "ACA": 'T',    "ACG": 'T',
	"AAU": 'N', "AAC": 'N',
    "AAA": 'K',    "AAG": 'K',
	"AGU": 'S', "AGC": 'S',
    "AGA": 'R',    "AGG": 'R',
	"GUU": 'V', "GUC": 'V', "GUA": 'V',    "GUG": 'V',
	"GCU": 'A', "GCC": 'A', "GCA": 'A',    "GCG": 'A',
	"GAU": 'D', "GAC": 'D', 
    "GAA": 'E',    "GAG": 'E',
	"GGU": 'G', "GGC": 'G', "GGA": 'G',    "GGG": 'G'
}

AA_POSS = Counter(RNA_CODON_MAP.values())
with open("rosalind_mrna.txt") as f:
	s = f.readline().strip()
print((reduce(mul, [AA_POSS[c] for c in s]) * AA_POSS["Stop"]) % 1000000)