# Filter out the rows with "inconclusive" correlation cluster
filtered_data = data[data["Correlation cluster"] != "Inconclusive"]

# Dictionary to store the filtered results
chi_square_filtered_results_correlation = {
    "Characteristic": [],
    "X^2": [],
    "df": [],
    "P-Value": [],
    "Significant": []
}

# Perform chi-square tests for each characteristic related to correlation clusters in filtered data
for column in columns_to_test_correlation:
    # Create contingency table
    contingency_table = pd.crosstab(filtered_data["Correlation cluster"], filtered_data[column])
    
    # Perform chi-square test
    chi2, p, dof, _ = stats.chi2_contingency(contingency_table)
    
    # Append results
    chi_square_filtered_results_correlation["Characteristic"].append(column)
    chi_square_filtered_results_correlation["X^2"].append(chi2)
    chi_square_filtered_results_correlation["df"].append(dof)
    chi_square_filtered_results_correlation["P-Value"].append(p)
    chi_square_filtered_results_correlation["Significant"].append(is_significant(p))

# Create a DataFrame to display the filtered results
chi_square_filtered_results_correlation_df = pd.DataFrame(chi_square_filtered_results_correlation)

tools.display_dataframe_to_user(name="Chi-Square Test Results for Correlation Clusters (Filtered)", dataframe=chi_square_filtered_results_correlation_df)

chi_square_filtered_results_correlation_df

