import json, csv
import pandas as pd

inputFile = open('yelp_academic_dataset_business.json') #open json file
outputFile = open('business_list.csv', 'w') #load csv file
  
  
# Opening JSON file and loading the data 
# into the variable data 
data=[]
with open('yelp_academic_dataset_business.json', errors='ignore') as json_file: 
  for line in json_file:
    data.append(json.loads(line))
 
 
# now we will open a file for writing 
data_file = open('business_list.csv', 'w') 
  
# create the csv writer object 
csv_writer = csv.writer(data_file) 
  
# Counter variable used for writing  
# headers to the CSV file 
count = 0
  
for emp in data: 
    if count == 0: 
  
        # Writing headers of CSV file 
        header = emp.keys() 
        csv_writer.writerow(header) 
        count += 1
  
    # Writing data of CSV file 
    csv_writer.writerow(emp.values()) 
  
data_file.close() 

df = pd.read_csv('business_list.csv', encoding = "ISO-8859-1")
# a=list(df.city.unique())
# for i in a:
# 	DF=df[df['city']==i]
# 	DF=DF[DF['categories'].str.contains('estaurant', na=False)]
# 	avg_c=DF['review_count'].mean(skipna = True)
# 	tot_c=DF.shape[0]
# 	tot=avg_c*tot_c
# 	if tot> 10000 and tot< 20000:
# 		print(i, avg_c, tot_c)

DF=df[df['city']=='Avondale']
DF=DF[DF['categories'].str.contains('estaurant', na=False)]

DF.to_csv ('Avondale_Restaurants.csv', index = False, header=True)

BIDs=[]
name_loc=[]
for index, row in DF.iterrows():
	BIDs.append(row['business_id'])
	name_loc.append((row['name'], row['latitude'], row['longitude']))


data=[]
with open('yelp_academic_dataset_review.json', errors='ignore') as json_file: 
  for line in json_file:
    data.append(json.loads(line))
 
 
# now we will open a file for writing 
data_file = open('Avondale_Restaurant_Review.csv', 'w', newline='') 
  
# create the csv writer object 
csv_writer = csv.writer(data_file) 

count=0
  
for emp in data: 
    if count == 0: 
  
        # Writing headers of CSV file 
        header = list(emp.keys())
        headers = header[:3]+['restaurant_name', 'latitude', 'longitude']+header[3:]
        csv_writer.writerow(headers) 
        count += 1
  
    # Writing data of CSV file 
    val=list(emp.values())
    try:
    	i=BIDs.index(val[2])
    	vals=val[:3]+[name_loc[i][0], name_loc[i][1], name_loc[i][2]]+val[3:]
    	csv_writer.writerow(vals)
    except ValueError:
    	continue

