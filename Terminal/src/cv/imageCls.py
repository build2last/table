import base64
import time
from urllib import request
from urllib import parse
import json
import conf

dish_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish"
general_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"


def add_ac_key(url):
	if url.endswith(("dish", "advanced_general")):
		return url + "?access_token=" + conf.ACCESS_KEY


def request_api(api_url, img_file):
	if isinstance(img_file, str):
		f = open(img_file, 'rb')
		img = base64.b64encode(f.read())
	else:
		img = img_file
	params = {"image":img, "top_num":5}
	params = parse.urlencode(params).encode("utf-8")
	req = request.Request(url=api_url, data=params)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	resp = request.urlopen(req)
	content = resp.read()
	if content:
		try:
			json_obj = json.loads(content)
			return json_obj["result"]
		except Exception as E:
			print(E)
			print(content)
			return ""


def what_is_img(img):
	api_url = add_ac_key(general_url)
	tags = request_api(api_url, img)
	return tags[0]["score"], tags[0]["keyword"]


def query_img(img):
	dish_info = request_api(add_ac_key(dish_url), img)
	tag_info = request_api(add_ac_key(general_url), img)
	return {
		"tid":conf.tid, "time":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())), 
		"dish":dish_info, "tag":tag_info}


def test():
	api_url = add_ac_key(general_url)
	img_file_path = "img/icecream.jpg"
	print(query_img(img_file_path))


if __name__ == '__main__':
	test()