import psycopg2

# Database connection details (replace with your credentials)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Check if pgvector extension is installed (optional)
cur.execute("SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'")
pgvector_installed = cur.fetchone()[0] > 0

if not pgvector_installed:
  print("pgvector extension not found. Please install it in your database.")
  exit()

# Sample operations (modify based on your needs)

# Create a table with a vector column (if not already exists)
table_name = "my_documents"
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR
);
"""
cur.execute(create_table_query)
conn.commit()

# Insert a document with content and a dummy embedding
content = "This is some sample document content."
dummy_embedding = [1.0, 2.0, 3.0]  # Replace with actual embedding generation logic
insert_query = f"""
INSERT INTO {table_name} (content, embedding)
VALUES (%s, %s)
"""
cur.execute(insert_query, (content, dummy_embedding))
conn.commit()

# Example query to find similar documents (replace with your actual similarity search logic)
query_embedding = [0.5, 1.5, 2.5]  # Replace with your query embedding
similar_query = f"""
SELECT * FROM {table_name}
ORDER BY cosine_distance(embedding, %s::vector) DESC
LIMIT 5;
"""
cur.execute(similar_query, (query_embedding,))
similar_documents = cur.fetchall()

print("Similar documents:")
for doc in similar_documents:
  print(f"  - ID: {doc[0]}, Content: {doc[1]}")

# Close the connection
cur.close()
conn.close()

print("Connection to pgvector database closed.")
