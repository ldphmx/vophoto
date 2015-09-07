conn = new Mongo()
db = conn.getDB("VoiceImageDB");

var ex = "IMG_"
var suffix = '.JPG'
var user_id = "b42c916c-3b1e-4235-85b7-451aea401218"   //need modified

//Lu jia zui
var LJZbegin = 1   //need modified
var LJZlength = 10   //need modified
var LJZname = []
for(i = 0;i<LJZlength;i++){
	 var num = LJZbegin + i;
	 var s_num = num.toString();
	 var item = ex + s_num +suffix;
	 LJZname[i] = item;
    }
print(LJZname);
var LJZLocation = [31.237185, 121.525490]
var LJZTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < LJZname.length; i++) {
	if(!db.voice_images.findOne({"image_name": LJZname[i]})) {
		db.voice_images.save({"user_id": user_id, "image_name": LJZname[i], "time": LJZTime, "location": {"longitude": LJZLocation[0], "latitude": LJZLocation[1]}, "desc":"", "processed": true, "tags": ["lu-jia-zui","test"]});
		print("Record added as:" + LJZname[i]);
	}
}

//Tian an men
var TAMbegin = 1   //need modified
var TAMlength = 10   //need modified
var TAMname = []
for(i = 0;i<TAMlength;i++){
	 var num = TAMbegin + i;
	 var s_num = num.toString();
	 var item = ex + s_num +suffix;
	 TAMname[i] = item;
    }
print(TAMname);
var TAMLocation = [39.908722, 116.397499]
var TAMTime = ISODate("2014-08-14T09:30:17.171Z")
for(i = 0; i < TAMname.length; i++) {
	if(!db.voice_images.findOne({"image_name": TAMname[i]})) {
		db.voice_images.save({"user_id": user_id, "image_name": TAMname[i], "time": TAMTime, "location": {"longitude": TAMLocation[0], "latitude": TAMLocation[1]}, "desc":"", "processed": true, "tags": ["tian-an-men","test"]});
		print("Record added as:" + TAMname[i]);
	}
}

//Bing ma yong
var BMYbegin = 1   //need modified
var BMYlength = 10  //need modified
var BMYname = []
for(i = 0;i<BMYlength;i++){
	 var num = BMYbegin + i;
	 var s_num = num.toString();
	 var item = ex + s_num +suffix;
	 BMYname[i] = item;
	}
print(BMYname);
var BMYLocation = [34.263161, 108.948021]
var BMYTime = ISODate("2014-08-19T09:05:17.171Z")
for(i = 0; i < BMYname.length; i++) {
	if(!db.voice_images.findOne({image_name: BMYname[i]})) {
		db.voice_images.save({"user_id": user_id, "image_name": BMYname[i], "time": BMYTime, "location": {"longitude": BMYLocation[0], "latitude": BMYLocation[1]}, "desc":"", "processed": true, "tags": ["bing-ma-yong","test"]});
		print("Record added as:" + BMYname[i]);
	}
}

//Spring festival
var SFbegin = 1   //need modified
var SFlength = 10   //need modified
var SFname = []
for(i = 0;i<SFlength;i++){
	 var num = SFbegin + i;
	 var s_num = num.toString();
	 var item = ex + s_num +suffix;
	 SFname[i] = item;
    }
print(SFname);
var SFLocation = [30.123456, 120.789456]
var SFdate = ISODate("2015-02-19T09:01:17.171Z")
for(i = 0; i < SFname.length; i++) {
	if(!db.voice_images.findOne({image_name: SFname[i]})) {
		db.voice_images.save({"user_id": user_id, "image_name": SFname[i], "time": SFdate, "location": {"longitude": SFLocation[0], "latitude": SFLocation[1]}, "desc":"", "processed": true, "tags": ["chun-jie","test"]});
		print("Record added as:" + SFname[i]);
	}
}

//Summer
var SMbegin = 1   //need modified
var SMlength = 10   //need modified
var SMname = []
for(i = 0;i<SMlength;i++){
	 var num = SMbegin + i;
	 var s_num = num.toString();
	 var item = ex + s_num +suffix;
	 SMname[i] = item;
    }
print(SMname);
var SMLocation = [38.456123, 115.456123]
var SMdate = ISODate("2014-07-07T11:01:17.171Z")
for(i = 0; i < SMname.length; i++) {
	if(!db.voice_images.findOne({image_name: SMname[i]})) {
		db.voice_images.save({"user_id": user_id, "image_name": SMname[i], "time": SMdate, "location": {"longitude": SMLocation[0], "latitude": SMLocation[1]}, "desc":"", "processed": true, "tags": ["xia-tian","test"]});
		print("Record added as:" + SMname[i]);
	}
}
