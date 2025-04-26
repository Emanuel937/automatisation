import pandas as pd

data = [[1, 2 , 4],[2, 4, 5]]
df = pd.DataFrame(data, columns=["id", "age", "last"])
print(df)

#data frame form dic 


my_dic = {
    "name":[
        "emanuel",
        "abizimi"
    ],
    "age":[
        27,
        50
    ],
    "country":[
        "angola",
        "portugal"
    ]

}


newDF = pd.DataFrame(my_dic, columns=['country', 'age'])

print(newDF)



#list of dic 

ldic = [
    {"name": "emauel abizimi", "age":20, "country": "Angola"},
     {"name": "emauel abizi", "age":25, "country": "Angola"}
]



ldicDF = pd.DataFrame(ldic)

print(ldicDF)

ldicDF = ldicDF.rename(columns={"name":"apelido"})

#drop column where age is 25 
ldicDF = ldicDF['apelido']


print(ldicDF)
