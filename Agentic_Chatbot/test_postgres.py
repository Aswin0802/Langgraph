import psycopg

DB_URI = "postgresql://postgres:Aswin%402004@localhost:5432/langgraph?sslmode=disable"
with psycopg.connect(DB_URI) as conn:
    print("PostgreSQL connection successful!")