import pandas as pd 

marque     = 'BOSCH'
price_file = pd.read_excel('bosch_products.xlsx')
left_file  = pd.read_excel('bosch_price.xlsx')


result     = left_file.merge(price_file['prince'], on='reference', how='left') 