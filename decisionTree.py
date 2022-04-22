import pandas as pd
import numpy as np
import random
import statistics
from Tree import Tree
from testData import TestData
from trainData import TrainData


data = pd.read_csv('house-votes-84.data.txt', sep=",",
                   names=['result', 'handicapped', 'water-project',
                          'budget-resolution', 'physician',
                          'el-salvador', 'religious',
                          'anti-satellite', 'nicaraguan-contras',
                          'mx-missile', 'immigration', 'corporation',
                          'education', 'superfund', 'crime',
                          'duty', 'export-administration'])

# splitting data to test and train #
data_test = data[109:]
data_train = data[:109]

size_of_rows = data_train.__len__()

head = None

features_list = []


print("The Iteration with the 25% split: ")
#   initializing the nodes of the tree
for i in range(1, 17):
    features_list.append(Tree(i, data_train))

training = TrainData(features_list)
head = training.train(data_train, head)
print("Tree height: ", head.height(head))


test_object = TestData(data_test.values)
test_object.matching_testdata(head)
print("*********************************************************")
print("********************** All test Data **************************")
for i in range(5):
    start_random_number = random.randint(0, data.__len__() - 109)
    end_random_number = start_random_number + 109
    data_test = data[0:start_random_number]
    append = data[end_random_number:].values
    data_test = data_test.values

    new_data_test = np.append(data_test, append, axis=0)

    data_train = data[start_random_number:end_random_number]
    head = None
    for j in range(1, 17):
        features_list.append(Tree(j, data_train))

    print("The ", i+1, "Iteration with the random split ", start_random_number, " and ", end_random_number, " : ")

    training = TrainData(features_list)
    head = training.train(data_train, head)

    print("Tree height: ", head.height(head))

    test_object = TestData(new_data_test)
    test_object.matching_testdata(head)
    print("*********************************************************")

print("*********************************************************")
print("*********************************************************")
print("*********************************************************")

size_percentage = 30
accuracy_list = []
tree_height_list = []
for i in range(5):
    split_index = round((len(data)*size_percentage)/100)
    print(split_index)
    data_test = data[split_index:].values
    data_train = data[:split_index]
    head = None
    for j in range(1, 17):
        features_list.append(Tree(j, data_train))

    print("The ", i+1, "Iteration with the split ", size_percentage, "(", round((len(data)*size_percentage)/100),
          ")percentage : ")

    training = TrainData(features_list)
    head = training.train(data_train, head)

    print("Tree height: ", head.height(head))
    tree_height_list.append(head.height(head))

    test_object = TestData(data_test)
    test_object.matching_testdata(head)
    accuracy_list.append(test_object.calc_accuracy())
    size_percentage += 10
    print("*********************************************************")

accuracy_mean = statistics.mean(accuracy_list)
accuracy_max = max(accuracy_list)
accuracy_min = min(accuracy_list)
print("accuracy mean: ", accuracy_mean, "     ||   accuracy max: ", accuracy_max, "    ||  accuracy min: ",
      accuracy_min)

tree_height_mean = statistics.mean(tree_height_list)
tree_height_max = max(tree_height_list)
tree_height_min = min(tree_height_list)
print("tree height mean: ", tree_height_mean, "  || tree height max: ", tree_height_max, " || tree height min: ",
      tree_height_min)

print("*********************************************************")
print("*********************************************************")
print("*********************************************************")
