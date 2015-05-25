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

def create_post_url(graph_url, APP_ID, APP_SECRET,since_date): 
    #create authenticated post URL
    post_args = "/posts/?fields=id,created_time,updated_time,type&limit=10&since="+ str(since_date) +"&key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args
    print post_url
    return post_url

def create_single_post_url(graph_url,APP_ID,APP_SECRET):
	single_post_args="?fields=shares,picture,link,message,full_picture&key=value&access_token=" + APP_ID + "|" + APP_SECRET
	single_post_url=graph_url + single_post_args
	return single_post_url

def extract_config():
	return file('config.txt').read().split(',')


def checkpostexists(post_id):
	return db.poststatistics.find({"post_id":post_id}).count()
def extractTime(page_name):
	return db.postutility.find({"page_name":page_name},{"_id":False,"latest_meme_time":True})

def build_data_structure(post_data):
	
	# len(post_data['message'])
	# datastructure={}
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
		
		data['memes_share_count']=post_data['shares']['count']
		data['memes_views_count']=0
		data['memes_likes_count']=0
		# datastructure['data']=data
		# datastructure['stats']=stats
	except KeyError:
		data['post_message']=" "
		data['post_id']=" "
		data['share_count']=" "
		data['category']='unassigned'
		data['tags']=[" "]
		data['title']=" "
		data["source"]=page_name
		data['memes_share_count']=0
		data['memes_views_count']=0
		data['memes_likes_count']=0

	
	# print data
	return data







configs=extract_config()

APP_SECRET =configs[0]
APP_ID =configs[1]


memes_pages=['kaatupoochi007']
graph_url="https://graph.facebook.com/"


# MongoDB Connection
client=MongoClient('labs.balaaagi.me', 27017)
# Connecting to DataBase
db=client.memesaggregate

page_name='memeschennai'
current_memes_page=graph_url + 'memeschennai'

json_memes_page=render_to_json(current_memes_page)
page_data = (json_memes_page["id"], json_memes_page["likes"],
                     json_memes_page["talking_about_count"],
                     json_memes_page["username"])
# print page_data
# print('-----------')

#extract post data
# extracted_time=extractTime(page_name)
for values in extractTime(page_name):
	extracted_time=values['latest_meme_time']

print extracted_time

post_url = create_post_url(current_memes_page, APP_ID, APP_SECRET,extracted_time.split(" ")[0])

json_postdata = render_to_json(post_url)



json_fbposts = json_postdata['data']
# complete_posts=[]
# count=0;
# while(True):
#     try:
#         for post in json_postdata['data']:
#         	count=count+1
#         	complete_posts.append(post)
        	
#         if(count>30):
#         	break
        	
#         # Attempt to make a request to the next page of data, if it exists.
#         json_postdata=requests.get(json_postdata['paging']['next']).json()
#     except KeyError:
#         # When there are no more pages (['paging']['next']), break from the
#         # loop and end the script.
#         break

# print complete_posts
latest_post_time=json_fbposts[0]['updated_time']
latest_post_time=latest_post_time[0:latest_post_time.index('+')]
latest_post_time=latest_post_time.replace('T',' ')
db.postutility.insert({"page_name":page_name,"latest_meme_time":latest_post_time});
for post in json_fbposts:
	if post['type']=='photo':
		data={}
		stats={}
		post_url=create_single_post_url(graph_url+post['id'],APP_ID,APP_SECRET)
		post_data=render_to_json(post_url)
		print post['id']
		posts_data=build_data_structure(post_data)
		print posts_data
		if checkpostexists(post['id'])==0:
			db.posts.insert(posts_data)
			# db.poststatistics.insert(posts_data['stats'])
			
		else:
			db.posts.update({"post_id":post['id']},{'$set':{'share_count':post_data['shares']['count']}})
			# db.poststatistics.update({"post_id":post['id']},{'$set':{'memes_share_count':post_data['shares']['count']}})
			
		
		
		
		
		

