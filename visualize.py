from flask import Flask, render_template, request, jsonify
import json
import pymongo

DBName="NewsDB"
COLName="Articles"
data_file="jsondata.json"
jdata={}

def create_news_database(PMClient,collection_name):
	global DBName, jdata, data_file
	data_source=open(data_file,"r", encoding="utf-8")
	jdata=json.load(data_source)
	data_source.close()

	indx=1
	for item in jdata:
		item['_id']=indx
		indx = indx + 1
	
	newsdb=PMClient[DBName]
	newscol=newsdb[collection_name]
	x=newscol.insert_many(jdata)
	print("%d items inserted." % (len(x.inserted_ids)))

pmcl=pymongo.MongoClient("mongodb://localhost:27017/")
dblist=pmcl.list_database_names()
print(dblist)

if DBName in dblist:
	print("%s database already exists." % (DBName))
	newsdb=pmcl[DBName]
	newscol=newsdb[COLName]
	finds=newscol.find()

	jdata=[]
	for x in finds:
		jdata.append(x);

else:
	print("%s database does not exist. Creating ..." % (DBName))
	create_news_database(pmcl,COLName)



vis_app= Flask(__name__)



class DataStore():
	year=0
	topic="*"
	sector="*"
	region="*"
	pestle="*"
	source="*"
	swot="*"
	country="*"
	city="*"
	serial=1


data=DataStore()


@vis_app.route("/main",methods=["GET","POST"])


@vis_app.route("/",methods=["GET"])
def landingpage():
	return render_template("/visualnew/public/index.html",\
gyear=data.year,gtopic=data.topic,gsector=data.sector,\
gregion=data.region,gpestle=data.pestle,gsource=data.source,gswot=data.swot,\
gcountry=data.country,gcity=data.city,gserial=data.serial)

@vis_app.route("/",methods=["POST"])
def postingpage():
	global data
	val=request.form.get('param',0)
	print(val)
	if val == 'param_reset':
		print('RESET')
		data=DataStore()
	else :
		data.year=request.form.get('year',0)
		if data.year == "*":
			data.year=0
		data.topic=request.form.get('topic',"*")
		data.sector=request.form.get('sector',"*")
		data.region=request.form.get('region',"*")
		data.pestle=request.form.get('pestle',"*")
		data.source=request.form.get('source',"*")
		data.swot=request.form.get('swot',"*")
		data.country=request.form.get('country',"*")
		data.city=request.form.get('city',"*")
		data.serial=request.form.get('serial',0)
		if data.serial == "*":
			data.serial=0
		print(data.year)
		print(data.topic)
		print(data.sector)
		print(data.region)
		print(data.pestle)
		print(data.source)
		print(data.swot)
		print(data.country)
		print(data.city)
		print(data.serial)
	return render_template("/visualnew/public/index.html",\
gyear=data.year,gtopic=data.topic,gsector=data.sector,\
gregion=data.region,gpestle=data.pestle,gsource=data.source,gswot=data.swot,\
gcountry=data.country,gcity=data.city,gserial=data.serial)

@vis_app.route("/visualnew/src/d3.js",methods=["GET","POST"])
def D3Library():
	return render_template("/visualnew/src/d3.js")

@vis_app.route("/fetchdata",methods=["GET","POST"])
def sendjData():
    global jdata
    return jsonify(jdata)



if __name__ == "__main__":
    vis_app.run(debug=True)



