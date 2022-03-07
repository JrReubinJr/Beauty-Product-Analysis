import pandas as pd
import datatable as dt


###
###Return Customer Analysis
###

customer_products = dt.fread("res/customer_by_product.csv").to_pandas()
### Query that produced this csv
# select o.customer_id as customer, prod.title as product, count(*)
# 	from orders as o
# 	inner join items as i on o.id = i.order_id
# 	inner join products as prod on i.product_id = prod.id
# 	group by(customer, product)
# 	order by count desc


products = customer_products['product'].unique()
product_frequency = customer_products['product'].value_counts().values
print(product_frequency)

purchases = []
frequency = []
print(products)

for p in products:
    purchase_count = 0
    count = 0
    for index, row in customer_products.iterrows():
        if p == row['product']:
            purchase_count += row['count']
            count +=1
            #print(p, customer_count)
    purchases.append(purchase_count)
    frequency.append(count)


resultDF = pd.DataFrame({'Product': products,
                         'Unique Purchases': frequency,
                         'Purchase Count': purchases})

resultDF['purchase_rate'] = resultDF['Purchase Count']/resultDF['Unique Purchases']

print(resultDF)

resultDF.to_csv('out/return_customers.csv')
