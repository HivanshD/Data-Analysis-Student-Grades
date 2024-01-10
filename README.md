# Data-Analysis-Student-Grades

In this question, you need to calculate student grades by integrating data from multiple sources.
It uses Python's Pandas and NumPy libraries, as well as Matplotlib and SciPy for data
manipulation and visualization. The job is straightforward. You are welcome to use the internet
for help. You will find a lot of resources that will give you the template that you can use.
You are provided a script and you need to fill in the code for the given steps which performs the
following steps. Each step here contributes to the next step, so follow these in order.
You can follow the Steps detailed here, you need to provide a final script which accumulates all
the scripts from each step.
1. Importing Libraries and Setting Paths:
a. Import libraries like pandas, numpy, matplotlib.pyplot, and scipy.stats
b. Set the current directory
2. Data Importation and Cleaning:
a. Read the data to create 3 pandas dataframe
b. Roster Data: Reads roster.csv, converting the 'NetID' and 'Email Address' to
lowercase and using 'NetID' as the index.
c. Homework and Exam Grades: Loads hw_exam_grades.csv, again converting
'SID' to lowercase and ignoring columns containing 'Submission', setting 'SID' as
the index.
d. Quiz Grades: It a bit tricky, you need to create a dataframe, for quiz_grades,
Aggregates quiz grades from all the files named quiz_*_grades.csv, renaming the
'Grade' column to the quiz name and setting 'Email' as the index.
3. Data Merging:
a. Combines the roster with homework and exam grades using 'NetID'/'SID' as the
common index.
b. Further merges this data with quiz grades, matching 'Email Address' from the
roster to 'Email' in quiz grades.
c. final_data = final_data.fillna(0)
4. Data Processing and Score Calculation:
a. Calculating Exam Scores:
i. The number of exams is set to 3.
ii. For each exam, calculate the score as a proportion of the maximum
points possible. This is done by dividing the student's score for
each exam by the maximum points for that exam. Use regex to find
the homework score and homework max points.
b. Calculating Total and Average Homework Scores:
i. Identify the columns that represent homework scores and their
corresponding maximum points using regular expressions.
ii. Sums up all homework scores and their respective maximum
points for each student.
iii. Calculates the total homework score as the ratio of the sum of
homework scores to the sum of maximum points.
iv. Computes the average homework score by dividing each homework
score by its maximum points, summing these ratios, and then
dividing by the number of homework assignments.
c. Final Homework Score Calculation:
i. Determines the final homework score by taking the maximum
between the total homework score and the average homework
score.
d. Calculating Total and Average Quiz Scores:
i. Filters columns representing quiz scores.
ii. Defines a series with the maximum points for each quiz.
iii. Sums up all quiz scores and the total maximum points for quizzes.
iv. Calculates the total quiz score as the ratio of the sum of quiz
scores to the sum of maximum points.
v. Computes the average quiz score by dividing each quiz score by its
maximum points, summing these ratios, and then dividing by the
number of quizzes.
e. Final Quiz Score Calculation:
i. Determines the final quiz score by taking the maximum between
the total quiz score and the average quiz score.
f. Calculating the Final Score:
i. Defines weightings for each component (exams, quizzes, and
homework).
ii. Calculates the final score by multiplying each component score by
its respective weighting and summing these values.
b. Rounding Up the Final Score:
i. Rounds up the final score to the nearest whole number by
multiplying it by 100 and applying the ceiling function.
5. Grade Assignment and Visualization:
a. Defining Grade Mapping:
i. A dictionary grades maps numerical thresholds to letter grades
(e.g., 90 to 'A', 80 to 'B', etc.).
ii. The function grade_mapping takes a numerical value and maps it to
a letter grade based on these thresholds. It iterates through the
grades dictionary and returns the corresponding letter grade for the
first threshold that the value meets or exceeds.
b. Applying Grade Mapping to Data:
i. The grade_mapping function is applied to the "Ceiling Score"
column in the final_data DataFrame, creating a series of letter
grades.
ii. These letter grades are then added to final_data as a new column
"Final Grade". The grades are treated as categorical data, ordered
according to the order of grades in the grades dictionary.
c. Processing Data by Sections:
i. The dataset is grouped by the "Section" column.
ii. For each section, a CSV file is created containing the sorted data
(by last and first names). The script also prints the number of
students in each section and the file path where the data is saved.
d. Visualizing Grade Distribution:
i. A bar plot is generated showing the count of each letter grade in the
"Final Grade" column.
ii. A histogram and a kernel density estimate are plotted for the "Final
Score" column, showing the distribution of final scores.
e. Plotting Normal Distribution:
i. The mean (final_mean) and standard deviation (final_std) of the
"Final Score" column are calculated.
ii. A range of values (x) is generated around the mean, spanning 5
standard deviations on either side.
iii. A normal distribution curve is plotted over this range, using the
calculated mean and standard deviation.
iv. This curve is overlaid on the histogram and density plot to visualize
how closely the final scores follow a normal distribution
