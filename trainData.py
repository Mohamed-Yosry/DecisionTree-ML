class TrainData:

    def __init__(self, features_list):
        self.features_list = features_list

    def max_information_gain_function(self, data_train):
        max_gain = -100  # sys.float_info.min       # 2.2250738585072014e-308
        index_of_max_gain = 0
        for i in range(1, self.features_list.__len__() + 1):
            self.features_list[i - 1].calc_entropy(data_train, data_train.__len__())
            self.features_list[i - 1].calc_feature_entropy(data_train, 'y', 0)
            self.features_list[i - 1].calc_feature_entropy(data_train, 'n', 1)
            self.features_list[i - 1].calc_information_gain(data_train.__len__())
            if self.features_list[i - 1].information_gain > max_gain:
                max_gain = self.features_list[i - 1].information_gain
                index_of_max_gain = i

        return max_gain, index_of_max_gain

    def train(self, data_train, head):

        (max_gain, index_of_max_gain) = self.max_information_gain_function(data_train)
        if head is None:
            head = self.features_list[index_of_max_gain - 1]
        self.features_list.remove(self.features_list[index_of_max_gain - 1])
        yes_data_set = data_train[(data_train.iloc[:, index_of_max_gain] == 'y')]
        no_data_set = data_train[(data_train.iloc[:, index_of_max_gain] == 'n')]
        head.set_datasets(yes_data_set, no_data_set)
        temp_head = head
        self.create_tree_recursively(temp_head)
        return head

    def create_tree_recursively(self, temp_node):
        # print("temp node: ", temp_node.entropy_value)
        if temp_node.yes is None and self.features_list:
            (temp_max_gain, temp_index_of_max_gain) = self.max_information_gain_function(temp_node.yes_dataset)
            self.features_list[temp_index_of_max_gain - 1].calc_entropy(temp_node.yes_dataset,
                                                                        temp_node.yes_dataset.__len__())
            entropy = self.features_list[temp_index_of_max_gain - 1].entropy_value
            if entropy != 0:
                yes_data_set = temp_node.yes_dataset[(temp_node.yes_dataset.iloc[:, temp_index_of_max_gain] == 'y')]
                no_data_set = temp_node.yes_dataset[(temp_node.yes_dataset.iloc[:, temp_index_of_max_gain] == 'n')]
                self.features_list[temp_index_of_max_gain - 1].set_datasets(yes_data_set, no_data_set)
                temp_node.yes = self.features_list[temp_index_of_max_gain - 1]
                self.features_list.remove(self.features_list[temp_index_of_max_gain - 1])
                self.create_tree_recursively(temp_node.yes)

        if temp_node.no is None and self.features_list:
            (temp_max_gain, temp_index_of_max_gain) = self.max_information_gain_function(temp_node.no_dataset)
            self.features_list[temp_index_of_max_gain - 1].calc_entropy(temp_node.no_dataset,
                                                                        temp_node.no_dataset.__len__())
            entropy = self.features_list[temp_index_of_max_gain - 1].entropy_value
            if entropy != 0:
                yes_data_set = temp_node.no_dataset[(temp_node.no_dataset.iloc[:, temp_index_of_max_gain] == 'y')]
                no_data_set = temp_node.no_dataset[(temp_node.no_dataset.iloc[:, temp_index_of_max_gain] == 'n')]
                self.features_list[temp_index_of_max_gain - 1].set_datasets(yes_data_set, no_data_set)
                temp_node.no = self.features_list[temp_index_of_max_gain - 1]
                temp_node.no = self.features_list[temp_index_of_max_gain - 1]
                self.features_list.remove(self.features_list[temp_index_of_max_gain - 1])
                self.create_tree_recursively(temp_node.no)
