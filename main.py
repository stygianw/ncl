from itertools import islice, chain

SEQ_START = 'ATG'
SEQ_END = ['TAA', 'TAG', 'TGA']


def read_file(filename):
    result = { }
    with open(filename, 'r') as f:
        key = None
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                key = line
                result[key] = ''
            else:
                result[key] = result[key] + line
    return result
            

def find_longest_orf_in_reading_2():
    data = read_file('dna2.fasta')
    lengths = []
    for sequence in data.values():
        forward = find_all_orfs_in_reading(sequence, 1)
        backward = find_all_orfs_in_reading(''.join(reversed(sequence)), 1)
        lengths.extend([len(x[1]) for x in forward])
        lengths.extend([len(x[1]) for x in backward])
    return max(lengths)
    

def any_sequence_any_forward_longest_length():
    data = read_file('dna2.fasta')
    all_results = []
    for sequence in data.values():
        reading1 = find_all_orfs_in_reading(sequence, 0)
        reading2 = find_all_orfs_in_reading(sequence, 1)
        reading3 = find_all_orfs_in_reading(sequence, 2)
        all_results.extend(x for x in reading1)
        all_results.extend(x for x in reading2)
        all_results.extend(x for x in reading3)
    longest_element = max(all_results, key=lambda x: len(x[1]))
    return len(longest_element[1])


def starting_position_in_longest_orf_reading3():
    data = read_file('dna2.fasta')
    all_results = []
    for sequence in data.values():
        forward = find_all_orfs_in_reading(sequence, 2)
        backward = find_all_orfs_in_reading(''.join(reversed(sequence)), 2)
        all_results.extend(x for x in forward)
        all_results.extend(x for x in backward)
    longest_element = max(all_results, key=lambda x: len(x[1]))
    return longest_element[0] + 1

def find_all_orfs_in_reading(sequence, offset = 0):
    result_list = []
    orf_started = False; orf_start_idx = None
    current_orf = ''
    for current_idx in range(offset, len(sequence), 3):
        portion = ''.join(sequence[current_idx:current_idx + 3])
        if(portion == SEQ_START and not orf_started):
            orf_start_idx = current_idx
            orf_started = True
        if orf_started:
            current_orf += portion
        if orf_started and portion in SEQ_END:
            result_list.append((orf_start_idx, current_orf, sequence))
            orf_start_idx = None
            orf_started = False
            current_orf = ''
    return result_list


print(any_sequence_any_forward_longest_length())


def test_find_all_orfs_in_reading_reading2():
    result = find_all_orfs_in_reading('AATGAAGAACTAGGTAATGGAGTGAAATA', 1)
    assert len(result) == 2
    assert result[0][0] == 1
    assert result[0][1] == "ATGAAGAACTAG"
    assert result[1][0] == 16
    assert result[1][1] == "ATGGAGTGA"


def test_find_all_orfs_in_reading_reading1_notfound():
    result = find_all_orfs_in_reading('AATGAAGAACTAGGTAATGGAGTGAAATA', 0)
    assert len(result) == 0
