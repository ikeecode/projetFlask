import psycopg2
from models.users import db, app

user = input('Entrer du user :  ')
password = input('Entrer votre mot de passe :  ')
database = input('Entrer le nom de la base de donnee à creer :  ')

#establishing the connection
conn = psycopg2.connect(
   database="postgres",
   user=f'{user}',
   password=f'{password}',
   host='127.0.0.1',
   port= '5432'
)

conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = f'''CREATE database {database}''';

#Creating a database
cursor.execute(sql)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost/{database}'

db.create_all()
print("Database created successfully........")

#Closing the connection
conn.close()

# sudo -u postgres psql postgres
#
# ALTER USER username CREATEDB; donne le droit a un user de creeer une base


# CREATE ROLE user_name PASSWORD 'tYPe_YoUr_PaSSwOrD' NOSUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
