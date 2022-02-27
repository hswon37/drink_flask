from sqlalchemy import create_engine
import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:root@13.209.167.99:3306/drinkDB'
db_connection = create_engine(db_connection_str, encoding='utf8')
conn = db_connection.connect()

#same with dataframe's columns name and table's columns name
drink_data = pd.read_excel('/home/ubuntu/drink_flask/static/drink.xlsx', engine='openpyxl', index_col=0)
drink_data.rename(columns={'ABV':'abv'})

#types, name, region, maker, `ABV`, styles
dtypesql = {'types':sqlalchemy.types.VARCHAR(10), 
          'name':sqlalchemy.types.VARCHAR(50), 
          'region':sqlalchemy.types.VARCHAR(10), 
          'maker':sqlalchemy.types.VARCHAR(300),
          'abv':sqlalchemy.types.FLOAT(5,5), 
          'styles':sqlalchemy.types.VARCHAR(100)
}
drink_data.to_sql(name='drink_pre', con=db_connection, if_exists='replace', index=False, dtype=dtypesql)
