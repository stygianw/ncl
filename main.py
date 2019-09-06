from orf_reader import provide_organized_data


def task1_longest_orf_reading2(organized_data):
    reading2_idx = 1
    all_reading2_orfs = (orf_data[1] for readings in organized_data.values() 
                         for direction in readings[reading2_idx] 
                         for orf_data in direction)
    longest_orf = max(all_reading2_orfs, key=lambda x: len(x))
    return len(longest_orf)


def task2_position_of_longest_orf_reading3(organized_data):
    reading3_idx = 2
    all_reading3_data = (orf_data for readings in organized_data.values() 
                         for direction in readings[reading3_idx] 
                         for orf_data in direction)
    longest_orf = max(all_reading3_data, key=lambda x: len(x[1]))
    longest_orf_position, _ = longest_orf
    return longest_orf_position


def task3_longest_forward_orf(organized_data):
    all_forward_orfs = (forward_orf for readings in organized_data.values() 
                        for reading in readings for forward_orf in reading[0])
    longest_orf = max(all_forward_orfs, key=lambda x: len(x[1]))
    return len(longest_orf[1])
    

def task4_longest_by_identifier(organized_data):
    identifier = "gi|142022655|gb|EQ086233.1|16"
    identifier_data = organized_data[identifier]
    all_orfs = (orf_data for reading in identifier_data 
                for direction in reading 
                for orf_data in direction)
    longest_orf = max(all_orfs, key=lambda x: len(x[1]))
    return len(longest_orf[1])


def main():
    organized_data = provide_organized_data()
    print(task1_longest_orf_reading2(organized_data))
    print(task2_position_of_longest_orf_reading3(organized_data))
    print(task3_longest_forward_orf(organized_data))
    print(task4_longest_by_identifier(organized_data))


if __name__ == '__main__':
    main()