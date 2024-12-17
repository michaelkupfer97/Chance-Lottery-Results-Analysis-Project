import os
import pandas as pd
from itertools import combinations
from scipy.stats import chi2_contingency

print(os.getcwd())

# מיפוי זוגות הקלפים בהתאמה
card_pairs = {
    '7': 'J', '8': 'Q', '9': 'K', '10': 'A',
    'J': '7', 'Q': '8', 'K': '9', 'A': '10'
}


# פונקציה שמחזירה את הקלף המשלים לפי החוקים
def get_expected_card(trio):
    # מוודאים ששני קלפים מתוך השלישייה הם בהתאמה לזוגות
    first_pair = card_pairs.get(trio[0])
    second_pair = card_pairs.get(trio[1])

    # אם יש שני קלפים עם התאמה ברורה, נחזיר את המשלים של השלישי
    if first_pair and second_pair:
        return card_pairs.get(trio[2])
    return None


# פונקציה לניתוח תבניות
def analyze_card_patterns(df):
    df.columns = ['תלתן', 'יהלום', 'לב', 'עלה']
    results = {}

    # עבור כל סדרה בודקים את הרצפים
    for suit in df.columns:
        total_patterns = 0
        matching_patterns = 0

        for i in range(len(df) - 3):  # נעצור ב-3 קלפים לפני הסוף
            trio = df[suit].iloc[i:i + 3].tolist()
            actual_next = df[suit].iloc[i + 3]

            # בודקים את הקלף הצפוי
            expected_next = get_expected_card(trio)

            if expected_next:
                total_patterns += 1
                if actual_next == expected_next:
                    matching_patterns += 1

        # מחשבים את האחוזים
        match_percentage = (matching_patterns / total_patterns * 100) if total_patterns > 0 else 0
        results[suit] = {
            'total_patterns': total_patterns,
            'matching_patterns': matching_patterns,
            'match_percentage': round(match_percentage, 2)
        }

    return results


# קריאה לקובץ CSV
df = pd.read_csv('Chance.csv', encoding='latin1')

# ביצוע הניתוח
results = analyze_card_patterns(df)

# הדפסת התוצאות
for suit, stats in results.items():
    print(f"\n--- ניתוח עבור {suit} ---")
    print(f"סך התבניות שנבדקו: {stats['total_patterns']}")
    print(f"מספר תבניות שהתאימו: {stats['matching_patterns']}")
    print(f"אחוז התאמה: {stats['match_percentage']}%\n")

# קריאת הנתונים
df = pd.read_csv('Chance.csv', encoding='latin1')

# הגדרת עמודות (בהתאם למבנה הקובץ שלך)
df.columns = ['תלתן', 'יהלום', 'לב', 'עלה']


# פונקציה לחישוב סטטיסטיקות בסיסיות
def basic_statistics(df):
    stats = {}

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # חישוב עבור עמודות נומריות
            stats[column] = {
                'Mean': df[column].mean(),
                'Median': df[column].median(),
                'Std Deviation': df[column].std(),
                'Most Common': df[column].mode()[0]  # חישוב המוד (ערך נפוץ)
            }
        else:
            # עבור עמודות טקסט (קלפים), נבצע חישובים אחרים, כמו ספירת תדירות
            stats[column] = {
                'Most Common': df[column].mode()[0],  # מציאת הערך הנפוץ ביותר בעמודה
                'Unique Values': df[column].nunique(),  # מספר הערכים הייחודיים
                'Value Counts': df[column].value_counts().to_dict()  # ספירת תדירות
            }

    return stats


# פונקציה לבדיקת קורלציות בין סדרות
def calculate_correlations(df):
    correlations = {}
    for col1, col2 in combinations(df.columns, 2):
        correlation = pd.crosstab(df[col1], df[col2])
        chi2, p, _, _ = chi2_contingency(correlation)
        correlations[f"{col1} & {col2}"] = {
            'Chi-Square': round(chi2, 2),
            'p-value': round(p, 4)
        }
    return correlations


# פונקציה לזיהוי רצפים נפוצים
def frequent_sequences(df, window_size=3):
    sequences = {}
    for col in df.columns:
        seq_counts = {}
        for i in range(len(df) - window_size):
            seq = tuple(df[col].iloc[i:i + window_size])
            seq_counts[seq] = seq_counts.get(seq, 0) + 1
        sequences[col] = sorted(seq_counts.items(), key=lambda x: -x[1])[:10]
    return sequences


# פונקציה לניתוח קשר בין קלף רביעי לשלישייה
def analyze_fourth_card_patterns(df):
    # מילון זוגות הקלפים
    pairs = {
        '7': 'J',
        '8': 'Q',
        '9': 'K',
        '10': 'A'
    }

    # משתנים להחזקת תוצאות
    matching_patterns = 0
    total_patterns = 0

    for i in range(len(df) - 3):  # חיפוש תבניות בחלונות של 4 קלפים
        trio = df.iloc[i:i + 3]  # שלושה קלפים רצופים
        next_card = df.iloc[i + 3]  # הקלף הרביעי

        # המרת הערכים של trio לערכים בודדים (ולא Series)
        trio_values = trio.values.tolist()  # המרת ל-list פשוט

        # המרת כל ערך לסטנדרט (כמו string) כדי לוודא שזה לא סדרה או אובייקט לא "נשמע"
        trio_values = [str(val) for val in trio_values]

        # בדוק אם כל אחד מהקלפים נמצא במילון pairs
        if trio_values[0] in pairs and trio_values[1] in pairs and trio_values[2] in pairs:
            if next_card == pairs[trio_values[2]]:  # בודק אם הקלף הבא מתאים
                matching_patterns += 1

        total_patterns += 1

    # חישוב אחוז התאמה
    match_percentage = (matching_patterns / total_patterns * 100) if total_patterns > 0 else 0
    return {
        'matching_patterns': matching_patterns,
        'total_patterns': total_patterns,
        'percentage': round(match_percentage, 2)
    }


# יצירת דו"ח מסכם
def create_summary_report(df):
    print("Analyzing file...")

    # ביצוע ניתוחים
    stats = basic_statistics(df)
    correlations = calculate_correlations(df)
    sequences = frequent_sequences(df)
    fourth_card_analysis = analyze_fourth_card_patterns(df)

    # אם fourth_card_analysis לא נמצא במבנה המתאים (מילון או רשימה של מילונים),
    # נהפוך אותו למילון עם תוצאות.
    # לדוגמה, ייתכן שצריך להכניס אותו לרשימה או למילון לפני הייצוא.
    fourth_card_analysis_data = [{
        'matching_patterns': fourth_card_analysis['matching_patterns'],
        'total_patterns': fourth_card_analysis['total_patterns'],
        'percentage': fourth_card_analysis['percentage']
    }]

    # יצוא ל-Excel
    with pd.ExcelWriter("Analysis_Report.xlsx", engine='xlsxwriter') as writer:
        # סטטיסטיקות בסיסיות
        pd.DataFrame(stats).to_excel(writer, sheet_name='Basic Statistics')

        # קורלציות
        pd.DataFrame(correlations).to_excel(writer, sheet_name='Correlations')

        # רצפים נפוצים
        seq_df = pd.DataFrame({col: [seq for seq, _ in sequences[col]] for col in sequences.keys()})
        freq_df = pd.DataFrame({col: [freq for _, freq in sequences[col]] for col in sequences.keys()})
        seq_df.to_excel(writer, sheet_name='Frequent Sequences (Top 10)')
        freq_df.to_excel(writer, sheet_name='Sequence Frequencies')

        # ניתוח קשר לקלף רביעי
        pd.DataFrame(fourth_card_analysis_data).to_excel(writer, sheet_name='Fourth Card Analysis')

    print("Analysis complete. Report saved as 'Analysis_Report.xlsx'.")


# הרצת הדו"ח
create_summary_report(df)
