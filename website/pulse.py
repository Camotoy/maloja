import urllib
import database

		
def instructions(keys):
	from utilities import getArtistInfo, getTrackInfo
	from htmlgenerators import getTimeDesc, artistLink, artistLinks, trackLink, scrobblesLink, keysToUrl, getRangeDesc, KeySplit
	from htmlmodules import module_pulse
	
	filterkeys, timekeys, delimitkeys, _ = KeySplit(keys)
	
	
	# describe the scope (and creating a key for the relevant artist or track)
	limitstring = ""
	#limitkey = {}
	if filterkeys.get("track") is not None:
		#limitkey["track"] = {"artists":keys.getall("artist"),"title":keys.get("title")}
		limitstring += "of " + trackLink(filterkeys["track"]) + " "
		limitstring += "by " + artistLinks(filterkeys["track"]["artists"])
	
	elif filterkeys.get("artist") is not None:
		#limitkey["artist"], limitkey["associated"] = keys.get("artist"), (keys.get("associated")!=None)
		limitstring += "of " + artistLink(filterkeys.get("artist"))
		if filterkeys.get("associated"):
			data = database.artistInfo(filterkeys["artist"])
			moreartists = data["associated"]
			if moreartists != []:
				limitstring += " <span class='extra'>including " + artistLinks(moreartists) + "</span>"
		
	
	# get image	
	if filterkeys.get("track") is not None:
		imgurl = getTrackInfo(filterkeys.get("track")["artists"],filterkeys.get("track")["title"]).get("image")
	elif filterkeys.get("artist") is not None:
		imgurl = getArtistInfo(keys.get("artist")).get("image")
	else:
		imgurl = ""
		
	pushresources = [{"file":imgurl,"type":"image"}] if imgurl.startswith("/") else []
	

	
	html_pulse = module_pulse(**filterkeys,**timekeys,**delimitkeys)
	
	replace = {"KEY_PULSE_TABLE":html_pulse,"KEY_IMAGEURL":imgurl,"KEY_LIMITS":limitstring}
	
	return (replace,pushresources)
		
