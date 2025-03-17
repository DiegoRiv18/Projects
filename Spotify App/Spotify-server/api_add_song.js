const musicapp_db = require('./musicapp_db.js');

//
// Adds a song's info into the songs table for each user
//

function query_database(db, sql, params = []) {
    return new Promise((resolve, reject) => {
      try {
        db.query(sql, params, (err, results, _) => {
          if (err) {
            reject(err);
          } else {
            resolve(results);
          }
        });
      } catch (err) {
        reject(err);
      }
    });
  }


/**
 * Add a favorite song to the database.
 */
exports.add_song = async (req, res) => {
    console.log("**Call to post /add_song...");

  try {
    // Extract song data from request body
    const { songid, userid, songname, artistname, genres } = req.body;
    console.log("Song details:")
    console.log(req.body)

    // Validate input
    if (!songid || !userid || !songname || !artistname || !genres) {
      return res.status(400).json({ success: false, message: "Missing required fields." });
    }

    // Check if the song already exists in the database
    sql = `SELECT songid FROM songs WHERE songid = ?`
    let result = await query_database(musicapp_db, sql, [songid]);
    if (result.length > 0) {
      return res.status(400).json({ success: false, message: "Song is already in favorites." });
    }

    // Insert song data into the songs table
    sql = `INSERT INTO songs (songid, userid, songname, artistname, genres) VALUES (?, ?, ?, ?, ?)`;
    await query_database(musicapp_db, sql, [songid, userid, songname, artistname, genres.join(', ')]);

    // Respond with success
    return res.status(200).json({ success: true, message: "Song added to favorites." });
  } 
  catch (err) {
    console.error("**Error in /favorites/add:", err.message);
    res.status(500).json({ success: false, message: "Internal server error." });
  }
};
