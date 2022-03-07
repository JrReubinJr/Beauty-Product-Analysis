import pandas as pd
import datatable as dt
import numpy as np

###
###Product Purchase Frequncey Analysis
###

customer_products = dt.fread("res/customer_by_product.csv").to_pandas()
items = dt.fread("res/date_frequency.csv").to_pandas()
### Query that produced this CSV
###
# select substring(DATE(o.created_at)::varchar from 1 for 7) as date,
#         o.customer_id as customer,
#         i.product_id as id,
#         prod.title as product,
#         prod.price as price
#         from orders as o
#             inner join items as i on o.id = i.order_id
#             inner join products as prod on i.product_id = prod.id
#             order by customer, date

removeIdx = []
productsRaw = items['product'].unique()
for i in range(0,len(productsRaw)):
    if 'Gift' in productsRaw[i]:
        removeIdx.append(i)
print(removeIdx)
products = np.delete(productsRaw, removeIdx)
print(products)

customers = items['customer'].unique()
dict = {}
for p in products:
    list = []
    for index, row in customer_products.iterrows():
        if p == row['product'] and row['count'] > 3:
            list.append(row['customer'])
    dict[p] = list


purchaseFrequency = [] #purchase frequency

first = True
dateA = None
dateB = None
length = len(dict['2-in-1 Conditioner (16 oz)'])
durationTotal = 0
minDuration = []
for d in dict:
    lowest = 10000
    for c in dict[d]:
        first = True
        total = 0
        count = 0
        for index, row in items.iterrows():
            if c == row['customer'] and row['product'] == d:
                count +=1
                if first:
                    dateB = row['date']
                    first = False
                else:
                    dateA = dateB
                    dateB = row['date']
                    delta = (dateB - dateA).days
                    if delta > 28: lowest = min(delta, lowest)
                    total += delta
        custAvg = total / count
        durationTotal += custAvg

    avgDuration = durationTotal/length
    purchaseFrequency.append(avgDuration)
    minDuration.append(lowest)
    print(f'The average purchase duration for {d} is {avgDuration} days, and the minimum duration is {lowest} days')

resultDF = pd.DataFrame({'Product': products,
                        'Avg Purchase Frequency': purchaseFrequency,
                         'Minimum Duration': minDuration})

resultDF['Recommended Duration 1'] = (resultDF['Avg Purchase Frequency'] + resultDF['Minimum Duration'])/2
resultDF['Recommended Duration 2'] = (resultDF['Avg Purchase Frequency']*0.75 + resultDF['Minimum Duration'])/2
resultDF['Recommended Duration 3'] = (resultDF['Avg Purchase Frequency']*0.5+ resultDF['Minimum Duration'])/2

print(resultDF)
resultDF.to_csv('out/minimum_duration.csv')

