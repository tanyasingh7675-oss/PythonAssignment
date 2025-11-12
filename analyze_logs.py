import pandas as pd

# Step 1: Load and clean data
def load_and_clean(path):
    df = pd.read_csv(path)
    # Convert start column to datetime; invalid values become NaT (Not a Time)
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    # Convert duration to numbers; invalid becomes NaN
    df['duration_min'] = pd.to_numeric(df['duration_min'], errors='coerce')
    
    # Create a 'valid' column
    df['valid'] = True
    # Mark invalid rows
    df.loc[df['start'].isna(), 'valid'] = False
    df.loc[df['duration_min'].isna() | (df['duration_min'] < 0), 'valid'] = False
    
    return df

# Step 2: Summarize results
def summarize(df):
    valid = df[df['valid']]
    # Total time by each user
    by_user = valid.groupby('user')['duration_min'].sum().reset_index()
    # Total time by each task type
    by_task = valid.groupby('task_type')['duration_min'].sum().reset_index()
    # Top 3 tasks
    top3 = by_task.sort_values('duration_min', ascending=False).head(3)

    # Save reports to CSV files
    by_user.to_csv('summary_by_user.csv', index=False)
    by_task.to_csv('summary_by_task.csv', index=False)
    top3.to_csv('top3_tasks.csv', index=False)
    df[~df['valid']].to_csv('invalid_rows.csv', index=False)

    print("\n✅ Analysis complete!")
    print("\nTop 3 Tasks:\n", top3)

# Step 3: Main code
if __name__ == "__main__":
    data = load_and_clean("task_logs.csv")
    summarize(data)