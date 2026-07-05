from app import create_app
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1412200five"
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS careconnect_v2 CHARACTER SET utf8mb4")
conn.commit()
conn.close()

app = create_app()


if __name__ == "__main__":
    app.run()
