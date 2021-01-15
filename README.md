# Naive_Bayes

## Description
The problem statement was to implement a Naive Bayes Classifier to classify two datasets called SpectHeart dataset and Mushroom dataset. The code uses the SpectHeart_train.csv and Mushroom_train.csv to train the model and uses SpectHeart_test.csv and Mushroom_test.csv to predict the classes and test for the accuracy. The model is built for a binary classifier, that is, the model classifies the instances to either 0 or 1. However, the attributes in the model can have n values. The accuracies of the model for both the datasets is given below:  
1. SpectHeart dataset = 79.62%  
2. Mushroom dataset = 99.73%  

The results are written into a file called RFile.txt and the probabilities of each attribute is given in the MFile.txt.

## Execution
The code has to be executed from the terminal using the following command:  
	`python NaiveBayes.py <train_filename> <test_filename> <model_filename> <results_filename>`
  
## Data
The data is present in the data folder. It has two train files and two test files which are in the csv format. The files must be in the same folder as the executing python file for successful execution.
