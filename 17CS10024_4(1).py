#Roll Number :- 	  17CS10024
#Name		 :- 	  K.V.R.K.Vivek
#Assignment Number :- 4

# If the obtained clusters are not as expected it is due to the bad 
# initial random points and upon running the code again with a 
# new set of random points we get correct clusters.

import pandas as pd 
import numpy as np 
import math
import random

def dist(a,b):								#	Function for calculating the distance
	distance=0								#	between two points
	for i in range(0,4):
		distance=distance+(a[i]-b[i])*(a[i]-b[i])
	distance=math.sqrt(distance)
	return distance


def jaquard_dist(a,b):						# Calculating the Jacquard distance 
	c_1=0									# of two lists
	for i in range(0,min(len(a),len(b))):
		if a[i][4]==b[i][4]:
			c_1=c_1+1
	return 1-c_1/(len(a)+len(b)-c_1)

inp_data=pd.read_csv('data4_19.csv')

col=inp_data.columns
a1=(col[0])
b1=(col[1])
c1=(col[2])
d1=(col[3])
e1=col[4]
a2=float(col[0])
b2=float(col[1])
c2=float(col[2])
d2=float(col[3])
e2=col[4]
pres_dict={
	'sep_len':a2,
	'sep_wid':b2,
	'pet_len':c2,
	'pet_wid':d2,
	'ground_truth':e2
}
inp_data=inp_data.rename(columns={
	a1:'sep_len',
	b1:'sep_wid',
	c1:'pet_len',
	d1:'pet_wid',
	e1:'ground_truth'
	})

inp_data=inp_data.append(pres_dict,ignore_index=True).reset_index(drop=True)


rand=[]
for i in range(0,100):
	rand.append(i)

pres_choice=np.random.choice(rand,3,[1/3,1/3,1/3])


point_1=inp_data.iloc[pres_choice[0]].tolist()
point_2=inp_data.iloc[pres_choice[1]].tolist()
point_3=inp_data.iloc[pres_choice[2]].tolist()


subset=[]

for i in range(0,10):
	subset_1=[]
	subset_2=[]
	subset_3=[]
	for k in range(0,len(inp_data)):
		j=inp_data.iloc[k].tolist()
		
		dist_1=dist(j,point_1)
		dist_2=dist(j,point_2)
		dist_3=dist(j,point_3)
	
		if(dist_1<=dist_2 and dist_1<=dist_3):
			subset_1.append(j)
		if(dist_2<=dist_1 and dist_2<=dist_3):
			subset_2.append(j)
		if(dist_3<=dist_2 and 	dist_3<=dist_1):
			subset_3.append(j)

	temp1=[0,0,0,0]
	temp2=[0,0,0,0]
	temp3=[0,0,0,0]

	for j in subset_1:
		for l in range(0,4):
			temp1[l]=temp1[l]+j[l]
	for j in subset_2:
		for l in range(0,4):
			temp2[l]=temp2[l]+j[l]
	for j in subset_3:
		for l in range(0,4):
			temp3[l]=temp3[l]+j[l]

	for l in range(0,4):
		point_1[l]=temp1[l]/len(subset_1)
		point_2[l]=temp2[l]/len(subset_2)
		point_3[l]=temp3[l]/len(subset_3)	

print('The final cluster means are ',point_1[:-1],', ',point_2[:-1],', ',point_3[:-1])

subset.append(subset_1)
subset.append(subset_2)
subset.append(subset_3)

inp_subset_1=[]
inp_subset_2=[]
inp_subset_3=[]

for count in range(0,len(inp_data)):
	i=inp_data.iloc[count]
	if i[4]=='Iris-setosa':
		inp_subset_1.append(i)
	if i[4]=='Iris-versicolor':
		inp_subset_2.append(i)
	if i[4]=='Iris-virginica':
		inp_subset_3.append(i)
													# subset contains all the obtained
inp_subset=[]										# clusters.
inp_subset.append(inp_subset_1)						# inp_subset contains all the 
inp_subset.append(inp_subset_2)						# given clusters.
inp_subset.append(inp_subset_3)

matrix=[]
pres=[]


for i in range(0,3):
	pres=[]
	for j in range(0,3):
		pres.append(jaquard_dist(subset[i],inp_subset[j]))
	matrix.append(pres)

jaquard_val=[]

for i in range(0,3):
	pres_min=2;
	for j in range(0,3):
		if matrix[i][j]<pres_min:
			pres_min=matrix[i][j]
			min_ind=j
	jaquard_val.append(pres_min)
	jaquard_val.append(min_ind)

for i in range(0,3):
	if jaquard_val[2*i+1]==0:
		print('The cluster ',i+1,' has a Jacquard distance of ',jaquard_val[2*i],' with Iris-setosa' )
	if jaquard_val[2*i+1]==1:
		print('The cluster ',i+1,' has a Jacquard distance of ',jaquard_val[2*i],' with Iris-versicolor' )
	if jaquard_val[2*i+1]==2:
		print('The cluster ',i+1,' has a Jacquard distance of ',jaquard_val[2*i],' with Iris-virginica' )


