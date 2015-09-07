conn = new Mongo()
db = conn.getDB("VoiceImageDB");

//Lu jia zui
var ex = 'IMG_'
var suffix = '.JPG'
var begin = 1   #need modified
var length = 10   #need modified
var LJZname = []
for i in range(length):
    num = begin + i
    item = ex + str(num) +suffix
    LJZname.append(item)
print(LJZname)
var LJZLocation = [31.237185, 121.525490]
var LJZTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < LJZname.length; i++) {
	if(!db.voice_images.findOne({"image_name": LJZname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": LJZname[i], "time": LJZTime, "location": {"longitude": LJZLocation[0], "latitude": LJZLocation[1]}, "desc":"", "processed": true, "tags": ["lu-jia-zui","test"]});
		print("Record added as:" + LJZname[i]);
	}
}

//Tian an men
var ex = 'IMG_'
var suffix = '.JPG'
var begin = 1   #need modified
var length = 10   #need modified
var TAMname = []
for i in range(length):
    num = begin + i
    item = ex + str(num) +suffix
    TAMname.append(item)
print(TAMname)
var TAMLocation = [39.908722, 116.397499]
var TAMTime = ISODate("2014-08-14T09:30:17.171Z")
for(i = 0; i < TAMname.length; i++) {
	if(!db.voice_images.findOne({"image_name": TAMname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": TAMname[i], "time": TAMTime, "location": {"longitude": TAMLocation[0], "latitude": TAMLocation[1]}, "desc":"", "processed": true, "tags": ["tian-an-men","test"]});
		print("Record added as:" + TAMname[i]);
	}
}

//Bing ma yong
var ex = 'IMG_'
var suffix = '.JPG'
var begin = 1   #need modified 
var length = 10   #need modified
var BMYname = []
for i in range(length):
    num = begin + i
    item = ex + str(num) +suffix
    BMYname.append(item)
print(BMYname)
var BMYLocation = [34.263161, 108.948021]
var BMYTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < BMYname.length; i++) {
	if(!db.voice_images.findOne({image_name: BMYname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": BMYname[i], "time": BMYTime, "location": {"longitude": BMYLocation[0], "latitude": BMYLocation[1]}, "desc":"", "processed": true, "tags": ["bing-ma-yong","test"]});
		print("Record added as:" + BMYname[i]);
	}
}

//Spring festival
var ex = 'IMG_'
var suffix = '.JPG'
var begin = 1   #need modified 
var length = 10   #need modified
var SFname = []
for i in range(length):
    num = begin + i
    item = ex + str(num) +suffix
    SFname.append(item)
print(SFname)
var SFLocation = [30.123456, 120.789456]
var SFdate = ISODate("2015-02-19T09:01:17.171Z")
for(i = 0; i < SFname.length; i++) {
	if(!db.voice_images.findOne({image_name: SFname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": SFname[i], "time": SFdate, "location": {"longitude": SFLocation[0], "latitude": SFLocation[1]}, "desc":"", "processed": true, "tags": ["chun-jie","test"]});
		print("Record added as:" + SFname[i]);
	}
}

//Summer
var ex = 'IMG_'
var suffix = '.JPG'
var begin = 1   #need modified 
var length = 10   #need modified
var SMname = []
for i in range(length):
    num = begin + i
    item = ex + str(num) +suffix
    SMname.append(item)
print(SMname)
var SMLocation = [38.456123, 115.456123]
var SMdate = ISODate("2014-07-07T11:01:17.171Z")
for(i = 0; i < SMname.length; i++) {
	if(!db.voice_images.findOne({image_name: SMname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": SMname[i], "time": SMdate, "location": {"longitude": SMLocation[0], "latitude": SMLocation[1]}, "desc":"", "processed": true, "tags": ["xia-tian","test"]});
		print("Record added as:" + SMname[i]);
	}
}