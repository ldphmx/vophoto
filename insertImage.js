conn = new Mongo()
db = conn.getDB("VoiceImageDB");

//Lu jia zui
var LJZname = ["IMG_1356.JPG", "IMG_1357.JPG","IMG_1358.JPG","IMG_1359.JPG","IMG_1360.JPG","IMG_1361.JPG","IMG_1362.JPG","IMG_1363.JPG","IMG_1364.JPG","IMG_1365.JPG","IMG_1366.JPG"]
var LJZLocation = [31.237185, 121.525490]
var LJZTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < LJZname.length; i++) {
	if(!db.voice_images.findOne({"image_name": LJZname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": LJZname[i], "time": LJZTime[i], "location": {"longitude": LJZLocation[0], "latitude": LJZLocation[1]}, "desc":"", "processed": true, "tags": ["lu-jia-zui","test"]});
		print("Record added as:" + LJZname[i]);
	}
}

//Tian an men
var TAMname = ["IMG_1338.JPG", "IMG_1339.JPG","IMG_1340.JPG","IMG_1341.JPG","IMG_1342.JPG","IMG_1343.JPG","IMG_1344.JPG","IMG_1345.JPG","IMG_1346.JPG"]
var TAMLocation = [39.908722, 116.397499]
var TAMTime = ISODate("2014-08-14T09:30:17.171Z")
for(i = 0; i < TAMname.length; i++) {
	if(!db.voice_images.findOne({"image_name": TAMname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": TAMname[i], "time": TAMTime[i], "location": {"longitude": TAMLocation[0], "latitude": TAMLocation[1]}, "desc":"", "processed": true, "tags": ["tian-an-men","test"]});
		print("Record added as:" + TAMname[i]);
	}
}

//Bing ma yong
var BMYname = ["IMG_1367.JPG", "IMG_1368.JPG","IMG_1369.JPG","IMG_1370.JPG","IMG_1371.JPG","IMG_1372.JPG","IMG_1373.JPG","IMG_1374.JPG","IMG_1375.JPG","IMG_1376.JPG","IMG_1377.JPG","IMG_1378.JPG","IMG_1379.JPG"]
var BMYLocation = [34.263161, 108.948021]
var BMYTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < BMYname.length; i++) {
	if(!db.voice_images.findOne({image_name: BMYname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": BMYname[i], "time": BMYTime[i], "location": {"longitude": BMYLocation[0], "latitude": BMYLocation[1]}, "desc":"", "processed": true, "tags": ["bing-ma-yong","test"]});
		print("Record added as:" + BMYname[i]);
	}
}

//Spring festival
var SFname = ["IMG_1347.JPG", "IMG_1348.JPG","IMG_1349.JPG","IMG_1350.JPG","IMG_1351.JPG","IMG_1352.JPG","IMG_1353.JPG","IMG_1354.JPG","IMG_1355.JPG"]
var SFLocation = [30.123456, 120.789456]
var SFdate = ISODate("2015-02-19T09:01:17.171Z")
for(i = 0; i < SFname.length; i++) {
	if(!db.voice_images.findOne({image_name: SFname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": SFname[i], "time": SFdate, "location": {"longitude": SFLocation[0], "latitude": SFLocation[1]}, "desc":"", "processed": true, "tags": ["chun-jie","test"]});
		print("Record added as:" + SFname[i]);
	}
}

//Summer
var SMname = ["IMG_1330.JPG", "IMG_1331.JPG","IMG_1332.JPG","IMG_1333.JPG","IMG_1334.JPG","IMG_1335.JPG","IMG_1336.JPG"]
var SMLocation = [38.456123, 115.456123]
var SMdate = ISODate("2014-07-07T11:01:17.171Z")
for(i = 0; i < SMname.length; i++) {
	if(!db.voice_images.findOne({image_name: SMname[i]})) {
		db.voice_images.save({"user_id": "b42c916c-3b1e-4235-85b7-451aea401218", "image_name": SMname[i], "time": SMdate, "location": {"longitude": SMLocation[0], "latitude": SMLocation[1]}, "desc":"", "processed": true, "tags": ["xia-tian","test"]});
		print("Record added as:" + SMname[i]);
	}
}