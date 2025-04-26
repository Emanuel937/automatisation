import pandas as pd
import os

file = 'upower.xlsx'

path = os.path.join(file)

df = pd.read_excel(path)

new_df = []



for index, row in df.iterrows():
    row_attr = row['attr']
    row_index = row['INDEX']

    # Extraire les valeurs depuis 'attr'
    attr_array = row_attr.split(':')

    if len(attr_array) > 1:
        attr_name = attr_array[0]
        attr_values = attr_array[1].split(',')

        for idx, element in enumerate(attr_values):
            # Déterminer le type d'attribut
            if  'Pointures' in attr_name:
                attr_type = 'select'
              
            else:
                attr_type = 'radio'
                

            new_df.append({
                "INDEX": row_index,
                "ATTR_NAME": f'{attr_name}:{attr_type}:{0}',
                "ATTR_VALUE": f'{element}:{0}'
            })

# Convertir en DataFrame et enregistrer
new_df = pd.DataFrame(new_df)
new_df.to_excel('upower-d.xlsx', index=False)
