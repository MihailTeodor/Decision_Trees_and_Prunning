import csv
from random import randrange
from random import shuffle


def manage_data(file, n, iteration, percentage):
    '''here we split the dataset in the 3 parts we need for the application: training_set(70%) and test_set(30%)
        then we split the training_set in the grow_set(70%) and the validation_set(30%)'''

    csvfile = open(file, 'r')
    fileToRead = csv.reader(csvfile)
    attributes = next(fileToRead)
# store the data in tmp_data as dictionary
    tmp_data = []
    for row in fileToRead:
        tmp_data.append(dict(zip(attributes, row)))
    shuffle(tmp_data)
# check if to continue the iteration
    if n > len(tmp_data):
        n = len(tmp_data)
        iteration = False
# create the data file with dimension n which will be used in current iteration
    data = []
    i = 0
    for row in tmp_data:
        if i < n:
            data.append(row)
            i += 1
    length = len(data)
# create the training_set and the test_set
    train_file = []
    test_file = []
    i = 0
    for row in data:
        if i < (length * 70) / 100:
            train_file.append(row)
            i += 1
        else:
            test_file.append(row)
# create the grow_set and the validation_set
    grow_file = []
    validation_file = []
    length = len(train_file)
    i = 0
    for row in train_file:
        if i < (length * 70) / 100:
            grow_file.append(row)
            i += 1
        else:
            validation_file.append(row)
# introduce the noise in the grow_set with indicated percentage
    grow_file = introduce_noise(grow_file, attributes[len(attributes) - 1], percentage)
    return grow_file, validation_file, test_file, attributes, iteration


def introduce_noise(data, target, percentage):
    '''method to introduce noise in the grow_set data '''

    target = target
    values = []
# store the possible values for the target attribute
    for row in data:
        if row[target] not in values:
            values.append(row[target])
# if only one possible value for the target attribute, don't introduce noise
    val_length = len(values)
    if val_length == 1:
        return data
# otherwise introduce noise by changing the target attribute value with another random value from the possible ones
    i = 0
    length = len(data)
    for row in data:
        value = row[target]
        if i < (length * percentage) / 100:
            while row[target] == value:
                k = randrange(val_length)
                row[target] = values[k]
            i += 1
        else:
            break

    shuffle(data)
    return data
