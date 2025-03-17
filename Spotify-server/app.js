//
// Express js (and node.js) web service that interacts with 
// AWS RDS and Spotify API to provide clients data for building a 
// simple music library
//
// Authors:
//  Diego Riverea
//  Prof. Joe Hummel (initial template)
//  Northwestern University
//

const express = require('express');
const app = express();
const config = require('./config.js');

const musicapp_db = require('./musicapp_db.js')

// support larger image uploads/downloads:
app.use(express.json({ strict: false, limit: "50mb" }));

var startTime;

//
// main():
//
app.listen(config.service_port, () => {
  startTime = Date.now();
  console.log('**Web service running, listening on port', config.service_port);
  //
  // Configure AWS to use our config file:
  //
  process.env.AWS_SHARED_CREDENTIALS_FILE = config.musicapp_config;
});

//
// request for default page /
//
app.get('/', (req, res) => {
  try {
    console.log("**Call to /...");
    
    let uptime = Math.round((Date.now() - startTime) / 1000);

    res.json({
      "status": "running",
      "uptime-in-secs": uptime,
      "dbConnection": musicapp_db.state
    });
  }
  catch(err) {
    console.log("**Error in /");
    console.log(err.message);

    res.status(500).json(err.message);
  }
});

//
// web service functions (API):
//
let recommendations = require('./api_recommendations.js');
let user = require('./api_new_user.js');
let sign_in = require('./api_sign_in.js');
let find_song = require('./api_find_song.js')
let add_song = require('./api_add_song.js')
let calc_time = require('./api_calc_time.js')
let get_songs = require('./api_get_songs.js')
let delete_song = require('./api_delete_song.js')
let calc_genres = require('./api_calc_genres.js')


app.get('/recommendations', recommendations.get_recommendations);
app.put('/new_user', user.put_user);
app.post('/signin', sign_in.sign_in);
app.post('/search_song', find_song.search_song)
app.post('/add_song', add_song.add_song)
app.get('/calc_time', calc_time.calc_time)
app.get('/get_songs', get_songs.get_songs)
app.delete('/delete_song', delete_song.delete_song)
app.get('/calc_genres',calc_genres.calc_genres)
