import psycopg2
 
conn = psycopg2.connect(
    host="your-hostname.render.com",
    port="5432",
    dbname="your-db-name",
    user="your-username",
    password="your-password"
)
 
cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
 
cur.close()
conn.close