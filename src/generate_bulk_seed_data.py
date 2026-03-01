import pandas as pd
import numpy as np
import random
import argparse
import os
from datetime import datetime, timedelta

"""
Bulk seed data generator.
Usage: python generate_bulk_seed_data.py --count 3000
"""
def random_date(start, end):
    """Generate a random date between start and end"""
    delta = end - start
    int_delta = delta.days
    if int_delta <= 0:
        return start
    random_day = random.randrange(int_delta)
    return start + timedelta(days=random_day)


def main(csv_path, count):
    df = pd.read_csv(csv_path)
    # Prepare ranges and templates
    max_id = df.iloc[:, 0].max()  # assumes first column is transaction_id
    # Get categorical columns (object dtype)
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    # Get numeric columns
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Determine date range from existing data
    try:
        dates = pd.to_datetime(df['event_date'], dayfirst=True, errors='coerce')
        min_date = dates.min() if dates.notna().any() else datetime(2000,1,1)
        max_date = dates.max() if dates.notna().any() else datetime.now()
    except Exception:
        min_date, max_date = datetime(2000,1,1), datetime.now()
    # Unique values for categorical to sample
    cat_values = {col: df[col].dropna().unique().tolist() for col in cat_cols}

    new_rows = []
    for i in range(1, count+1):
        max_id += 1
        # start with template from random existing row
        template = df.sample(1).iloc[0].to_dict()
        row = {}
        for col in df.columns:
            if col == df.columns[0]:  # transaction_id
                row[col] = max_id
            elif col == 'event_date':
                d = random_date(min_date, max_date)
                row[col] = d.strftime('%d/%m/%Y')
            elif col in cat_cols:
                row[col] = random.choice(cat_values.get(col, [template[col]]))
            elif col in num_cols:
                # perturb numeric by up to ±10%
                val = template[col]
                row[col] = round(max(0, val * (1 + random.uniform(-0.1, 0.1))), 4)
            else:
                row[col] = template[col]
        new_rows.append(row)
    df_new = pd.DataFrame(new_rows)
    df_out = pd.concat([df, df_new], ignore_index=True)
    df_out.to_csv(csv_path, index=False)
    print(f"Appended {count} rows to {csv_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bulk seed data generator')
    parser.add_argument('--count', type=int, required=True, help='Number of rows to append')
    args = parser.parse_args()
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'seeds', 'seed_data.csv')
    )
    main(csv_path, args.count)
