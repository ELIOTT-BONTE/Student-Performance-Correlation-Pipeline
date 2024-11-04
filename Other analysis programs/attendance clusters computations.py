import scipy.stats as stats

# Define the columns to be used in the chi-square tests
columns_to_test = [
    "Type of sessions", "Factual complexity", "Main teaching method",
    "Course frequency (per week)", "Number of instructors", "Assessment method",
    "Interaction level (out of 5)", "Experience (years)", 
    "Ideas expression encouragement", "Overall effective teaching", "Start time"
]

# Dictionary to store the results
chi_square_results = {
    "Characteristic": [],
    "X^2": [],
    "df": [],
    "P-Value": [],
    "Significant": []
}

# Function to determine if the result is significant
def is_significant(p_value, alpha=0.05):
    return "Yes" if p_value < alpha else "No"

# Perform chi-square tests for each characteristic
for column in columns_to_test:
    # Create contingency table
    contingency_table = pd.crosstab(data["Attendance cluster"], data[column])
    
    # Perform chi-square test
    chi2, p, dof, _ = stats.chi2_contingency(contingency_table)
    
    # Append results
    chi_square_results["Characteristic"].append(column)
    chi_square_results["X^2"].append(chi2)
    chi_square_results["df"].append(dof)
    chi_square_results["P-Value"].append(p)
    chi_square_results["Significant"].append(is_significant(p))

# Create a DataFrame to display the results
chi_square_results_df = pd.DataFrame(chi_square_results)

import ace_tools as tools; tools.display_dataframe_to_user(name="Chi-Square Test Results", dataframe=chi_square_results_df)

chi_square_results_df
