from flask import Flask,render_template,request
import json
import pandas as pd
import matplotlib.pyplot as pplt
import numpy as np
import sys
import os
import shutil
from zipfile import *
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import subprocess
from openpyxl import Workbook
from tqdm import tqdm
import math
import pickle


file_uploaded_currently=''

app=Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/update", methods=['GET', 'POST'])
def update():
	if request.method == 'POST':
		plotdata=request.get_data()
		plotdata=json.loads(plotdata)
		print(plotdata)
		retpath=""
		models=plotdata['model_list']
		models=models.replace("\n"," ")
		models=models.split(' ')
		df_overall=pd.DataFrame()
		df_dataset=pd.read_csv('./static/data/'+plotdata['data_source']+'/'+plotdata['data_source']+'-dev.csv')
		print(df_dataset.head(5))
		df_overall['sample_id']=df_dataset.index
		df_overall['sample']=df_dataset['sentence']
		df_overall['gold']=df_dataset['label']
		for i in range(len(models)):
			infile='./static/data/'+plotdata['data_source']+'/'+'PLOTS.xlsx'
			df_rawmodel=pd.read_excel(infile,sheet_name=models[i],engine='openpyxl')
			print(df_rawmodel.head(5))
			df_overall[models[i]+'_model_label']=df_rawmodel['LABEL']
			arr=[]
			for j in range(len(df_rawmodel)):
				arr.append(max(df_rawmodel.iloc[j]['P1'],df_rawmodel.iloc[j]['P2']))
			df_overall[models[i]+'_confidence']=arr			
#----------------------------------------------------------------------------------------------------
		if(plotdata['metric_selected']=='WOOD'):
			if(plotdata['data_source']=='SST-2'):
				tg1=np.load("./static/data/SST-2/slurm_chunk0000_4412163.npy")
				tg2=np.load("./static/data/SST-2/slurm_chunk0001_4412161.npy")
				tg3=np.load("./static/data/SST-2/slurm_chunk0002_4412160.npy")
				tg4=np.load("./static/data/SST-2/slurm_chunk0003_4412162.npy")
				tg5=np.load("./static/data/SST-2/slurm_chunk0004_4412166.npy")
				tg6=np.load("./static/data/SST-2/slurm_chunk0005_4412167.npy")
				tg7=np.load("./static/data/SST-2/slurm_chunk0006_4412164.npy")
				tg8=np.load("./static/data/SST-2/slurm_chunk0007_4412165.npy")
				tg9=np.load("./static/data/SST-2/slurm_chunk0008_4412168.npy")
				tg10=np.load("./static/data/SST-2/slurm_chunk0009_4412170.npy")
				tg11=np.load("./static/data/SST-2/slurm_chunk0010_4412169.npy")
				tg12=np.load("./static/data/SST-2/slurm_chunk0011_4412172.npy")
				tg13=np.load("./static/data/SST-2/slurm_chunk0012_4412171.npy")
				tg14=np.load("./static/data/SST-2/slurm_chunk0013_4412173.npy")
				tg15=np.load("./static/data/SST-2/slurm_chunk0014_4412174.npy")
				tg16=np.load("./static/data/SST-2/slurm_chunk0015_4412175.npy")
				tg17=np.load("./static/data/SST-2/slurm_chunk0016_4412176.npy")
				tg18=np.load("./static/data/SST-2/slurm_chunk0017_4412177.npy")
				tg19=np.load("./static/data/SST-2/slurm_chunk0018_4412179.npy")
				tg20=np.load("./static/data/SST-2/slurm_chunk0019_4412178.npy")
				tg21=np.load("./static/data/SST-2/slurm_chunk0020_4412180.npy")
				tg22=np.load("./static/data/SST-2/slurm_chunk0021_4412181.npy")
				tg23=np.load("./static/data/SST-2/slurm_chunk0022_4412182.npy")
				tg24=np.load("./static/data/SST-2/slurm_chunk0023_4412183.npy")
			else:
				#IMDB here slurm chunks
				tg1=np.load("./static/data/IMDb/slurm_chunk0000_4414910.npy")
				tg2=np.load("./static/data/IMDb/slurm_chunk0001_4414911.npy")
				tg3=np.load("./static/data/IMDb/slurm_chunk0002_4414909.npy")
				tg4=np.load("./static/data/IMDb/slurm_chunk0003_4414912.npy")
				tg5=np.load("./static/data/IMDb/slurm_chunk0004_4414914.npy")
				tg6=np.load("./static/data/IMDb/slurm_chunk0005_4414913.npy")
				tg7=np.load("./static/data/IMDb/slurm_chunk0006_4414916.npy")
				tg8=np.load("./static/data/IMDb/slurm_chunk0007_4414919.npy")
				tg9=np.load("./static/data/IMDb/slurm_chunk0008_4414915.npy")
				tg10=np.load("./static/data/IMDb/slurm_chunk0009_4414918.npy")
				tg11=np.load("./static/data/IMDb/slurm_chunk0010_4414917.npy")
				tg12=np.load("./static/data/IMDb/slurm_chunk0011_4414922.npy")
				tg13=np.load("./static/data/IMDb/slurm_chunk0012_4414920.npy")
				tg14=np.load("./static/data/IMDb/slurm_chunk0013_4414921.npy")
				tg15=np.load("./static/data/IMDb/slurm_chunk0014_4414923.npy")
				tg16=np.load("./static/data/IMDb/slurm_chunk0015_4414925.npy")
				tg17=np.load("./static/data/IMDb/slurm_chunk0016_4414924.npy")
				tg18=np.load("./static/data/IMDb/slurm_chunk0017_4414926.npy")
				tg19=np.load("./static/data/IMDb/slurm_chunk0018_4414927.npy")
				tg20=np.load("./static/data/IMDb/slurm_chunk0019_4414929.npy")
				tg21=np.load("./static/data/IMDb/slurm_chunk0020_4414931.npy")
				tg22=np.load("./static/data/IMDb/slurm_chunk0021_4414928.npy")
				tg23=np.load("./static/data/IMDb/slurm_chunk0022_4414930.npy")
				tg24=np.load("./static/data/IMDb/slurm_chunk0023_4414932.npy")
			testgood=pd.DataFrame(tg1)
			testgood=testgood.append(list(tg2))
			testgood=testgood.append(list(tg3))
			testgood=testgood.append(list(tg4))
			testgood=testgood.append(list(tg5))
			testgood=testgood.append(list(tg6))
			testgood=testgood.append(list(tg7))
			testgood=testgood.append(list(tg8))
			testgood=testgood.append(list(tg9))
			testgood=testgood.append(list(tg10))
			testgood=testgood.append(list(tg11))
			testgood=testgood.append(list(tg12))
			testgood=testgood.append(list(tg13))
			testgood=testgood.append(list(tg14))
			testgood=testgood.append(list(tg15))
			testgood=testgood.append(list(tg16))
			testgood=testgood.append(list(tg17))
			testgood=testgood.append(list(tg18))
			testgood=testgood.append(list(tg19))
			testgood=testgood.append(list(tg20))
			testgood=testgood.append(list(tg21))
			testgood=testgood.append(list(tg22))
			testgood=testgood.append(list(tg23))
			testgood=testgood.append(list(tg24))
			testgood=testgood.reset_index(drop=True)
			testgood_t=testgood
			testgood_transpose=testgood_t.transpose()
			arr=testgood_transpose.values
			percents=['1','5','10','25','30','40','50','75','100']
			per=plotdata['sts_percentage']
			persize=len(testgood_transpose.columns)
			endindex=math.ceil((float(per)/100)*persize)
			stsarr=[]
			for k in tqdm(range(len(arr))):
				a=list(arr[k])
				a.sort(reverse=True)
				stsarr.append(sum(a[0:endindex])/endindex)
			df_overall['STS']=stsarr
			df_overall=df_overall.sort_values(by=['STS'],ascending=False)
			split_number=int(plotdata['split_number'])
			weighting=plotdata['weighting']
			valp=[]
			valn=[]
			if(weighting=='NN'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(split_number-pp)
			elif(weighting=='NZ'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(0)
			elif(weighting=='ZN'):
				for pp in range(split_number):
					valp.append(0)
					valn.append(split_number-pp)
			elif(weighting=='NT'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append((split_number-pp)/2)
			elif(weighting=='TN'):
				for pp in range(split_number):
					valp.append((split_number-pp)/2)
					valn.append(split_number-pp)			
			split_result=[]
			splitindex=[]
			split_type=plotdata['split_formation']
			for ii in range(split_number):
				splitindex.append([])
			if(split_type=='E'):
				split_result=np.array_split(range(len(df_overall)), split_number)
				for ii in range(len(split_result)):
						splitindex[ii].append(split_result[ii][0])
						splitindex[ii].append(split_result[ii][len(split_result[ii])-1])
			else:
				stsarr=list(df_overall['STS'])
				startsts=stsarr[0]
				endsts=stsarr[len(stsarr)-1]
				interval=(startsts-endsts)/split_number
				intervals=[]
				for ii in range(split_number):
					intervals.append(endsts+ii*interval)
				sindex=split_number-1
				splitindex[0].append(0)
				for ii in range(len(df_overall)):
					if(df_overall.iloc[ii]['STS']<intervals[sindex]):
						splitindex[split_number-sindex-1].append(ii-1)
						sindex=sindex-1
						splitindex[split_number-sindex-1].append(ii)
				splitindex[len(splitindex)-1].append(len(df_overall)-1)
			factor=plotdata['weight_factor']
			for m in range(len(models)):
				arr=[]
				for ii in range(len(df_overall)):
					if(df_overall.iloc[ii]['gold']==df_overall.iloc[ii][models[m]+'_model_label']):
						arr.append(1)
					else:
						arr.append(-1)
				if(factor=='O'):
					df_overall[models[m]+'_factor']=arr
				elif(factor=='P'):
					for ii in range(len(df_overall)):
						arr[ii]=arr[ii]*df_overall.iloc[ii][models[m]+'_confidence']
					df_overall[models[m]+'_factor']=arr
				elif(factor=='S'):
					for ii in range(len(df_overall)):
						arr[ii]=arr[ii]*df_overall.iloc[ii]['STS']
					df_overall[models[m]+'_factor']=arr
			wood=[]
			acc=[]
			splitwiserow=[]
			splitwisevalue=[]
			splitwisemodel=[]
			for calc in range(len(models)):
				sarr=[]
				sarrr=[]
				for calcc in range(len(splitindex)):
					sarr.append(list(df_overall[models[calc]+'_factor'][splitindex[calcc][0]:splitindex[calcc][1]]))
					sarrr.append(list(df_overall[models[calc]+'_factor'][splitindex[calcc][0]:splitindex[calcc][1]]))
					nr=0.0
					dr=0.0
				for x in range(len(sarr)):
					for xx in range(len(sarr[x])):
						if(sarr[x][xx]>0):
							sarr[x][xx]=sarr[x][xx]*valp[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valp[split_number-x-1]
						else:
							sarr[x][xx]=sarr[x][xx]*valn[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valn[split_number-x-1]						
					nr=nr+sum(sarr[x])
					dr=dr+sum(sarrr[x])
					print(sum(sarr[x]),sum(sarrr[x]),x+1,models[calc])
					if(sum(sarrr[x])==0):
						splitwisevalue.append(0)
					else:
						splitwisevalue.append(sum(sarr[x])/sum(sarrr[x]))
					splitwiserow.append(x+1)
					splitwisemodel.append(models[calc])
				wood.append(nr/dr*100)
				s=list(df_overall[models[calc]+'_factor'])
				acc.append(len(list(filter(lambda x:(x>=0),s)))*100/len(s))
			print(df_overall.head(20),endindex,valp,valn,splitindex,wood,acc,models)
			split_column=[]
			for i in range(len(splitindex)):
				adding=splitindex[i][1]-splitindex[i][0]+1
				for j in range(adding):
					split_column.append(i+1)
			df_save=pd.DataFrame()
			df_save['val']=df_overall['STS']
			for ii in range(len(models)):
				df_save[models[ii]+'_factor']=df_overall[models[ii]+'_factor']
			df_save['ID']=df_overall['sample_id']
			df_save['sample']=df_overall['sample']
			df_save['gold']=df_overall['gold']
			df_save['split']=split_column
			df_save['val'].round(decimals=4)
			if os.path.isdir('./static/data/plotting'):
				shutil.rmtree('./static/data/plotting')
			os.mkdir('./static/data/plotting')
			df_save.to_csv('./static/data/plotting/beeswarm-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save1=pd.DataFrame()
			df_save1['Split']=splitwiserow
			df_save1['Score']=splitwisevalue
			df_save1['Label']=splitwisemodel
			df_save1.to_csv('./static/data/plotting/splitwise-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save2a=pd.DataFrame()
			df_save2a['Acc']=acc
			df_save2a['Score']=wood
			df_save2a['Model']=models
			df_save2a=df_save2a.sort_values(by=['Acc'],ascending=True)
			df_save2b=pd.DataFrame()
			df_save2b['Acc']=acc
			df_save2b['Score']=wood
			df_save2b['Model']=models
			df_save2b=df_save2b.sort_values(by=['Score'],ascending=True)
			df_save2=pd.DataFrame()
			df_save2['Acc']=df_save2a['Acc']
			df_save2['Score']=df_save2a['Score']
			df_save2['Model']=list(df_save2a['Model'])
			df_save2['WModel']=list(df_save2b['Model'])
			print(df_save2a['Model'],df_save2b['Model'],df_save2)
			df_save2.to_csv('./static/data/plotting/acc-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			c=[[],[],[],[],[]]
			for i in range(split_number):				
				df_temp=df_save[df_save['split'] == i+1]
				for m in range(len(models)):
					df_tempp=df_temp[df_temp[models[m]+'_factor'] >= 0]
					c[0].append(models[m])
					c[1].append(len(df_temp))
					c[2].append(len(df_tempp))
					c[3].append(len(df_temp)-len(df_tempp))
					c[4].append(i+1)
			df_sun=pd.DataFrame()
			df_sun['Model']=c[0]
			df_sun['Split']=c[4]
			df_sun['Size']=c[1]
			df_sun['Correct']=c[2]
			df_sun['Incorrect']=c[3]
			df_sun.to_csv('./static/data/plotting/sun-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
#----------------------------------------------------------------------------------------------------
		elif(plotdata['metric_selected']=='WMProb'):
			df_mprob=pd.DataFrame()
			for i in range(len(models)):
				dfx=pd.DataFrame()
				dfx['confidence']=df_overall[models[i]+'_confidence']
				dfx['label']=df_overall[models[i]+'_model_label']
				dfx['gold']=df_overall['gold']
				dfx['sampleid']=df_overall['sample_id']
				dfx=dfx.sort_values(by=['confidence'],ascending=False)
				m=models[i]
				df_mprob[m+'_id']=list(dfx['sampleid'])
				df_mprob[m+'_label']=list(dfx['label'])
				df_mprob[m+'_gold']=list(dfx['gold'])
				df_mprob[m+'_confidence']=list(dfx['confidence'])
			split_number=int(plotdata['split_number'])
			weighting=plotdata['weighting']
			valp=[]
			valn=[]
			if(weighting=='NN'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(split_number-pp)
			elif(weighting=='NZ'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(0)
			elif(weighting=='ZN'):
				for pp in range(split_number):
					valp.append(0)
					valn.append(split_number-pp)
			elif(weighting=='NT'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append((split_number-pp)/2)
			elif(weighting=='TN'):
				for pp in range(split_number):
					valp.append((split_number-pp)/2)
					valn.append(split_number-pp)			
			split_result=[]
			splitindex=[]
			split_type=plotdata['split_formation']
			for ii in range(split_number):
				splitindex.append([])
			if(split_type=='E'):
				split_result=np.array_split(range(len(df_mprob)), split_number)
				for ii in range(len(split_result)):
						splitindex[ii].append(split_result[ii][0])
						splitindex[ii].append(split_result[ii][len(split_result[ii])-1])
				splits_i=[]
				for ii in range(len(models)):
					splits_i.append(splitindex)
				splitindex=splits_i
			else:
				splitindex=[]
				for ii in range(len(models)):
					splitindex.append([])
				for ii in range(len(splitindex)):
					for jj in range(split_number):
						splitindex[ii].append([])
				arrm=[]
				for ii in range(len(models)):
					arrm.append(models[ii]+'_confidence')
				maxval=df_mprob[arrm].max().max()
				minval=df_mprob[arrm].min().min()
				interval=(maxval-minval)/split_number
				intervals=[]
				for ii in range(split_number):
					intervals.append(minval+ii*interval)
				sindex=split_number-1
				for ii in range(len(models)):
					splitindex[ii][0].append(0)
				for mm in range(len(models)):
					sindex=split_number-1
					for ii in range(len(df_mprob)):
						if(df_mprob.iloc[ii][models[mm]+'_confidence']<intervals[sindex]):
							splitindex[mm][split_number-sindex-1].append(ii-1)
							sindex=sindex-1
							splitindex[mm][split_number-sindex-1].append(ii)				
			print(splitindex)
			factor=plotdata['weight_factor']
			for m in range(len(models)):
				arr=[]
				for ii in range(len(df_mprob)):
					if(df_mprob.iloc[ii][models[m]+'_gold']==df_mprob.iloc[ii][models[m]+'_label']):
						arr.append(1)
					else:
						arr.append(-1)
				if(factor=='O'):
					df_mprob[models[m]+'_factor']=arr
				elif(factor=='P'):
					for ii in range(len(df_mprob)):
						arr[ii]=arr[ii]*df_mprob.iloc[ii][models[m]+'_confidence']
					df_mprob[models[m]+'_factor']=arr
			wmprob=[]
			acc=[]
			splitwiserow=[]
			splitwisevalue=[]
			splitwisemodel=[]
			for i in range(len(splitindex)):
				for j in range(len(splitindex[i])):
					if(len(splitindex[i][j])==0):
						splitindex[i][j].append(871)
						splitindex[i][j].append(871)
					elif(len(splitindex[i][j])==1):
						splitindex[i][j].append(871)
			print(splitindex)
			for i in range(len(splitindex)):
				sarr=[]
				sarrr=[]
				nr=0.0
				dr=0.0
				for j in range(len(splitindex[i])):
					sarr.append(list(df_mprob[models[i]+'_factor'][splitindex[i][j][0]:splitindex[i][j][1]]))
					sarrr.append(list(df_mprob[models[i]+'_factor'][splitindex[i][j][0]:splitindex[i][j][1]]))
				for x in range(len(sarr)):
					for xx in range(len(sarr[x])):
						if(sarr[x][xx]>0):
							sarr[x][xx]=sarr[x][xx]*valp[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valp[split_number-x-1]
						else:
							sarr[x][xx]=sarr[x][xx]*valn[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valn[split_number-x-1]						
					nr=nr+sum(sarr[x])
					dr=dr+sum(sarrr[x])
					if(sum(sarrr[x])==0):
						splitwisevalue.append(0)
					else:
						splitwisevalue.append(sum(sarr[x])/sum(sarrr[x]))
					splitwiserow.append(x+1)
					splitwisemodel.append(models[i])
				wmprob.append(nr/dr*100)
				s=list(df_mprob[models[i]+'_factor'])
				acc.append(len(list(filter(lambda x:(x>=0),s)))*100/len(s))
			print(df_mprob.head(20),valp,valn,splitindex,wmprob,acc,models,splitwisevalue,splitwisemodel,splitwiserow)	
			df_save=pd.DataFrame()
			for ii in range(len(splitindex)):
				split_column=[]
				for jj in range(len(splitindex[ii])):
					adding=splitindex[ii][jj][1]-splitindex[ii][jj][0]+1
					for kk in range(adding):
						split_column.append(jj+1)
				split_column=split_column[:872]
				df_save[models[ii]+'-split']=split_column			
			for i in range(len(models)):
				df_save[models[i]+'_factor']=df_mprob[models[i]+'_factor']
				df_save[models[i]+'_gold']=df_mprob[models[i]+'_gold']
				df_save[models[i]+'_id']=df_mprob[models[i]+'_id']
				df_save[models[i]+'-val']=df_mprob[models[i]+'_confidence']
				df_save[models[i]+'-val'].round(decimals=4)
			if os.path.isdir('./static/data/plotting'):
				shutil.rmtree('./static/data/plotting')
			os.mkdir('./static/data/plotting/')
			df_save.to_csv('./static/data/plotting/beeswarm-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save1=pd.DataFrame()
			df_save1['Split']=splitwiserow
			df_save1['Score']=splitwisevalue
			df_save1['Label']=splitwisemodel
			df_save1.to_csv('./static/data/plotting/splitwise-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save2a=pd.DataFrame()
			df_save2a['Acc']=acc
			df_save2a['Score']=wmprob
			df_save2a['Model']=models
			df_save2a=df_save2a.sort_values(by=['Acc'],ascending=True)
			df_save2b=pd.DataFrame()
			df_save2b['Acc']=acc
			df_save2b['Score']=wmprob
			df_save2b['Model']=models
			df_save2b=df_save2b.sort_values(by=['Score'],ascending=True)
			df_save2=pd.DataFrame()
			df_save2['Acc']=df_save2a['Acc']
			df_save2['Score']=df_save2a['Score']
			df_save2['Model']=list(df_save2a['Model'])
			df_save2['WModel']=list(df_save2b['Model'])
			print(df_save2a['Model'],df_save2b['Model'],df_save2)
			df_save2.to_csv('./static/data/plotting/acc-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			c=[[],[],[],[],[]]
			for i in range(split_number):				
				for m in range(len(models)):
					df_temp=df_save[df_save[models[m]+'-split'] == i+1]
					df_tempp=df_temp[df_temp[models[m]+'_factor'] >= 0]
					c[0].append(models[m])
					c[1].append(len(df_temp))
					c[2].append(len(df_tempp))
					c[3].append(len(df_temp)-len(df_tempp))
					c[4].append(i+1)
			df_sun=pd.DataFrame()
			df_sun['Model']=c[0]
			df_sun['Split']=c[4]
			df_sun['Size']=c[1]
			df_sun['Correct']=c[2]
			df_sun['Incorrect']=c[3]
			print(df_sun)
			df_sun.to_csv('./static/data/plotting/sun-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
#----------------------------------------------------------------------------------------------------
		elif(plotdata['metric_selected']=='WSBias'):
			print(df_overall)
			df_bias=pd.DataFrame()
			algo=plotdata['bias_algo']
			if(plotdata['data_source']=='SST-2'):
				if(algo=='1'):
					print("ALGO 128")
					fpath='./static/data/'+plotdata['data_source']+'/algo1.pkl'
					with open(fpath, 'rb') as f:
						data = pickle.load(f)
					scores=list(data.values())
					ids=list(data.keys())
					df=pd.read_csv('./static/data/'+plotdata['data_source']+"/algo1data.csv")
					ar=list(df['sentence'])
					arr=list(df_overall['sample'])
					ind=[]
					for i in range(len(ar)):
						ind.append(arr.index(ar[i]))
					df['INDEX']=ind
					ind=list(df.index)
					pred=[]
					for i in range(len(df)):
						y=ids.index(ind[i])
						x=scores[y]
						pred.append(x)
					df['SCORE']=pred
					df_bias=df
				else:
					print("4 Models")
					fpath='./static/data/'+plotdata['data_source']+'/algo2.pkl'
					with open(fpath, 'rb') as f:
						data = pickle.load(f)
					scores=list(data.values())
					ids=list(data.keys())
					df=pd.read_csv('./static/data/'+plotdata['data_source']+"/algo2data.csv")
					ar=list(df['sentence'])
					arr=list(df_overall['sample'])
					ind=[]
					for i in range(len(ar)):
						ind.append(arr.index(ar[i]))
					df['INDEX']=ind
					ind=list(df.index)
					pred=[]
					for i in range(len(df)):
						y=ids.index(ind[i])
						x=scores[y]
						pred.append(x)
					df['SCORE']=pred
					df_bias=df
				for ii in tqdm(range(len(models))):
					ind=df_bias['INDEX']
					aaa=[]
					aaaa=[]
					aaaaa=[]
					minfile='./static/data/'+plotdata['data_source']+'/'+'PLOTS.xlsx'
					df_temp=pd.read_excel(minfile,sheet_name=models[ii],engine='openpyxl')
					for i in range(len(ind)):
						a=list(df_temp.loc[ind[i]])
						aa=list(df_bias.loc[i])
						p=max(a[3],a[4])
						q=aa[3]
						r=1
						if(a[7]!=aa[1]):
							p=p*-1
							q=q*-1
							r=-1
						aaa.append(p)
						aaaa.append(q)
						aaaaa.append(r)
					df_bias[models[ii]]=aaa
					df_bias[models[ii]+'-P']=aaaa
					df_bias[models[ii]+'-1']=aaaaa
			else:
				keeparr=[3,37,38,95,138,188,257,271,324,334,362,387,388,428,487,492,587,604,701,773,782,785,791,890,895,907,908,921,927,935,972,979,1000,1042,1066,1076,1092,1094,1101,1103,1107,1130,1159,1167,1170,1207,1231,1270,1317,1321,1367,1405,1434,1441,1450,1484,1489,1524,1575,1610,1625,1642,1651,1658,1670,1791,1795,1850,1914,1953,2067,2108,2166,2177,2218,2235,2271,2289,2296,2419,2449,2488,2507,2543,2594,2646,2647,2648,2692,2725,2763,2784,2821,2829,2851,2881,3072,3082,3091,3146,3158,3270,3298,3314,3317,3438,3490,3520,3581,3638,3656,3701,3707,3716,3889,3911,3940,3972,4001,4015,4040,4078,4109,4112,4143,4174,4222,4227,4265,4280,4324,4463,4505,4518,4563,4570,4586,4617,4622,4680,4724,4735,4761,4791,4801,4840,4850,4879,4909,4924,4928,4937,4947,4965,4966,4984,5034,5037,5089,5140,5196,5258,5279,5294,5324,5327,5342,5399,5430,5438,5473,5524,5571,5691,5744,5755,5759,5781,5931,5965,5968,5979,6055,6091,6125,6183,6229,6289,6319,6337,6382,6432,6467,6472,6481,6519,6530,6534,6545,6593,6626,6696,6737,6745,6818,6819,6870,6945,6988,7003,7021,7023,7065,7085,7097,7110,7114,7123,7164,7184,7205,7233,7251,7337,7374,7375,7392,7431,7509,7515,7577,7597,7661,7684,7797,7837,7847,7873,7924,8006,8022,8074,8075,8097,8099,8185,8249,8278,8292,8296,8305,8400,8457,8475,8529,8576,8631,8646,8652,8662,8696,8752,8829,8906,8944,8955,8960,8985,9055,9208,9274,9296,9305,9316,9376,9383,9397,9532,9561,9568,9571,9672,9700,9702,9797,9936,10090,10113,10137,10153,10184,10208,10277,10279,10334,10336,10362,10371,10506,10528,10572,10608,10634,10682,10686,10687,10720,10763,10804,10812,10834,10892,10899,10901,10914,11001,11043,11045,11055,11116,11124,11140,11204,11398,11432,11496,11529,11584,11612,11615,11668,11684,11702,11737,11800,11828,11839,11846,11927,11976,12001,12002,12040,12058,12131,12158,12165,12172,12184,12268,12288,12325,12328,12405,12409,12503,12550,12560,12583,12595,12659,12676,12710,12744,12753,12765,12814,12901,12928,13052,13055,13078,13101,13114,13127,13131,13158,13166,13218,13256,13261,13316,13343,13380,13381,13407,13451,13498,13537,13555,13575,13589,13625,13654,13686,13691,13715,13788,13794,13803,13868,13889,13892,13924,13926,13965,14039,14052,14076,14081,14098,14135,14210,14232,14239,14275,14278,14339,14366,14376,14381,14420,14422,14450,14458,14479,14496,14551,14554,14571,14581,14613,14660,14764,14788,14822,14847,14849,14854,14864,14890,14908,14917,14936,14949,14989,14993,15019,15037,15057,15157,15163,15183,15198,15257,15307,15312,15362,15374,15392,15504,15532,15613,15631,15704,15707,15763,15776,15797,15863,15928,15991,15997,16003,16036,16054,16101,16104,16124,16152,16160,16225,16248,16296,16354,16394,16517,16522,16524,16548,16573,16581,16600,16603,16635,16640,16671,16677,16681,16685,16722,16728,16764,16790,16794,16815,16833,16836,16905,16932,16989,17064,17073,17077,17099,17111,17126,17171,17182,17208,17209,17243,17289,17313,17317,17345,17366,17393,17429,17436,17444,17534,17582,17653,17662,17721,17749,17756,17757,17797,17843,17869,17877,17880,17886,17907,17919,17922,17938,17951,17960,18022,18059,18060,18072,18086,18116,18160,18220,18274,18337,18356,18359,18394,18448,18468,18484,18531,18579,18586,18635,18647,18694,18710,18716,18726,18751,18771,18846,18881,18906,18924,18933,18935,18950,18965,18989,19045,19061,19084,19109,19175,19189,19227,19293,19301,19367,19379,19382,19394,19453,19459,19516,19543,19581,19606,19626,19654,19692,19728,19747,19782,19790,19805,19819,19821,19857,19876,19915,19968,19998,20011,20015,20056,20064,20124,20183,20217,20240,20247,20254,20264,20302,20319,20320,20323,20390,20393,20439,20448,20449,20522,20557,20563,20611,20639,20642,20652,20677,20709,20714,20741,20780,20844,20848,20872,20904,20946,20951,20979,20980,20992,21030,21032,21076,21093,21109,21142,21168,21183,21256,21258,21340,21354,21406,21468,21697,21727,21729,21761,21792,21893,21898,21937,21989,21992,21997,22031,22033,22069,22099,22114,22155,22204,22215,22237,22303,22344,22351,22387,22405,22417,22464,22470,22480,22505,22523,22559,22584,22587,22626,22661,22694,22812,22832,22917,22920,22964,22966,22986,22996,23015,23020,23051,23075,23100,23140,23147,23150,23174,23225,23243,23247,23276,23292,23323,23357,23358,23408,23412,23424,23434,23466,23493,23524,23597,23601,23623,23638,23665,23668,23686,23688,23771,23809,23833,23872,23878,23900,23920,23969,23982,24030,24031,24066,24124,24160,24186,24222,24305,24326,24327,24414,24433,24436,24539,24583,24646,24654,24692,24748,24821,24824,24852,24856]
				if(algo=='1'):
					print("ALGO 128")
					fpath='./static/data/'+plotdata['data_source']+'/algo1.pkl'
					with open(fpath, 'rb') as f:
					    data = pickle.load(f)
					scores=list(data.values())
					ids=list(data.keys())
					df=pd.read_csv('./static/data/'+plotdata['data_source']+"/algo1data.csv")
					ar=list(df['index'])
					df_overall['bindex']=df_dataset['index']
					arr=list(df_overall['bindex'])
					ind=[]
					for i in range(len(ar)):
						ind.append(arr.index(ar[i]))
					df['index']=ind
					ind=list(df.index)
					pred=[]
					for i in range(len(df)):
						y=ids.index(ind[i])
						x=scores[y]
						pred.append(x)
					df['SCORE']=pred
					df_bias_temp=pd.DataFrame()
					for ii in tqdm(range(len(models))):
						minfile='./static/data/'+plotdata['data_source']+'/'+'PLOTS-FULL.xlsx'
						df_temp=pd.read_excel(minfile,sheet_name=models[ii],engine='openpyxl')
						fdf_temp=pd.DataFrame()
						arr_temp=[]
						larr_temp=[]
						for i in tqdm(range(len(keeparr))):
							fdf_temp=fdf_temp.append(df_temp.loc[keeparr[i]])
						for i in tqdm(range(len(fdf_temp))):
							arr_temp.append(max(fdf_temp.iloc[i]['P1'],fdf_temp.iloc[i]['P2']))
							larr_temp.append(fdf_temp.iloc[i]['LABEL'])
						df_bias_temp[models[ii]]=arr_temp
						df_bias_temp['l-'+models[ii]]=larr_temp
					gold=df['label']
					print(df_bias_temp)	
					df_bias['sentence']=df['sentence']
					df_bias['label']=gold
					df_bias['SCORE']=df['SCORE']
					for ii in tqdm(range(len(models))):
						a1=[]
						a2=[]
						a3=[]
						for i in range(len(df_bias_temp)):
							if(df_bias_temp.iloc[i]['l-'+models[ii]]!=df_bias.iloc[i]['label']):
								a1.append(-1)
								a2.append(-1*df_bias_temp.iloc[i][models[ii]])
								a3.append(-1*df_bias.iloc[i]['SCORE'])
							else:
								a1.append(1)
								a2.append(1*df_bias_temp.iloc[i][models[ii]])
								a3.append(1*df_bias.iloc[i]['SCORE'])								
						df_bias[models[ii]+'-P']=a3
						df_bias[models[ii]]=a2
						df_bias[models[ii]+'-1']=a1
				else:
					print("4 Models")
					fpath='./static/data/'+plotdata['data_source']+'/algo2.pkl'
					with open(fpath, 'rb') as f:
						data = pickle.load(f)
					scores=list(data.values())
					ids=list(data.keys())
					df=pd.read_csv('./static/data/'+plotdata['data_source']+"/algo2data.csv")
					ar=list(df['index'])
					df_overall['bindex']=df_dataset['index']
					arr=list(df_overall['bindex'])
					ind=[]
					for i in range(len(ar)):
						ind.append(arr.index(ar[i]))
					df['index']=ind
					ind=list(df.index)
					pred=[]
					for i in range(len(df)):
						y=ids.index(ind[i])
						x=scores[y]
						pred.append(x)
					df['SCORE']=pred
					df_bias_temp=pd.DataFrame()
					for ii in tqdm(range(len(models))):
						minfile='./static/data/'+plotdata['data_source']+'/'+'PLOTS-FULL.xlsx'
						df_temp=pd.read_excel(minfile,sheet_name=models[ii],engine='openpyxl')
						fdf_temp=pd.DataFrame()
						arr_temp=[]
						larr_temp=[]
						for i in tqdm(range(len(keeparr))):
							fdf_temp=fdf_temp.append(df_temp.loc[keeparr[i]])
						for i in tqdm(range(len(fdf_temp))):
							arr_temp.append(max(fdf_temp.iloc[i]['P1'],fdf_temp.iloc[i]['P2']))
							larr_temp.append(fdf_temp.iloc[i]['LABEL'])
						df_bias_temp[models[ii]]=arr_temp
						df_bias_temp['l-'+models[ii]]=larr_temp
					gold=df['label']
					print(df_bias_temp)	
					df_bias['sentence']=df['sentence']
					df_bias['label']=gold
					df_bias['SCORE']=df['SCORE']
					for ii in tqdm(range(len(models))):
						a1=[]
						a2=[]
						a3=[]
						for i in range(len(df_bias_temp)):
							if(df_bias_temp.iloc[i]['l-'+models[ii]]!=df_bias.iloc[i]['label']):
								a1.append(-1)
								a2.append(-1*df_bias_temp.iloc[i][models[ii]])
								a3.append(-1*df_bias.iloc[i]['SCORE'])
							else:
								a1.append(1)
								a2.append(1*df_bias_temp.iloc[i][models[ii]])
								a3.append(1*df_bias.iloc[i]['SCORE'])								
						df_bias[models[ii]+'-P']=a3
						df_bias[models[ii]]=a2
						df_bias[models[ii]+'-1']=a1
			df_bias=df_bias.sort_values(by=['SCORE'],ascending=False)
			split_number=int(plotdata['split_number'])
			weighting=plotdata['weighting']
			valp=[]
			valn=[]
			if(weighting=='NN'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(split_number-pp)
			elif(weighting=='NZ'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append(0)
			elif(weighting=='ZN'):
				for pp in range(split_number):
					valp.append(0)
					valn.append(split_number-pp)
			elif(weighting=='NT'):
				for pp in range(split_number):
					valp.append(split_number-pp)
					valn.append((split_number-pp)/2)
			elif(weighting=='TN'):
				for pp in range(split_number):
					valp.append((split_number-pp)/2)
					valn.append(split_number-pp)			
			split_result=[]
			splitindex=[]
			split_type=plotdata['split_formation']
			for ii in range(split_number):
				splitindex.append([])
			if(split_type=='E'):
				split_result=np.array_split(range(len(df_bias)), split_number)
				for ii in range(len(split_result)):
						splitindex[ii].append(split_result[ii][0])
						splitindex[ii].append(split_result[ii][len(split_result[ii])-1])
			else:
				stsarr=list(df_bias['SCORE'])
				startsts=stsarr[0]
				endsts=stsarr[len(stsarr)-1]
				interval=(startsts-endsts)/split_number
				intervals=[]
				for ii in range(split_number):
					intervals.append(endsts+ii*interval)
				sindex=split_number-1
				splitindex[0].append(0)
				for ii in range(len(df_bias)):
					if(df_bias.iloc[ii]['SCORE']<intervals[sindex]):
						splitindex[split_number-sindex-1].append(ii-1)
						sindex=sindex-1
						splitindex[split_number-sindex-1].append(ii)
				splitindex[len(splitindex)-1].append(len(df_bias)-1)
			factor=plotdata['weight_factor']
			for m in range(len(models)):
				if(factor=='O'):
					df_bias[models[m]+'_factor']=df_bias[models[m]+'-1']
				elif(factor=='P'):
					df_bias[models[m]+'_factor']=df_bias[models[m]]
				elif(factor=='S'):
					df_bias[models[m]+'_factor']=df_bias[models[m]+'-P']
			wsbias=[]
			acc=[]
			splitwiserow=[]
			splitwisevalue=[]
			splitwisemodel=[]
			for calc in range(len(models)):
				sarr=[]
				sarrr=[]
				for calcc in range(len(splitindex)):
					sarr.append(list(df_bias[models[calc]+'_factor'][splitindex[calcc][0]:splitindex[calcc][1]]))
					sarrr.append(list(df_bias[models[calc]+'_factor'][splitindex[calcc][0]:splitindex[calcc][1]]))
					nr=0.0
					dr=0.0
				for x in range(len(sarr)):
					for xx in range(len(sarr[x])):
						if(sarr[x][xx]>0):
							sarr[x][xx]=sarr[x][xx]*valp[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valp[split_number-x-1]
						else:
							sarr[x][xx]=sarr[x][xx]*valn[split_number-x-1]
							sarrr[x][xx]=abs(sarrr[x][xx])*valn[split_number-x-1]						
					nr=nr+sum(sarr[x])
					dr=dr+sum(sarrr[x])
					if(sum(sarrr[x])==0):
						splitwisevalue.append(0)
					else:
						splitwisevalue.append(sum(sarr[x])/sum(sarrr[x]))
					splitwiserow.append(x+1)
					splitwisemodel.append(models[calc])
					print(sum(sarr[x]),sum(sarrr[x]),x+1,models[calc])
				wsbias.append(nr/dr*100)
				s=list(df_bias[models[calc]+'_factor'])
				acc.append(len(list(filter(lambda x:(x>=0),s)))*100/len(s))
			print(df_bias.head(20),valp,valn,splitindex,wsbias,acc,models)
			df_save=pd.DataFrame()
			split_column=[]
			for i in range(len(splitindex)):
				adding=splitindex[i][1]-splitindex[i][0]+1
				for j in range(adding):
					split_column.append(i+1)
			df_save['val']=df_bias['SCORE']
			for ii in range(len(models)):
				df_save[models[ii]+'_factor']=df_bias[models[ii]+'_factor']
			if(plotdata['data_source']=='SST-2'):
				df_save['ID']=df_bias['INDEX']
			else:
				df_save['ID']=df_bias.index
			df_save['sample']=df_bias['sentence']
			df_save['gold']=df_bias['label']
			df_save['val']=df_save['val'].round(decimals=4)
			df_save['split']=split_column
			if os.path.isdir('./static/data/plotting'):
				shutil.rmtree('./static/data/plotting')
			os.mkdir('./static/data/plotting')
			df_save.to_csv('./static/data/plotting/beeswarm-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save1=pd.DataFrame()
			df_save1['Split']=splitwiserow
			df_save1['Score']=splitwisevalue
			df_save1['Label']=splitwisemodel
			df_save1.to_csv('./static/data/plotting/splitwise-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			df_save2a=pd.DataFrame()
			df_save2a['Acc']=acc
			df_save2a['Score']=wsbias
			df_save2a['Model']=models
			df_save2a=df_save2a.sort_values(by=['Acc'],ascending=True)
			df_save2b=pd.DataFrame()
			df_save2b['Acc']=acc
			df_save2b['Score']=wsbias
			df_save2b['Model']=models
			df_save2b=df_save2b.sort_values(by=['Score'],ascending=True)
			df_save2=pd.DataFrame()
			df_save2['Acc']=df_save2a['Acc']
			df_save2['Score']=df_save2a['Score']
			df_save2['Model']=list(df_save2a['Model'])
			df_save2['WModel']=list(df_save2b['Model'])
			print(df_save2a['Model'],df_save2b['Model'],df_save2)
			df_save2.to_csv('./static/data/plotting/acc-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
			c=[[],[],[],[],[]]
			for i in range(split_number):				
				df_temp=df_save[df_save['split'] == i+1]
				for m in range(len(models)):
					df_tempp=df_temp[df_temp[models[m]+'_factor'] >= 0]
					c[0].append(models[m])
					c[1].append(len(df_temp))
					c[2].append(len(df_tempp))
					c[3].append(len(df_temp)-len(df_tempp))
					c[4].append(i+1)
			df_sun=pd.DataFrame()
			df_sun['Model']=c[0]
			df_sun['Split']=c[4]
			df_sun['Size']=c[1]
			df_sun['Correct']=c[2]
			df_sun['Incorrect']=c[3]
			df_sun.to_csv('./static/data/plotting/sun-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv')
		return './static/data/plotting/beeswarm-'+plotdata['data_source']+'-'+plotdata['metric_selected']+'-'+plotdata['split_formation']+'-'+plotdata['split_number']+'-'+plotdata['weighting']+'-'+plotdata['sts_percentage']+'-'+plotdata['weight_factor']+'-'+plotdata['bias_algo']+'.csv'