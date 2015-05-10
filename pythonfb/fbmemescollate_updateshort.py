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
    post_args = "/posts/?fields=id,created_time,updated_time,type&limit=100&key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args
 
    return post_url

def create_single_post_url(graph_url,APP_ID,APP_SECRET):
	single_post_args="?fields=shares,picture,link,message,full_picture&key=value&access_token=" + APP_ID + "|" + APP_SECRET
	single_post_url=graph_url + single_post_args
	return single_post_url

def extract_config():
	return file('config.txt').read().split(',')

def extract_hq_img_link(post_link):
	page=urllib2.urlopen(post_link)
	page_source=page.read()
	fbimage="fbPhotoImage"
	firstindex=page_source.index(fbimage)+len("fbPhotoImage")
	print fbimage
	# return page_source[page_source.index(fbimage)+len("fbPhotoImage")+5:page_source.index("alt",page_source.index(fbPhotoImage)+len("fbPhotoImage"))-1]
	return page_source[page_source.index(fbimage,firstindex)+len("fbPhotoImage img")+5+len("fbPhotoImage src="):page_source.index("alt",page_source.index(fbimage,firstindex)+len("fbPhotoImage img")+5+len("fbPhotoImage src="))	]
# <img class="fbPhotoImage img" id="fbPhotoImage" src="https://scontent-ams.xx.fbcdn.net/hphotos-xtp1/v/t1.0-9/11061958_981270221913237_3655352908611889968_n.jpg?oh=b1b30095a52bc058d739204db3063671&amp;oe=55C4EAEE" alt="">
# https://scontent-ams.xx.fbcdn.net/hphotos-xtp1/v/t1.0-9/11061958_981270221913237_3655352908611889968_n.jpg?oh=b1b30095a52bc058d739204db3063671&amp;oe=55C4EAEE
# https://scontent-sin.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11193244_980789221961337_2441215843286533284_n.jpg?oh=ed0594cc3a62c5cfb5b76a39ddfa4da9&amp;oe=55D2B472 

def checkpostexists(post_id):
	return db.poststatistics.find({"post_id":post_id}).count()

def build_data_structure(post_data):
	
	# len(post_data['message'])
	datastructure={}
	try:
		data['post_message']=post_data['message']
		data['memes_url']=post_data['picture']
		data['hd_img_url']=post_data['full_picture']
		data['post_id']=post_data['id']
		data['share_count']=post_data['shares']['count']
		data['category']='unassigned'
		data['tags']=[" "]
		data['title']=" "
		data["source"]=page_name
		stats['post_id']=post_data['id']
		stats['memes_share_count']=post_data['shares']['count']
		stats['memes_views_count']=0
		stats['memes_likes_count']=0
		datastructure['data']=data
		datastructure['stats']=stats
	except KeyError:
		data['post_message']=" "
		data['post_id']=" "
		data['share_count']=" "
		data['category']='unassigned'
		data['tags']=[" "]
		data['title']=" "
		data["source"]=page_name
		stats['post_id']=post_data['id']
		stats['memes_share_count']=0
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

page_name='kaatupoochi007'
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
complete_posts=[]
count=0;
while(True):
    try:
        for post in json_postdata['data']:
        	count=count+1
        	complete_posts.append(post)
        	
        if(count>30):
        	break
        	
        # Attempt to make a request to the next page of data, if it exists.
        json_postdata=requests.get(json_postdata['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break

# print complete_posts

for post in complete_posts:
	if post['type']=='photo':
		data={}
		stats={}
		post_url=create_single_post_url(graph_url+post['id'],APP_ID,APP_SECRET)
		post_data=render_to_json(post_url)
		print post['id']
		posts_data=build_data_structure(post_data)
		print post['updated_time']
		if checkpostexists(post['id'])==0:
			db.posts.insert(posts_data['data'])
			db.poststatistics.insert(posts_data['stats'])
		else:
			db.posts.update({"post_id":post['id']},{'$set':{'share_count':post_data['shares']['count']}})
			db.poststatistics.update({"post_id":post['id']},{'$set':{'memes_share_count':post_data['shares']['count']}})
			
		
		
		
		
		

