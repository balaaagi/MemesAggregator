
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var user = require('./routes/user');
var http = require('http');
var path = require('path');

//var mongo=require('mongodb');
var mongo=require('mongoskin');
//var db=monk('localhost:27017/mylinks');
var db=mongo.db("mongodb://localhost:27017/memesaggregate",{native_parser:true});

var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('your secret here'));
app.use(express.session());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', routes.index);
app.get('/users', user.list);
app.get('/helloworld',routes.helloworld);
app.get('/linklist',routes.linklist(db));
app.get('/newlink',routes.newlink);
app.post('/addlink',routes.addlink(db));
app.get('/showtags',routes.showtags(db));
app.get('/showmemes',routes.showmemes(db));
app.get('/newcategory',routes.newcategory);
app.post('/modifymeme',routes.modifymeme(db))
app.post('/addcategory',routes.addcategory(db))
app.get('/showcategory',routes.showcategory(db))


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
