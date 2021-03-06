
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'My Links' });
};

exports.helloworld =function(req,res){
	res.render('helloworld',{title:'Hello, World!'});
};

exports.linklist=function(db){
	return function(req,res){
/*        db.collection('links').find({},{},function(err,result){
            res.render('linklist',
                {"linklist":result});
        });*/
		//var collection=db.get('links');
		db.collection('links').find().toArray(function(e,docs){
			res.render('linklist',{
				linklist:docs
			});

		});

	};
};

exports.showmemes=function(db){
    return function(req,res){
        //db.collection('posts').find({$where:"(this.category.length == 1)"}).toArray(function(e,docs){
          db.collection('posts').find({category:"unassigned"}).toArray(function(e,docs){  
            if(!e){
                db.collection('categories').find().toArray(function(err,d){
                    
                        var memesData = {};
                        memesData.memes = docs || [];
                        memesData.categories = d || [];
                        
                       res.render('showmemes',{ 
                        showmemes:memesData

                        
                    });
                });

            }else{
                console.log(e);
                res.send("Failed! Please check Console errors");
            }
            
            // res.send(docs);
        });
    }
}



exports.newuser=function(req,res){
	res.render('newuser',{title: 'New User'});
};

exports.newlink=function(req,res){
    res.render('newlink',{title:'Add New Link'});
};

exports.showtags=function(db){
    return function(req,res){
        db.collection('links').distinct('tag',function(err,items){
            res.json(items);
        })
    }

};

exports.newcategory=function(req,res){
    res.render('addcategory',{title:'Add New Category'})

}

exports.addcategory=function(db){
    return function(req,res){
        var newcategory=req.body.newcategory;
        db.collection('categories').insert({
            "category_name":newcategory
        },function(err,doc){
            if(err){
                res.send("Something went wrong");
            }else{
                res.location("/showcategory");
                res.redirect("showcategory");
            }
        });
    }
}



exports.modifymeme=function(db){
    return function(req,res){
        console.log("comgin");
        var tags=[];
        var deletepost=req.body.deletepost;
        var id=req.body.id;
        console.log(req.body.deletepost);
        if(deletepost=="on"){
                db.collection('posts').remove({
                    "post_id":id},function(err,doc){
                        if(err){
                            res.send("There was some problem during insertions of linkes");
                        }
                        else{
                            db.collection('poststatistics').remove({
                            "post_id":id},function(err,doc){
                            if(err){
                                res.send("There was some problem during insertions of linkes");
                            }
                            else{
                            
                            res.location("/showmemes");
                            res.redirect("showmemes");
                            } 
                            }

                            );
                            
                        } 
                    }

                );

        }else{
        tags=req.body.tags.split(",");
        var category=req.body.memescategory;
        var memestitle=req.body.title;
        //console.log(memestitle);
        console.log(tags);
        console.log(category);
        console.log(id);
        if(tags.length==0)
            category='unassigned';
        db.collection('posts').update({
            "post_id":id},{$set:{
            "tags":tags,
            "category":category,
            "title":memestitle}

        },function(err,doc){
            if(err){
                res.send("There was some problem during insertions of linkes");
            }
           else{
                res.location("/showmemes");
                res.redirect("showmemes");
           } 
        });
    }


    }
}

exports.showcategory=function(db){
    return function(req,res){
        db.collection('categories').find().toArray(function(e,docs){
            res.render('showcategories',{
                showcategories:docs
            });
            // res.send(docs);
        });
    }
}

exports.addlink=function(db){
    return function(req,res){
        var url=req.body.link;
        var tags=[];
        tags=req.body.tags.split(",");

        //var collection=db.get('links');

        db.collection('links').insert({
            "link":url,
            "tag":tags
        },function(err,doc){
            if(err){
                res.send("There was some problem during insertions of linkes");
            }
           else{
                res.location("/linklist");
                res.redirect("linklist");
           } 
        });
    }
}

exports.sampleapi=function(db){
    return function(req,res){
        db.collection('posts').find().limit(50).toArray(function(e,docs){
            var memes={};
            if(!e){
                db.collection('poststatistics').find().limit(50).toArray(function(err,doc){
                    if(!err){
                        memes.posts=docs || [];
                        memes.stats=doc || [];
                        res.send(memes);
                    }

                });

            }
            
            // res.send(docs);
            
        });
    }
}


exports.adduser = function(db) {
    return function(req, res) {

        // Get our form values. These rely on the "name" attributes
        var userName = req.body.username;
        var userEmail = req.body.useremail;


        // Set our collection
        var collection = db.get('usercollection');

        // Submit to the DB
        collection.insert({
            "username" : userName,
            "email" : userEmail
        }, function (err, doc) {
            if (err) {
                // If it failed, return error
                res.send("There was a problem adding the information to the database.");
            }
            else {
                // If it worked, set the header so the address bar doesn't still say /adduser
                res.location("/userlist");
                // And forward to success page
                res.redirect("userlist");
            }
        });

    }
}
