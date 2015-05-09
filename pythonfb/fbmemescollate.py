import facebook
import requests
import urllib2
import json

def render_to_json(graph_url):
    #render graph url call to JSON
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    
    return json_data

def create_post_url(graph_url, APP_ID, APP_SECRET): 
    #create authenticated post URL
    post_args = "/posts/?fields=id,created_time,updated_time,type&limit=10&key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args
 
    return post_url

def create_single_post_url(graph_url,APP_ID,APP_SECRET):
	single_post_args="?fields=shares,picture,link,message&key=value&access_token=" + APP_ID + "|" + APP_SECRET
	single_post_url=graph_url + single_post_args
	return single_post_url

def extract_config():
	return file('config.txt').read().split(',')

def extract_hq_img_link(post_link):
	page=urllib2.urlopen(post_link)
	page_source=page.read()

def build_data_structure(post_data):
	
	# len(post_data['message'])

	data['post_message']=post_data['message']
	data['memes_url']=post_data['picture']
	data['hd_img_url']=post_data['link']
	data['post_id']=post_data['id']
	data['share_count']=post_data['shares']['count']
	return data




configs=extract_config()

APP_SECRET =configs[0]
APP_ID =configs[1]


memes_pages=['kaatupoochi007']
graph_url="https://graph.facebook.com/"


current_memes_page=graph_url + 'kaatupoochi007'

json_memes_page=render_to_json(current_memes_page)
page_data = (json_memes_page["id"], json_memes_page["likes"],
                     json_memes_page["talking_about_count"],
                     json_memes_page["username"])
print page_data
print('-----------')

#extract post data
post_url = create_post_url(current_memes_page, APP_ID, APP_SECRET)

json_postdata = render_to_json(post_url)



json_fbposts = json_postdata['data']


for post in json_fbposts:
	if(post['type']=='photo'):
		data={}
		post_url=create_single_post_url(graph_url+post['id'],APP_ID,APP_SECRET)
		post_data=render_to_json(post_url)
		print build_data_structure(post_data)
		# extract_hq_img_link(post_data['link'])

