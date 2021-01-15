import csv
import sys


# Reads each line from the input file and writes it into a list.
def read_input(filename):
    data_set = csv.reader(open(filename))
    data_set = list(data_set)
    data_set = data_set[1:]
    return data_set


# Classifies each instance into either 0 class or 1 class based on the last column.
def get_class(data_set):
    separate = {}
    separate[0] = []
    separate[1] = []
    for i in data_set:
        if i[len(data_set[0]) - 1] == '0':
            separate[0].append(i)
        else:
            separate[1].append(i)
    return separate


# Returns the unique values of each attribute (column).
def get_features(instances):
    all_attr = []
    for i in range(len(instances[0])):
        attributes = []
        for j in range(len(instances)):
            attributes.append(instances[j][i])
        all_attr.append(attributes)
    features = []
    for i in range(len(all_attr)):
        list_features = set(all_attr[i])
        list_features = list(list_features)
        features.append(list_features)
    return features, all_attr


# Calculates the probability of each feature in each column for both classes 0 and 1.
def get_prob(data_set):
    separated_class = get_class(data_set)
    attribute_0 = separated_class[0]
    attribute_1 = separated_class[1]
    class_probabilities = {'0': [], '1': []}
    features_0, all_attr_0 = get_features(attribute_0)
    for i in range(0, len(attribute_0[0])):
        prob = {}
        for feature in features_0[i]:
            count_feature = all_attr_0[i].count(feature)
            prob_feature = count_feature/len(attribute_0)
            prob[feature] = prob_feature
        class_probabilities['0'].append(prob)

    features_1, all_attr_1 = get_features(attribute_1)
    for i in range(0, len(attribute_1[0])):
        prob = {}
        for feature in features_1[i]:
            count_feature = all_attr_1[i].count(feature)
            prob_feature = count_feature / len(attribute_1)
            prob[feature] = prob_feature
        class_probabilities['1'].append(prob)

    return class_probabilities


# Predicts the class of each instance of the test set using the probabilities obtained by examining train set.
def predict(test_set, class_probabilities):
    predictions = []
    for instance in test_set:
        instance = instance[:len(instance) - 1]
        prob_attr_0 = len(class_probabilities['0'])/(len(class_probabilities['0']) + len(class_probabilities['1']))
        prob_attr_1 = len(class_probabilities['1'])/(len(class_probabilities['0']) + len(class_probabilities['1']))
        features_test, all_attr = get_features(test_set)
        for i in range(len(instance)):
            if instance[i] in features_test[i]:
                try:
                    prob_attr_0 = prob_attr_0 * class_probabilities['0'][i][instance[i]]
                except KeyError:
                    prob_attr_0 = prob_attr_0 * 0
                try:
                    prob_attr_1 = prob_attr_1 * class_probabilities['1'][i][instance[i]]
                except KeyError:
                    prob_attr_1 = prob_attr_1 * 0
        if prob_attr_0 > prob_attr_1:
            predictions.append('0')
        else:
            predictions.append('1')
    return predictions


# Calculates the accuracy of the predictions that were obtained with the actual class values of the test set.
def get_accuracy(predictions, test_set):
    count = 0
    for i in range(0, len(predictions)):
        if predictions[i] == test_set[i][len(test_set[0])-1]:
            count = count + 1
    accuracy = count/len(predictions) * 100
    return accuracy


# Constructs the confusion matrix by comparing the predictions and the actual classes of the test set.
def construct_confusion_matrix(predictions, test_set):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(predictions)):
        if test_set[i][len(test_set[0])-1] == '1' and predictions[i] == '0':
            fn = fn + 1
        elif test_set[i][len(test_set[0])-1] == '0' and predictions[i] == '1':
            fp = fp + 1
        elif test_set[i][len(test_set[0])-1] == '0' and predictions[i] == '0':
            tn = tn + 1
        elif test_set[i][len(test_set[0]) - 1] == '1' and predictions[i] == '1':
            tp = tp + 1

    confusion_matrix = [[tp, fn],
                        [fp, tn]]
    return confusion_matrix


# Writes the data to the MFile.txt.
def write_m_file(class_probabilities, train_set):
    m_file.write("The probabilities are: \r")
    features = get_features(train_set)
    features = features[:-1]
    for i in range(len(class_probabilities['0']) - 1):
        m_file.write("Evidence: E%s \r" % (i+1))
        m_file.write("----------------------------------\r")
        for feature in features[0][i]:
            try:
                m_file.write("Probability(F%s" %(i + 1)+"=%s" % feature + " | C=0) = %s\r" % str(class_probabilities['0'][i][feature]))
            except KeyError:
                m_file.write("Probability(F%s" % (i + 1)+"=%s" % feature + " | C=0) = 0.0\r")
            try:
                m_file.write("Probability(F%s" %(i + 1)+"=%s" % feature + " | C=1) = %s\r" % str(class_probabilities['1'][i][feature]))
            except KeyError:
                m_file.write("Probability(F%s" % (i + 1)+"=%s" % feature + " | C=1) = 0.0\r")
        m_file.write("\r")


# Writes the data to the RFile.txt.
def write_r_file(predictions, test_set, confusion_matrix, accuracy):
    r_file.write("The results are: \r")
    r_file.write("Predicted value \t Actual value\r")
    for i in range(len(predictions)):
        r_file.write("\t\t%s \t\t\t\t\t" % predictions[i] + "%s\r" % test_set[i][len(test_set[0])-1])
    r_file.write("\r\r")
    r_file.write("Confusion matrix: \r\r")
    r_file.write("\t\t\tClass 0\t\t\tClass 1\r")
    r_file.write("Class 0\t\t%s\t\t\t\t" % confusion_matrix[0][0] + "%s\r" % confusion_matrix[0][1])
    r_file.write("Class 1\t\t%s\t\t\t\t" % confusion_matrix[1][0] + "%s\r" % confusion_matrix[1][1])
    r_file.write("\r\rAccuracy: %s" % accuracy + "%")


def main():
    train_set = read_input(sys.argv[1])
    test_set = read_input(sys.argv[2])
    class_probabilities = get_prob(train_set)
    predictions = predict(test_set, class_probabilities)
    accuracy = get_accuracy(predictions, test_set)
    confusion_matrix = construct_confusion_matrix(predictions, test_set)
    write_m_file(class_probabilities, train_set)
    write_r_file(predictions, test_set, confusion_matrix, accuracy)


if __name__ == "__main__":
    m_name = sys.argv[3]
    r_name = sys.argv[4]
    open(m_name, "w").close()
    open(r_name, "w").close()
    m_file = open(m_name, "a+")
    r_file = open(r_name, "a+")
    main()
