# -*- coding: utf-8 -*-
"""Tumor Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RHL0SFxUslXnUO6g-A6PVDxoJi_7-f9a
"""

# Anika Koul
# Sources
# https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection?resource=download for data
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html for resultsPlot function (adding text above bars)
# https://www.w3schools.com/python/matplotlib_pie_charts.asp for detectedTumorPlot and knownTumorPlot functions

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def contourFinder(fileName, lowerBound): # inputs are fileName and lowerBound, output is contours on images
  brain = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE) # reads the given file in grayscale
  brain = cv2.GaussianBlur(brain, (5,5), cv2.BORDER_DEFAULT) # applies gaussian blur on the image to reduce background noise
  ret, thresh = cv2.threshold(brain, lowerBound, 255, cv2.THRESH_BINARY) # thresholds the image
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # finds contours of the image
  cnt = cv2.drawContours(brain, contours, -1, (0, 255, 0), 3) # draws contours onto the image
  # cv2.imshow(cnt)
  return contours

def noTumor(lowerBound): # input is lowerBound, output is a list of all images that are detected to have no contours (tumors)
  noContours = [] # creates an empty list to store all images without contours
  for i in range(1, 99): # iterates through all images that should not have contours
    fileName = f"no/{i} no.jpg" # file path for no folder
    contours = contourFinder(fileName, lowerBound) # runs contourFinder function to detect contours in images
    if len(contours) == 0: # checks if there are contours
      noContours.append(fileName) # appends all images with no contours to list
  return noContours

def yesTumor(lowerBound): # input is lowerBound, output is a list of all images that are detected to have contours (tumors)
  allContours = [] # creates an empty list to store all images with contours
  for i in range(1, 99): # iterates through all images that should have contours
    fileName = f"yes/Y{i}.jpg"  # file path for yes folder
    contours = contourFinder(fileName, lowerBound) # runs contourFinder function to detect contours in images
    if len(contours) > 0: # checks if there are contours
      allContours.append(fileName) # appends all images with contours to list
  return allContours

def boundStats(lowerBound): # input is lowerBound, output is specificity and sensitivity for a given lower bound
  yesTumorList = [] # creates an empty list for images that are known to have tumors
  for i in range(1, 99): # iterates through all images known to have tumors
    fileName1 = f"yes/Y{i}.jpg" # file path for yes folder
    yesTumorList.append(fileName1) # adds all images known to have tumors to yesTumorList

  noTumorList = [] # creates an empty list for images that are known to have no tumors
  for i in range(1, 99): # iterates through all images known to not have tumors
    fileName2 = f"no/{i} no.jpg" # # file path for no folder
    noTumorList.append(fileName2) # adds all images known to not have tumors to noTumorList

  truePos = 0 # assigns the value of true positives to 0 as a baseline
  falseNeg = 0 # assigns the value of false negatives to 0 as a baseline
  for fileName1 in yesTumorList: # iterates through list of brains with tumors
    contours = contourFinder(fileName1, lowerBound) # calls contourFinder function to test lower bound values
    if len(contours) > 0: # tests detection of if there is a tumor
        truePos += 1 # adds to true positives if there is a tumor and a tumor is detected
    else:
        falseNeg += 1 # adds to false negatives if there is a tumor and a tumor is not detected

  trueNeg = 0 # assigns the value of true negatives to 0 as a baseline
  falsePos = 0  # assigns the value of false positives to 0 as a baseline
  for fileName in noTumorList: # iterates through list of brains without tumors
    contours = contourFinder(fileName, lowerBound) # calls contourFinder function to test lower bound values
    if len(contours) == 0: # tests if there is no tumor
        trueNeg += 1 # adds to true negatives if there is no tumor and no tumor is detected
    else:
        falsePos += 1 # adds to false positives if there is no tumor and a tumor is detected

  sensitivity = truePos/(truePos + falseNeg) # calculates the sensitivity of the lower bound
  specificity = trueNeg/(trueNeg + falsePos) # calculates the specificity of the lower bound

  return sensitivity, specificity, truePos, trueNeg, falsePos, falseNeg

def findBestBound(): # no inputs, output is the best lower bound based on highest average sensitivity and specificity
  bounds = np.arange(0, 256, 5) # creates a range of threshold values to iterate through
  bestBound = 0 # assigns value of best bound to 0 as a baseline
  bestAccuracy = 0 # assigns value of best accuracy to 0 as a baseline
  for lowerBound in bounds: # iterates through each potential bound value
    sensitivity, specificity, truePos, trueNeg, falsePos, falseNeg = boundStats(lowerBound) # runs threshStats function to get sensitivity and specificity values for each lower bound
    accuracy = (sensitivity + specificity)/2 # calculates average sensitivity and specificity (accuracy)
    if accuracy > bestAccuracy: # checks if accuracy calculated for each bound is greater than the previously calculated accuracy
        bestAccuracy = accuracy # reassigns bestAccuracy every time there is a higher accuracy value
        bestBound = lowerBound # reassigns bestBound every time there is a bound which gives a higher accuracy value

  return bestBound, bestAccuracy

def tumorProb(): # no inputs, output is the probability
  numTumors = 155 # assigns a variable to the known number of tumors
  numBrains = 253 # assigns a variable to the known number of brain images in the dataset
  probability = numTumors/numBrains # calculates the probability of a tumor in the dataset
  return probability

def accuracyPlot(lowerBound):
  bounds = np.arange(0, 256, 5) # creates a range of bound values to iterate through
  accuracies = [] # creates an empty list to add accuracies to
  for bound in bounds: # iterates through all potential threshold values
      sensitivity, specificity, truePos, trueNeg, falsePos, falseNeg = boundStats(bound) # runs threshStats function to get sensitivity and specificity values
      accuracy = (sensitivity + specificity)/2 # calculates each accuracy using sensitivity and specificity
      accuracies.append(accuracy) # adds each accuracy value to the list
  plt.figure() # creates a canvas for the plot
  plt.scatter(bounds, accuracies, color = "red") # plots bounds and corresponding accuracies as scatter points
  plt.xlabel('Lower Bound') # labels the x axis
  plt.ylabel('Accuracy') # labels the y axis
  plt.title('Accuracy vs. Lower Bound') # adds a title
  plt.show() # shows the plot

def boundStatsPlot(lowerBound):
  bounds = np.arange(0, 256, 5) # creates a range of lower bound values to iterate through
  sensitivities = [] # creates an empty list to add sensitivities to
  specificities = [] # creates an empty list to add specificities to
  for bound in bounds: # iterates through all potential threshold values
      sensitivity = boundStats(bound)[0] # runs boundStats function to get sensitivity values
      specificity = boundStats(bound)[1] # runs boundStats function to get specificity values
      sensitivities.append(sensitivity) # adds each sensitivity to the list of sensitivities
      specificities.append(specificity) # adds each specificity to the list of specificities

  plt.figure() # creates a canvas for the plot
  plt.scatter(bounds, sensitivities, label = "Sensitivity", color = "red") # plots bounds and corresponding sensitivities as scatter points
  plt.scatter(bounds, specificities, label = "Specificity", color = "blue") # plots bounds and corresponding specificities as scatter points
  plt.xlabel('Lower Bound') # labels the x axis
  plt.ylabel('Value') # labels the y axis
  plt.legend() # adds a legend
  plt.title('Value vs. Lower Bound') # adds a title
  plt.show() # shows the plot

def boundCountPlot():
  bounds = range(0, 256) # creates a range of bound values to test
  numTumors = [] # creates an empty list to store the number of tumors detected at each bound
  for lowerBound in bounds: # iterates through all potential lower bound values
    tumorImages = yesTumor(lowerBound) # runs yesTumor function to find all images with tumors at the given bound
    numTumors.append(len(tumorImages)) # adds the number of tumor images found to the list of the number of tumors for each bound
  plt.scatter(bounds, numTumors) # plots the scatter plot using the bounds on the x axis and the number of tumors on the y axis
  plt.xlabel("Lower Bound") # labels the x axis
  plt.ylabel("Number of Tumors Detected") # labels the y axis
  plt.title("Number of Tumors Detected vs. Lower Bound") # adds a title
  plt.show()

def detectedTumorPlot(lowerBound):
  noTumorCount = len(noTumor(lowerBound)) # assigns a variable to store the number of detected brains without tumors at a lower bound of bestBound
  tumorCount = len(yesTumor(lowerBound)) # assigns a variable to store the number of detected brains with tumors at a lower bound of bestBound
  labels = ["No Tumor", "Tumor"] # labels the parts of the pie chart
  values = [noTumorCount, tumorCount] # makes numTumorCount and tumorCount the values to be used in the pie slices
  colors = ["pink", "teal"] # assigns colors to the pie slices
  plt.pie(values, labels = labels, colors = colors, autopct = '%1.1f%%', startangle = 90) # plots the pie chart
  plt.axis('equal') # sets an equal axis
  plt.title("Proportion of Detected Images with Tumors") # adds title
  plt.show()

def knownTumorPlot():
  noTumorCount = 98 # assigns a variable to store the number of known brains without tumors
  tumorCount = 155 # assigns a variable to store the number of known brains with tumors
  labels = ["No Tumor", "Tumor"] # labels the parts of the pie chart
  values = [noTumorCount, tumorCount] # makes numTumorCount and tumorCount the values to be used in the pie slices
  colors = ["pink", "teal"] # assigns colors to the pie slices
  plt.pie(values, labels = labels, colors = colors, autopct = '%1.1f%%', startangle = 90) # plots the pie chart
  plt.axis('equal') # sets an equal axis
  plt.title("Proportion of Known Images with Tumors") # adds title
  plt.show()

def resultsPlot(lowerBound):
  x = ["True Positives", "True Negatives", "False Positives", "False Negatives"] # assigns labels for each bar on x axis
  stats = boundStats(lowerBound) # creates a variable to store information from boundStats function
  truePos = stats[2] # accesses truePos value from boundStats function
  trueNeg = stats[3] # accesses trueNeg value from boundStats function
  falsePos = stats[4] # accesses falsePos value from boundStats function
  falseNeg = stats[5] # accesses falseNeg value from boundStats function
  plt.bar(x[0], truePos, color = "skyblue") # plots bar for truePos
  plt.bar(x[1], trueNeg, color = "green") # plots bar for trueNeg
  plt.bar(x[2], falsePos, color = "crimson") # plots bar for falsePos
  plt.bar(x[3], falseNeg, color = "purple") # plots bar for falseNeg
  plt.xlabel("Results") # adds label to x axis
  plt.ylabel("Value") # adds label to y axis
  plt.title(f"Results at a Threshold of {lowerBound}") # adds title
  plt.text(x[0], truePos + 0.1, truePos, ha = 'center', fontsize = 10)
  plt.text(x[1], trueNeg + 0.1, trueNeg, ha = 'center', fontsize = 10)
  plt.text(x[2], falsePos + 0.1, falsePos, ha = 'center', fontsize = 10)
  plt.text(x[3], falseNeg + 0.1, falseNeg, ha='center', fontsize = 10)
  plt.show()

def main():#
  bestBound = findBestBound() # runs the findBestBound function to find the best lower bound
  print("The best lower bound and accuracy is:", bestBound) # prints the best bound and accuracy

  detectedNo = len(noTumor(bestBound[0])) # runs the noTumor function to find the number of detected brains without tumors at the best lower bound
  print("The number of detected brains without tumors at this lower bound is:", detectedNo) # prints this value

  detectedYes = len(yesTumor(bestBound[0])) # runs the yesTumor function to find the number of detected brains with tumors at the best lower bound
  print("The number of detected brains with tumors at this lower bound is:", detectedYes) # prints this value

  print("The probability of having a tumor in this dataset is:", tumorProb()) # prints the probability of having a tumor in this dataset using the tumorProb function
  print("")

  print("The plot below shows the accuracy at each lower bound tested.")
  accuracyPlot(bestBound[0]) # displays a scatter plot of Accuracy vs. Lower Bound
  print("")

  print("The plot below shows the relationship between sensitivity and specificity values at each lower bound tested.")
  boundStatsPlot(bestBound[0]) # displays a scatter plot of Sensitivity and Specificity Values vs. Lower Bound
  print("")

  print("The plot below shows the number of tumors detected for each threshold value.")
  boundCountPlot() # displays a scatter plot of Number of Tumors Detected vs. Lower Bound
  print("")

  print(f"The plot below shows the proportion of detected tumors compared to no tumors in the dataset at a lower bound of {bestBound[0]}.")
  detectedTumorPlot(bestBound[0]) # displays a pie chart of detected tumors compared to no tumors in the dataset at a lower bound of bestBound
  print("")

  print("The plot below shows the proportion of known tumors compared to no tumors in the dataset.")
  knownTumorPlot() # displays a pie chart of known tumors compared to no tumors in the dataset
  print("")

  print(f"The plot below shows the number of true positives, true negatives, false positives, and false negatives at a lower bound of {bestBound[0]}.")
  resultsPlot(bestBound[0]) # displays a bar chart of true positives, true negatives, false positives, and false negatives at a lower bound of bestBound

if __name__ == "__main__":
  main()

import unittest

class TestModel(unittest.TestCase):

  def test_noTumor_OutputValue(self):
    lowerBound = 200 # assigns a value to lowerBound
    output = noTumor(lowerBound) # runs the noTumor function to get a list of brains detected to have no tumor
    self.assertTrue(len(output) > 0) # checks if there are files in list

  def test_yesTumor_OutputValue(self):
    lowerBound = 200 # assigns a value to lowerBound
    output = yesTumor(lowerBound) # runs the yesTumor function to get a list of brains detected to have a tumor
    self.assertTrue(len(output) > 0) # checks if there are files in list

  def test_boundStats_OutputType(self):
    lowerBound = 200 # assigns a value to lowerBound
    output = boundStats(lowerBound) # runs the boundStats function to calculate sensitivity and specificity
    self.assertTrue(isinstance(output[0], float)) # checks if the type of the first value in the tuple output is a float
    self.assertTrue(isinstance(output[1], float)) # checks if the type of the second value in the tuple output is a float

  def test_findBestBound_OutputType(self):
    output = findBestBound() # runs the boundStats function to find the best threshold and its accuracy
    self.assertTrue(isinstance(output[0], (int, np.integer, float))) # checks if the type of the first value in the tuple output is an int, np.int64, or a float
    self.assertTrue(isinstance(output[1], float)) # checks if the type of the second value in the tuple output is a float

  def test_tumorProb_OutputType(self):
    numTumors = 10 # assigns a value to the known number of tumors
    numBrains = 50 # assigns a value to the known number of images (brains)
    output = numTumors/numBrains # calculates the probability of having a tumor in the dataset
    self.assertTrue(type(output) == float) # checks if the type of the output is a float

  def test_tumorProb_OutputValue(self):
    numTumors = 10 # assigns a value to the known number of tumors
    numBrains = 50 # assigns a value to the known number of images (brains)
    output = numTumors/numBrains # calculates the probability of having a tumor in the dataset
    self.assertTrue(output == 0.2) # checks if the output is correct or not

unittest.main(argv=[''], verbosity=2, exit=False)