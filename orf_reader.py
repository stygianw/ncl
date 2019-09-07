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
                key = line[1:].split()[0]
                result[key] = ''
            else:
                result[key] = result[key] + line
    return result


def organize_data(data):
    for name, sequence in data.items():
        data[name] = []
        for reading in range(3):
            forward = find_all_orfs_in_reading(sequence, reading)
            backward = find_all_orfs_in_reading(sequence, reading, True)
            data[name].append((forward, backward))
    return data


def find_all_orfs_in_reading(sequence, offset = 0, reverse = False):
    result_list = []
    if reverse:
        sequence = ''.join(reversed(sequence))
    current_segments = []
    for current_idx in range(offset, len(sequence), 3):
        portion = ''.join(sequence[current_idx:current_idx + 3])
        if(portion == SEQ_START):
            current_segments.append([current_idx + 1, ''])
        if current_segments:
            for current_segment in current_segments:
                current_segment[1] += portion
        if current_segments and portion in SEQ_END:
            result_list.extend((x[0], x[1]) for x in current_segments)
            current_segments.clear()
    return result_list


def provide_organized_data():
    raw_data = read_file('dna2.fasta')
    organized_data = organize_data(raw_data)
    return organized_data


if __name__ == '__main__':
    pass


def test_find_all_orfs_in_reading_reading2():
    result = find_all_orfs_in_reading('AATGAATAACTAGGTAATGGAGTGAAATA', 1)
    assert len(result) == 2
    assert result[0][0] == 2
    assert result[0][1] == "ATGAATAACTAG"
    assert result[1][0] == 17
    assert result[1][1] == "ATGGAGTGA"

def test_find_all_orfs_in_reading_reading2_reversed():
    result = find_all_orfs_in_reading('AATGAATAACTAGGTAATGGAGTGAAATA', 1, True)
    assert len(result) == 1
    assert result[0][0] == 14
    assert result[0][1] == "ATGGATCAATAA"


def test_find_all_orfs_in_reading_reading2_nested():
    result = find_all_orfs_in_reading('AATGAAGTCAATGAACTAGGTAATGGAGTGAAATA', 1)
    assert len(result) == 3
    assert result[0][0] == 2
    assert result[0][1] == "ATGAAGTCAATGAACTAG"
    assert result[1][0] == 11
    assert result[1][1] == "ATGAACTAG"
    assert result[2][0] == 23
    assert result[2][1] == "ATGGAGTGA"


def test_find_all_orfs_in_reading_reading1_notfound():
    result = find_all_orfs_in_reading('AATGAAGAACTAGGTAATGGAGTGAAATA', 0)
    assert len(result) == 0


def test_organize_data():
    incoming_data = {'test_name': 'AATGAATAACTAGGTAATGGAGTGAAATA'}
    organized_data = organize_data(incoming_data)
    assert len(organized_data.keys()) == 1
    assert 'test_name' in organized_data
    assert len(organized_data['test_name']) == 3
    forward_read2, backward_read2 = organized_data['test_name'][1]
    forward_indices_read2 = [x[0] for x in forward_read2]
    assert 2 in forward_indices_read2 and 17 in forward_indices_read2
    forward_orfs_read2 = [x[1] for x in forward_read2]
    assert "ATGAATAACTAG" in forward_orfs_read2 and "ATGGAGTGA" in forward_orfs_read2
    backward_indices_read2 = [x[0] for x in backward_read2]
    assert 14 in backward_indices_read2
    backward_orfs_read2 = [x[1] for x in backward_read2]
    assert "ATGGATCAATAA" in backward_orfs_read2

