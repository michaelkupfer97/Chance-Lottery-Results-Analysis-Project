# Lotto Trend Analysis Project

This project analyzes the trends in Lotto results (Israeli Lotto) by performing various checks and calculations, and generates an Excel report. The program reads a CSV file containing Lotto data, performs statistical analysis, and outputs insights into common patterns, correlations, and trends in the results.

## Features
- Reads Lotto results data from a CSV file (`Chance.csv`).
- Analyzes patterns, such as expected card pairs, common sequences, and correlations between different suits.
- Performs basic statistical analysis (mean, median, standard deviation) on numeric columns.
- Calculates the most frequent sequences of Lotto results.
- Generates a detailed Excel report containing all the analysis results.

## How to Use

### 1. Prepare Your Data
The program expects a CSV file (`Chance.csv`) with 4 columns, representing the four suits in the Lotto game:
- **תלתן (Clubs)**
- **יהלום (Diamonds)**
- **לב (Hearts)**
- **עלה (Spades)**

Each row represents a drawn set of cards, with each column containing the value of the corresponding suit for that draw.

Example:
    A,A,10,10 
    J,K,9,8
    Q,J,A,9 
    7,8,8,7 
    Q,7,A,10


### 2. Running the Program
- Place the `Chance.csv` file in the same directory as the script.
- Run the script in your Python environment.

### 3. Output
The program will generate an Excel file (`Analysis_Report.xlsx`) containing the following sheets:
- **Basic Statistics**: Descriptive statistics for each suit, including mean, median, standard deviation, and most common values.
- **Correlations**: Chi-square test results for correlations between different suits.
- **Frequent Sequences (Top 10)**: The top 10 most common sequences of 3 consecutive results for each suit.
- **Sequence Frequencies**: The frequency of each sequence of 3 cards in each suit.
- **Fourth Card Analysis**: Analysis of patterns related to the fourth card in the sequence.

### 4. Additional Features
- **Card Pairing**: The program checks for expected card pairs based on predefined rules. For example, if the first two cards in a sequence are `7` and `J`, the third card is expected to be `Q` (the complementary card).
- **Pattern Matching**: The program tracks how often the expected card matches the actual card in the sequence and calculates the percentage of matches.

## Code Overview

### Key Functions:
1. **get_expected_card(trio)**: Returns the expected third card based on the first two cards in a trio, according to predefined pairings.
2. **analyze_card_patterns(df)**: Analyzes card patterns across the suits, checking for expected next cards and calculating the match percentage.
3. **basic_statistics(df)**: Calculates basic statistics (mean, median, standard deviation, most common) for each suit.
4. **calculate_correlations(df)**: Computes Chi-square test results for correlations between suits.
5. **frequent_sequences(df, window_size=3)**: Identifies the most frequent sequences of 3 consecutive cards in each suit.
6. **analyze_fourth_card_patterns(df)**: Analyzes patterns related to the fourth card in a sequence.
7. **create_summary_report(df)**: Generates the final Excel report with all the analysis results.

## Requirements
- Python 3.x
- Libraries: `pandas`, `scipy`, `xlsxwriter`

To install the required libraries, run:
```bash
pip install pandas scipy xlsxwriter

