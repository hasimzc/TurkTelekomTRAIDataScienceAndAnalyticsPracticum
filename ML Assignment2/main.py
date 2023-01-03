import pandas as pd
import numpy as np
import pprint
dataset = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")  # importing the dataset from the disk
dataset_array = dataset.to_numpy()
np.random.shuffle(dataset_array)
row = dataset.shape[0]


def discretize(arr, steps):
    maxvalue = np.max(arr)
    minvalue = np.min(arr)
    difference = maxvalue - minvalue
    step_size = difference / steps
    for k in range(0, len(arr)):
        if arr[k] == maxvalue:
            arr[k] = steps - 1
        else:
            arr[k] = int((arr[k] - minvalue) // step_size)
    return arr


numerics = ['int16', 'int32', 'int64'] # types of integers
dataset_numeric = dataset.select_dtypes(include=numerics) # selects integer type columns
numeric_columns = dataset_numeric.columns.to_numpy()

whole_columns = dataset.columns.to_numpy()

numeric_location = [] # for saving numeric columns index

for i in range(len(numeric_columns)):
    for j in range(len(whole_columns)):
        if numeric_columns[i] == whole_columns[j]:
            numeric_location.append(j)

for i in range(len(numeric_location)):
    dataset_array[:, numeric_location[i]] = discretize(dataset_array[:, numeric_location[i]], 3)

training1 = dataset_array[row // 5:]
training1 = pd.DataFrame(training1, columns=list(dataset.keys()))
training2 = np.concatenate((dataset_array[:row // 5], dataset_array[2 * row // 5:]))
training2 = pd.DataFrame(training2, columns=list(dataset.keys()))
training3 = np.concatenate((dataset_array[:2 * row // 5], dataset_array[3 * row // 5:]))
training3 = pd.DataFrame(training3, columns=list(dataset.keys()))
training4 = np.concatenate((dataset_array[:3 * row // 5], dataset_array[4 * row // 5:]))
training4 = pd.DataFrame(training4, columns=list(dataset.keys()))
training5 = dataset_array[:4 * row // 5]
training5 = pd.DataFrame(training5, columns=list(dataset.keys()))
test1 = dataset_array[:row // 5]
test1 = pd.DataFrame(test1, columns=list(dataset.keys()))
test2 = dataset_array[row // 5:2 * row // 5]
test2 = pd.DataFrame(test2, columns=list(dataset.keys()))
test3 = dataset_array[2 * row // 5:3 * row // 5]
test3 = pd.DataFrame(test3, columns=list(dataset.keys()))
test4 = dataset_array[3 * row // 5:4 * row // 5]
test4 = pd.DataFrame(test4, columns=list(dataset.keys()))
test5 = dataset_array[4 * row // 5:]
test5 = pd.DataFrame(test5, columns=list(dataset.keys()))


def entropy_calculator(filtered_data):
    entropy = 0
    class_count = filtered_data.shape[0]
    for c in ['Yes', 'No']:
        entropy_class = 0
        filtered_class_count = filtered_data[filtered_data['Attrition'] == c].shape[0]  # row count of Yes and NO
        if filtered_class_count != 0:
            probability_class = filtered_class_count / class_count  # probability of the class
            entropy_class = - probability_class * np.log2(probability_class)  # entropy
        entropy += entropy_class
    return entropy


def total_entropy_calculator(train_data):
    total_entropy = 0
    total_row = train_data.shape[0]  # the total size of the dataset
    for c in ['Yes', 'No']:
        total_class_count = train_data[train_data['Attrition'] == c].shape[0]  # number of the class
        total_class_entropy = - (total_class_count / total_row) * np.log2(
            total_class_count / total_row)  # entropy of the class
        total_entropy += total_class_entropy  # adding the class entropy to the total entropy of the dataset
    return total_entropy


def gain_calculator(feature_name, train_data):
    feature = 0.0
    feature_value_list = train_data[feature_name].unique()  # unique values of the feature
    feature_row = train_data.shape[0]
    for feature_value in feature_value_list:
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # filtering rows with that feature_value
        feature_value_count = feature_value_data.shape[0]
        feature_value_entropy = entropy_calculator(feature_value_data)  # calculates entropy for the feature value
        feature_value_probability = feature_value_count / feature_row
        feature += feature_value_probability * feature_value_entropy  # calculates information of the feature value
    return total_entropy_calculator(train_data) - feature  # calculates information gain by subtracting

def find_most_effective_feature(train_data):
    max_gain = -1
    feature_list = train_data.columns.drop('Attrition') # finding the feature names in the dataset
    # Attrition is not a feature, so dropping it
    max_feature = None
    for feature in feature_list:  # for each feature in the dataset
        feature_gain = gain_calculator(feature, train_data)
        if max_gain < feature_gain:  # selecting feature name with the highest information gain
            max_gain = feature_gain
            max_feature = feature

    return max_feature


def generate_sub_tree(feature_name, train_data):
    feature_value_count_dict = train_data[feature_name].value_counts(
        sort=False)  # dictionary of the count of unique feature value
    tree = {}  # sub tree or node

    for feature_value, count in feature_value_count_dict.items():
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # dataset with only feature_name = feature_value

        assigned_to_node = False  # flag for tracking feature_value is pure class or not
        for c in ['Yes', 'No']:
            class_count = feature_value_data[feature_value_data['Attrition'] == c].shape[0]  # count of class Yes or No
            if class_count == count:  # count of (feature_value = count) of class (pure class)
                tree[feature_value] = c  # adding node to the tree
                train_data = train_data[train_data[feature_name] != feature_value]  # removing rows with feature_value
                assigned_to_node = True
        if not assigned_to_node:  # not pure class
            tree[feature_value] = "?"  # as feature_value is not a pure class, it should be expanded further,
            # so the branch is marking with ?

    return tree, train_data


def make_tree(root, prev_feature_value, train_data):
    if train_data.shape[0] != 0:  # if dataset becomes empty after updating
        max_feature = find_most_effective_feature(train_data)  # most effective feature
        tree, train_data = generate_sub_tree(max_feature, train_data)  # getting tree node and updated dataset

        if prev_feature_value is not None:  # add to mediate node of the tree
            root[prev_feature_value] = dict()
            root[prev_feature_value][max_feature] = tree
            next_root = root[prev_feature_value][max_feature]
        else:  # add to root of the tree
            root[max_feature] = tree
            next_root = root[max_feature]

        for node, branch in list(next_root.items()): # iterate the tree node
            if branch == "?":  # if it is expandable
                feature_value_data = train_data[train_data[max_feature] == node]  # using the updated dataset
                make_tree(next_root, node, feature_value_data)  # recursive call with updated dataset


def id3(train_data):
    tree = {}  # tree which will be updated
    make_tree(tree, None, train_data)  # start calling recursion
    return tree


def predict(tree, sample):
    if not isinstance(tree, dict):  # if it is leaf node
        return tree  # return the value
    else:
        root_node = next(iter(tree))  # getting first key/feature name of the dictionary
        feature_value = sample[root_node]  # value of the feature
        if feature_value in tree[root_node]:  # checking the feature value in current tree node
            return predict(tree[root_node][feature_value], sample)  # goto next feature
        else:
            return None


def metrics_calculator(tree, test_data):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for index, test_row in test_data.iterrows():  # for each row in the dataset
        result = predict(tree, test_data.iloc[index])  # predict the row
        if result == test_data['Attrition'].iloc[index]:  # predicted value and expected value is same or not
            if result == 'Yes':
                TP += 1
            else:
                TN += 1
        else:
            print(test_data.iloc[index])
            if result == 'Yes':
                FP += 1
            else:
                FN += 1

    accuracy = (TP + TN) / (TP+TN+FP+FN)  # calculating accuracy
    precision = TP / (TP+FP)
    recall = TP / (TP+FN)
    F1Score = (2*recall*precision) / (recall+precision)
    return accuracy, precision , recall, F1Score


tree1 = id3(training1)
metrics1 = metrics_calculator(tree1, test1)  # evaluating the test dataset
tree2 = id3(training2)
metrics2 = metrics_calculator(tree2, test2)
tree3 = id3(training3)
metrics3 = metrics_calculator(tree3, test3)
tree4 = id3(training4)
metrics4 = metrics_calculator(tree4, test4)
tree5 = id3(training5)
metrics5 = metrics_calculator(tree5, test5)
# print(metrics1, metrics2, metrics3, metrics4, metrics5)
metricsavg = []
for i in range(len(metrics1)):
    metricsavg.append((metrics1[i]+metrics2[i]+metrics3[i]+metrics4[i]+metrics5[i])/5)
# print(metricsavg)
pprint.pprint(tree1)
