conn = new Mongo()
db = conn.getDB("VoiceImageDB");

//Lu jia zui
var LJZname = ["IMG1.JPG", "IMG2.JPG"]
var LJZLocation = [31.237185, 121.525490]
for(i = 0; i < LJZname.length; i++) {
	if(!db.voice_images.findOne({"image_name": LJZname[i]})) {
		db.voice_images.save({"user_id": "test", "image_name": LJZname[i], "location": {"longitude": LJZLocation[0], "latitude": LJZLocation[1]}, "desc":"", "processed": true, "tags": ["lujiazui","test"]});
		print("Record added as:" + LJZname[i]);
	}
}

//Tian an men
var TAMname = ["IMG3.JPG", "IMG4.JPG"]
var TAMLocation = [39.908722, 116.397499]
for(i = 0; i < TAMname.length; i++) {
	if(!db.voice_images.findOne({"image_name": TAMname[i]})) {
		db.voice_images.save({"user_id": "test", "image_name": TAMname[i], "location": {"longitude": TAMLocation[0], "latitude": TAMLocation[1]}, "desc":"", "processed": true, "tags": ["tiananmen","test"]});
		print("Record added as:" + TAMname[i]);
	}
}

//Bing ma yong
var BMYname = ["IMG5.JPG", "IMG6.JPG"]
var BMYLocation = [34.263161, 108.948021]
for(i = 0; i < BMYname.length; i++) {
	if(!db.voice_images.findOne({image_name: BMYname[i]})) {
		db.voice_images.save({"user_id": "test", "image_name": BMYname[i], "location": {"longitude": BMYLocation[0], "latitude": BMYLocation[1]}, "desc":"", "processed": true, "tags": ["bingmayong","test"]});
		print("Record added as:" + BMYname[i]);
	}
}

//Spring festival
var SFname = ["IMG7.JPG", "IMG8.JPG"]
var SFdate = ISODate("2015-02-19T09:01:17.171Z")
for(i = 0; i < SFname.length; i++) {
	if(!db.voice_images.findOne({image_name: SFname[i]})) {
		db.voice_images.save({"user_id": "test", "image_name": SFname[i], "time": SFdate, "desc":"", "processed": true, "tags": ["chunjie","test"]});
		print("Record added as:" + SFname[i]);
	}
}

//Summer
var SMname = ["IMG9.JPG", "IMG10.JPG"]
var SMdate = ISODate("2015-07-07T11:01:17.171Z")
for(i = 0; i < SMname.length; i++) {
	if(!db.voice_images.findOne({image_name: SMname[i]})) {
		db.voice_images.save({"user_id": "test", "image_name": SMname[i], "time": SMdate, "desc":"", "processed": true, "tags": ["xiatian","test"]});
		print("Record added as:" + SMname[i]);
	}
}
