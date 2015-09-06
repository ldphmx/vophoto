conn = new Mongo()
db = conn.getDB("VoiceImageDB");

//Lu jia zui
var LJZname = ["IMG1.JPG", "IMG2.JPG"]
var LJZLocation = [31.237185, 121.525490]
for(i = 0; i < LJZname.length; i++) {
	db.voice_images.save({"user_id":"test", "image_name": LJZname[i], "time": "", "location":{"longitude": LJZLocation[0], "latitude": LJZLocation[1] }, "desc":"", "processed": true, "tags":["lujiazui","test"]});
	print("Record added as:" + LJZname[i]);
}

//Tian an men
var TAMname = ["IMG3.JPG", "IMG4.JPG"]
var TAMLocation = [39.908722, 116.397499]
for(i = 0; i < TAMname.length; i++) {
	db.voice_images.save({"user_id":"test", "image_name": TAMname[i], "time": "", "location":{"longitude": TAMLocation[0], "latitude": TAMLocation[1] }, "desc":"", "processed": true, "tags":["tiananmen","test"]});
	print("Record added as:" + TAMname[i]);
}

//Bing ma yong
var BMYname = ["IMG5.JPG", "IMG6.JPG"]
var BMYLocation = [34.263161, 108.948021]
for(i = 0; i < BMYname.length; i++) {
	db.voice_images.save({"user_id":"test", "image_name": BMYname[i], "time": "", "location":{"longitude": BMYLocation[0], "latitude": BMYLocation[1] }, "desc":"", "processed": true, "tags":["bingmayong","test"]});
	print("Record added as:" + BMYname[i]);
}
