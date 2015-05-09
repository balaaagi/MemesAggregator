import facebook
import requests
import urllib2
import json
import pymongo
from pymongo import MongoClient

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

def checkpostexists(post_id):
	return db.poststatistics.find({"post_id":post_id}).count()

def build_data_structure(post_data):
	
	# len(post_data['message'])
	datastructure={}
	data['post_message']=post_data['message']
	data['memes_url']=post_data['picture']
	data['hd_img_url']=post_data['link']
	data['post_id']=post_data['id']
	data['share_count']=post_data['shares']['count']
	data['category']='unassigned'
	data['tags']=[" "]
	stats['post_id']=post_data['id']
	stats['memes_share_count']=post_data['shares']['count']
	stats['memes_views_count']=0
	stats['memes_likes_count']=0
	datastructure['data']=data 
	datastructure['stats']=stats
	# print data
	return datastructure







configs=extract_config()

APP_SECRET =configs[0]
APP_ID =configs[1]


memes_pages=['kaatupoochi007']
graph_url="https://graph.facebook.com/"


# MongoDB Connection
client=MongoClient('localhost', 27017)
# Connecting to DataBase
db=client.memesaggregate


current_memes_page=graph_url + 'kaatupoochi007'

json_memes_page=render_to_json(current_memes_page)
page_data = (json_memes_page["id"], json_memes_page["likes"],
                     json_memes_page["talking_about_count"],
                     json_memes_page["username"])
# print page_data
# print('-----------')

#extract post data
post_url = create_post_url(current_memes_page, APP_ID, APP_SECRET)

json_postdata = render_to_json(post_url)



json_fbposts = json_postdata['data']


for post in json_fbposts:
	if post['type']=='photo':
		data={}
		stats={}
		post_url=create_single_post_url(graph_url+post['id'],APP_ID,APP_SECRET)
		post_data=render_to_json(post_url)
		posts_data=build_data_structure(post_data)
		if checkpostexists(post['id'])==0:
			db.posts.insert(posts_data['data'])
			db.poststatistics.insert(posts_data['stats']) 
		else:
			db.posts.update({"post_id":post[id]},{'$set':{"share_count":post_data['shares']['count']}})
			db.poststatistics.update({"post_id":post[id]},{'$set':{"memes_share_count":post_data['shares']['count']}})
			
		
		
		
		# db.posts.insert(build_data_structure_newpost(post_data)) 
			
		
		# print build_data_structure(post_data)

		
		# extract_hq_img_link(post_data['link'])

