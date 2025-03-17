import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go


def get_float64_column_names(df: pd.DataFrame) -> list[str]:
    """Get the float64 column names from a DataFrame.

    Args:
        df: DataFrame to extract float64 columns from.

    Returns:
        List of strings with the float64 column names.
    """
    return  df.select_dtypes(include=["float64"]).columns.tolist()

def get_missing_value_indices(df: pd.DataFrame, column: str) -> list[int]:
    """Get the row indices of missing values within a column.

    Args:
        df: DataFrame with missing values.
        column: Column with missing values.

    Returns:
        Indices of missing values, as a list of ints.
    """
    missing = df[column].isna()
    return df[missing].index.tolist()

def fill_float64_cols_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Fill float64 columns with the mean of the column.

    Args:
        df: DataFrame with missing values and float64 type columns.

    Returns:
        DataFrame with missing values filled with the mean of the column.
    """
    float_columns = get_float64_column_names(df)
    for column in float_columns:
        
        # Get indices of missing values.
        missing_indices = get_missing_value_indices(df, column)

        # Get the mean of the column.
        if column == 'Condition':
            mean_values = [0] * len(missing_indices)
        else:
            mean = df[column].mean(skipna=True)
            mean_values = [mean] * len(missing_indices)

        # Fill missing values with the mean.
        df.loc[missing_indices, column] = mean_values

    return df

def regression_plot(feature, target):
    """Plot a feature of the data against another.

    Args:
        str: feature - Feature of the data to plot.
        str: target - Target of the data to plot aginst.

    Returns:
        None - Displays the plot.
    """
    # Regression Analysis
    X = np.array(df_filled[feature]).reshape(-1, 1)
    y = np.array(df_filled[target])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

    # Training model
    regr = LinearRegression()
    regr.fit(X_train, y_train)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x= X_test.flatten(), y=y_test, mode='markers', name='Actual Data'))

    # Plot regression line
    X_line = np.linspace(X.min(), X.max(), 100).reshape(-1,1)
    y_line = regr.predict(X_line)
    fig.add_trace(go.Scatter(x=X_line.flatten(), y=y_line.flatten(), mode='lines', name='Regression Line'))

    fig.update_layout(title=f"Regression Plot {feature} vs. {target}", template = 'plotly_white', xaxis_title="Space", yaxis_title=target)
    fig.show()


# Analysis of Housing Data


df = pd.read_csv('realest.csv')

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors= 'coerce')

df_filled = fill_float64_cols_with_mean(df)

features = ['Space', 'Room', 'Bedroom']

# Statistic Analysis
fig = px.scatter_matrix(df_filled, dimensions=features, color="Price")
fig.update_layout(title="Housing Data", template = "plotly_white", width=1200, height=1200)
fig.show()

for feature in features:
    regression_plot(feature, 'Price')