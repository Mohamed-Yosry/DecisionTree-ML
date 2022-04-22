class TestData:

    def __init__(self, test_data):
        self.test_data = test_data
        self.count_democrat = 0
        self.count_republican = 0
        self.correct_prediction = 0
        self.predicted_expected = ['', False]

    def matching_recursion(self, temp_node, prev_node, is_yes, i):
        if temp_node is None:
            republican_length = 0
            democrat_length = 0
            if prev_node.yes is None and is_yes is 'y':
                republican_length = prev_node.yes_dataset[(prev_node.yes_dataset['result'] == 'republican') & (
                            prev_node.yes_dataset.iloc[:, prev_node.index] == is_yes)].__len__()
                democrat_length = prev_node.yes_dataset[(prev_node.yes_dataset['result'] == 'democrat') & (
                            prev_node.yes_dataset.iloc[:, prev_node.index] == is_yes)].__len__()
            if prev_node.no is None and is_yes is 'n':
                republican_length = prev_node.no_dataset[(prev_node.no_dataset['result'] == 'republican') & (
                            prev_node.no_dataset.iloc[:, prev_node.index] == is_yes)].__len__()
                democrat_length = prev_node.no_dataset[(prev_node.no_dataset['result'] == 'democrat') & (
                            prev_node.no_dataset.iloc[:, prev_node.index] == is_yes)].__len__()
            if (republican_length > 0 and democrat_length > 0) or (republican_length == 0 and democrat_length == 0):
                if republican_length > democrat_length:
                    if self.test_data[i][0] == "republican":
                        self.predicted_expected[1] = True
                        self.correct_prediction += 1
                    self.predicted_expected[0] = "republican"
                    self.count_republican += 1
                else:
                    if self.test_data[i][0] == "democrat":
                        self.predicted_expected[1] = True
                        self.correct_prediction += 1
                    self.predicted_expected[0] = "democrat"
                    self.count_democrat += 1
            elif republican_length == 0:
                if self.test_data[i][0] == "democrat":
                    self.predicted_expected[1] = True
                    self.correct_prediction += 1
                self.count_democrat += 1
                self.predicted_expected[0] = "democrat"
            elif democrat_length == 0:
                if self.test_data[i][0] == "republican":
                    self.predicted_expected[1] = True
                    self.correct_prediction += 1
                self.count_republican += 1
                self.predicted_expected[1] = "republican"
            return

        prev_node = temp_node
        if self.test_data[i][temp_node.index] is 'y':
            temp_node = temp_node.yes
            is_yes = 'y'
            self.matching_recursion(temp_node, prev_node, is_yes, i)
        elif self.test_data[i][temp_node.index] is 'n':
            temp_node = temp_node.no
            is_yes = 'n'
            self.matching_recursion(temp_node, prev_node, is_yes, i)
        elif self.test_data[i][temp_node.index] is '?':
            if temp_node.no is not None:
                self.matching_recursion(temp_node.no, prev_node, 'n', i)
            if temp_node.yes is not None:
                self.matching_recursion(temp_node.yes, prev_node, 'y', i)

    def calc_accuracy(self):
        return self.correct_prediction / len(self.test_data) * 100

    def matching_testdata(self, tree_head):
        prev_node = tree_head
        is_yes = '0'

        for i in range(len(self.test_data)):
            temp_node = tree_head
            self.matching_recursion(temp_node, prev_node, is_yes, i)
        print("correct prediction: ", self.correct_prediction, "   ||   of: ", len(self.test_data),
              " ||   accuracy: ", self.calc_accuracy())
