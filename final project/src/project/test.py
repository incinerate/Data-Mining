
import csv

if __name__ == '__main__':
    ground_truth = csv.reader(open('test_label.csv'))
    total = 0
    correct = 0
    for row in ground_truth:
        if row[0] == 'enrollment_id':
            continue
        total = total + 1
        if abs(float(row[1])- float(row[-1]))<0.5:
            correct = correct + 1
    print correct
    print total
    print float(correct) / float(total)
    pass