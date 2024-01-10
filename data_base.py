from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import norm

HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

# Data Importation and Cleaning
roster = pd.read_csv(
    DATA_FOLDER / "roster.csv",
    converters={'NetID': str.lower, 'Email Address': str.lower},
    index_col='NetID'
)

hw_exam_grades = pd.read_csv(
    DATA_FOLDER / "hw_exam_grades.csv",
    index_col="SID",
    usecols=lambda col: 'Submission' not in col
)

quiz_files = DATA_FOLDER.glob('quiz_*_grades.csv')
quiz_grades = pd.DataFrame()

for quiz_file in quiz_files:
    quiz_data = pd.read_csv(quiz_file)
    quiz_name = quiz_file.stem.replace('quiz_', '').replace('_grades', '')
    quiz_data.set_index('Email', inplace=True)
    quiz_grades[f'Quiz {quiz_name}'] = quiz_data['Grade']
# Data Merging: Roster and Homework
final_data = pd.merge(
    roster,
    hw_exam_grades,
    how='left',
    left_index=True,
    right_index=True
)

# Data Merging: Final data and quiz grades
final_data = pd.merge(
    final_data,
    quiz_grades,
    how='left',
    left_on='Email Address',
    right_index=True
)

final_data = final_data.fillna(0)

n_exams = 3

# For each exam, calculate the score as a proportion of the maximum points possible.
for n in range(1, n_exams + 1):
    # Filter exam scores and corresponding max points using regex
    exam_scores_col = f'Exam {n}'
    exam_max_points_col = f'Exam {n} - Max Points'
    # Your code here to calculate the score as a proportion of the maximum points
    final_data[exam_scores_col] = final_data[exam_scores_col] / final_data[exam_max_points_col]
# Calculating Exam Scores:
# Filter exam scores and corresponding max points
exam_scores = final_data.filter(like='Exam')
exam_max_points = final_data.filter(like='Exam - Max Points')


sum_of_hw_scores = final_data.filter(regex=r'^Homework \d+$').sum(axis=1)
sum_of_hw_max = final_data.filter(regex=r'^Homework \d+ - Max Points$').sum(axis=1)
final_data["Total Homework"] = sum_of_hw_scores / sum_of_hw_max

# Calculating Average Homework Scores
hw_max_renamed = final_data.filter(regex=r'^Homework \d+ - Max Points$').rename(columns=lambda x: x.replace(' - Max Points', ''))
average_hw_scores = final_data.filter(regex=r'^Homework \d+$') / hw_max_renamed
final_data["Average Homework"] = average_hw_scores.mean(axis=1)

# Display the resulting DataFrame
final_data["Homework Score"] = final_data[['Total Homework', 'Average Homework']].max(axis=1)




quiz_scores = final_data.filter(regex='^Quiz \d+')

# Step i: Define a series with the maximum points for each quiz
quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)

sum_of_quiz_scores = quiz_scores.sum(axis=1)
sum_of_quiz_max = quiz_max_points.sum()
final_data["Total Quizzes"] = sum_of_quiz_scores / sum_of_quiz_max

# Calculate average quiz scores
average_quiz_scores = quiz_scores.div(quiz_max_points).mean(axis=1)
final_data["Average Quizzes"] = average_quiz_scores

final_data["Quiz Score"] = final_data[["Total Quizzes", "Average Quizzes"]].max(axis=1)

weightings = pd.Series({
  "Exam 1 Score": 0.05,
  "Exam 2 Score": 0.1,
  "Exam 3 Score": 0.15,
  "Quiz Score": 0.30,
  "Homework Score": 0.4,
})

# Calculate the final score
final_data["Final Score"] = (
  final_data["Exam 1"] * weightings["Exam 1 Score"] +
  final_data["Exam 2"] * weightings["Exam 2 Score"] +
  final_data["Exam 3"] * weightings["Exam 3 Score"] +
  final_data["Quiz Score"] * weightings["Quiz Score"] +
  final_data["Homework Score"] * weightings["Homework Score"]
)

# Round up the final score to the nearest whole number
final_data["Ceiling Score"] = np.ceil(final_data["Final Score"] * 100)


grades = {
  90: "A",
  80: "B",
  70: "C",
  60: "D",
  0: "F",
}

def grade_mapping(value):
  for threshold, grade in grades.items():
      if value >= threshold:
          return grade

letter_grades = final_data["Ceiling Score"].apply(grade_mapping)
final_data["Final Grade"] = pd.Categorical(letter_grades, categories=grades.values(), ordered=True)

for section, table in final_data.groupby("Section"):
  table = table.sort_values(by=["Last Name", "First Name"])
  num_students = len(table)
  print(f"Section {section} has {num_students} students.")
  file_path = f"section_{section}_data.csv"
  table.to_csv(file_path, index=False)
  print(f"Data saved to: {file_path}\n")



grade_counts = final_data["Final Grade"].value_counts()

# Plotting Bar Plot for Grade Distribution
grade_counts.plot(kind="bar", color="skyblue")
plt.title("Grade Distribution")
plt.xlabel("Letter Grade")
plt.ylabel("Count")
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(final_data["Final Score"], bins=20, color="skyblue", density=True, alpha=0.7, label="Histogram")
plt.title("Final Score Distribution")
plt.xlabel("Final Score")
plt.ylabel("Density")

final_mean = final_data["Final Score"].mean()
final_std = final_data["Final Score"].std()

xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, final_mean, final_std)
plt.plot(x, p, 'k', linewidth=2, label="Normal Distribution")

# Adding Kernel Density Estimate
final_data["Final Score"].plot.density(linewidth=4, label="Kernel Density Estimate")

plt.legend()
plt.show()