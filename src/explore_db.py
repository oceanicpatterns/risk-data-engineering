import duckdb

DB_PATH = 'db.db'  # Adjust path if needed

if __name__ == "__main__":
    con = duckdb.connect(DB_PATH)
    print("Tables in database:")
    tables = con.execute("SHOW TABLES").fetchall()
    if tables:
        for t in tables:
            print(f"- {t[0]}")
        print("\nPreview of each table:")
        for t in tables:
            print(f"\nFirst 10 rows of '{t[0]}':")
            print(con.execute(f"SELECT * FROM {t[0]} LIMIT 10").fetchdf())
    else:
        print("No tables found.")
    con.close()
