import math


class Tree:
    number_of_democrat = 0
    number_of_republican = 0
    entropy_value = 0.0
    feature_entropy_value = [0]*2
    feature_probability = [0]*2
    information_gain = 0.0

    def __init__(self, index, data_set):
        self.index = index
        self.data_set = data_set
        self.yes = None
        self.no = None

    def set_datasets(self, yes_dataset, no_dataset):
        self.yes_dataset = yes_dataset
        self.no_dataset = no_dataset

    def insert(self, data, is_yes):
        if is_yes and self.yes is None:
            self.yes = data
        elif not is_yes and self.no is None:
            self.no = data

    def set_number_of_democrat(self, democrat):
        self.number_of_democrat = democrat

    def set_number_of_republican(self, republican):
        self.number_of_republican = republican

    def calc_entropy(self, data_train, size_of_rows):
        self.set_number_of_republican(data_train[(data_train['result'] == 'republican')].__len__())
        self.set_number_of_democrat(data_train[(data_train['result'] == 'democrat')].__len__())
        if size_of_rows > 0:
            probability1 = self.number_of_democrat / size_of_rows
            probability2 = self.number_of_republican / size_of_rows
        else:
            probability1 = 0
            probability2 = 0

        value_entropy = 0.0
        if probability1 != 0.0 and probability2 != 0.0:
            value_entropy = -probability1 * math.log(probability1, 2) - probability2 * math.log(probability2, 2)
        elif probability1 != 0.0:
            value_entropy = -probability1 * math.log(probability1, 2)
        elif probability2 != 0.0:
            value_entropy = -probability2 * math.log(probability2, 2)

        self.entropy_value = value_entropy

    def calc_feature_entropy(self, data_train, feature_value, index):
        republican_length = data_train[(data_train['result'] == 'republican') &
                                       (data_train.iloc[:, self.index] == feature_value)].__len__()
        democrat_length = data_train[(data_train['result'] == 'democrat') &
                                     (data_train.iloc[:, self.index] == feature_value)].__len__()

        self.feature_probability[index] = republican_length+democrat_length

        if self.number_of_republican == 0:
            probability1 = 0
        else:
            probability1 = republican_length / self.number_of_republican
        if self.number_of_democrat == 0:
            probability2 = 0
        else:
            probability2 = democrat_length / self.number_of_democrat

        value_of_entropy = 0.0
        if probability1 != 0.0 and probability2 != 0.0:
            value_of_entropy = -probability1 * math.log(probability1, 2) - probability2 * math.log(probability2, 2)
        elif probability1 != 0.0:
            value_of_entropy = -probability1 * math.log(probability1, 2)
        elif probability2 != 0.0:
            value_of_entropy = -probability2 * math.log(probability2, 2)

        self.feature_entropy_value[index] = value_of_entropy

    def calc_information_gain(self, data_train_size):
        if data_train_size == 0:
            self.information_gain = self.entropy_value
        else:
            self.information_gain = \
                self.entropy_value - self.feature_probability[0]/data_train_size*self.feature_entropy_value[0] -\
                self.feature_probability[1]/data_train_size*self.feature_entropy_value[1]

    def height(self, root):
        if root is None:
            return 0
        yes_ans = self.height(root.yes)
        no_ans = self.height(root.no)
        return max(yes_ans, no_ans) + 1
