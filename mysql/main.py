import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2406",
    database="first_database"
)

mycursor = db.cursor()

mycursor.execute(
    """
    INSERT INTO test (name, gender) VALUES (%s,%s)
    """, ("Florian", "male")
)
db.commit()
