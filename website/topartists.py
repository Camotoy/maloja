import urllib

		
def instructions(keys):
	from utilities import getArtistInfo
	from htmlgenerators import KeySplit
	from htmlmodules import module_artistcharts

	
	_, timekeys, _, amountkeys = KeySplit(keys)
	
	html_charts, rep = module_artistcharts(**amountkeys,**timekeys)
	
	if rep is not None:
		imgurl = getArtistInfo(rep).get("image")
	else:
		imgurl = ""
		
	pushresources = [{"file":imgurl,"type":"image"}] if imgurl.startswith("/") else []
	

	replace = {"KEY_TOPARTIST_IMAGEURL":imgurl,"KEY_ARTISTLIST":html_charts}

	return (replace,pushresources)
