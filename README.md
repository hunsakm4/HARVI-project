# HARVI-project
The HARVI Python program analyzes phishing susceptibility scores before and after training. It outputs average scores, percentage changes, participant improvements, paired t-test results, two comparison charts, and a CSV report for the Pilot, Technology, and Marketing groups.

# HARVI Automated Analysis Program

## Project Overview

The HARVI Automated Analysis Program uses Python to evaluate cybersecurity awareness training effectiveness by comparing phishing susceptibility scores before and after training.

The program analyzes participant data from the Pilot, Technology, and Marketing groups, performs statistical calculations, generates visualizations, and summarizes training outcomes.

**Important:** Lower HARVI scores indicate lower phishing susceptibility and better security outcomes.

## 1. Requirements

Before running the program, install:

- Python 3.10 or newer
- Visual Studio Code (VS Code), recommended
- Python extension for VS Code
- Required Python libraries: pandas, matplotlib, and scipy

## 2. Installing Python Libraries

Open the terminal in VS Code by selecting **Terminal → New Terminal**.

Run the following command:

```powershell
python -m pip install pandas matplotlib scipy
```

If `python` is not recognized on Windows, try:

```powershell
py -m pip install pandas matplotlib scipy
```

To verify installation:

```powershell
python -m pip show pandas matplotlib scipy
```

## 3. Preparing the Project

1. Create a folder named `HARVI_Project`.
2. Save the Python analysis script inside the folder.
3. Place the required HARVI CSV datasets in the same folder, unless the script specifies another location.
4. Open the project folder in VS Code.
5. Verify that the filenames in the Python script match the actual CSV filenames.

## 4. Running the Program

Open the VS Code terminal and navigate to the project directory.

Run:

```powershell
python HARVI_Project.py
```

Alternatively, use the **Run Python File** button in VS Code.

## 5. Program Outputs

The program analyzes each study group and produces:

| Output | Description |
|---|---|
| Average HARVI scores | Mean scores before and after training |
| Percentage change | Relative increase or decrease in susceptibility |
| Participant outcomes | Number of participants who improved, worsened, or remained unchanged |
| Paired-samples t-test | Statistical test of before-and-after score differences |
| Figure 1 | Bar chart comparing average HARVI scores |
| Figure 2 | Stacked bar chart showing participant outcome percentages |
| CSV summary | Exported statistical results for further analysis |

## 6. Interpreting Results

- **Decreased HARVI score:** Improvement in phishing susceptibility.
- **Increased HARVI score:** Worsening phishing susceptibility.
- **Unchanged HARVI score:** No measured difference.
- **p-value below .05:** Statistically significant before-and-after difference.
- **p-value of .05 or greater:** Insufficient evidence of a statistically significant difference.

Statistical significance does not necessarily establish that the training caused the observed change.

## 7. Troubleshooting

**ModuleNotFoundError**

Install the missing library using:

```powershell
python -m pip install library_name
```

**FileNotFoundError**

Verify that the CSV files are located in the correct directory and their filenames match those referenced in the script.

**Python is not recognized**

Verify that Python is installed and accessible through your system's PATH, or try the `py` command on Windows.

**Charts are not displaying**

Verify that Matplotlib is installed and that the Python script executes successfully.

## 8. Project Purpose

HARVI demonstrates how Python automation can simplify cybersecurity training assessments by reducing manual calculations, identifying measurable changes in phishing susceptibility, and providing visual and statistical evidence to support training evaluations.
