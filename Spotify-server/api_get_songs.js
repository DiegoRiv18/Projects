const musicapp_db = require('./musicapp_db.js');

//
// Get's all the song names associated with a user
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

// Query the database to get all songs from a user
async function get_user_songs(userid) {
  // Modify SQL to select both songname and artistname
  const sql = 'SELECT songname, artistname FROM songs WHERE userid = ?';
  const results = await query_database(musicapp_db, sql, [userid]);
  // Map the results to include both songname and artistname
  return results.map(result => ({
      songname: result.songname,
      artistname: result.artistname
  }));
}

/**
 * Add a favorite song to the database.
 */
exports.get_songs = async (req, res) => {
    console.log("**Call to get /get_songs...");

  try {
    // Extract song data from request body
    const { userid } = req.body;

    // Validate input
    if (!userid) {
      return res.status(400).json({ success: false, message: "Missing userid." });
    }

    // Get all songs for the given user
    const songs = await get_user_songs(userid);

    // Respond with success
    return res.status(200).json({ success: true, songs: songs});
  } 
  catch (err) {
    console.error("**Error in /get_songs:", err.message);
    res.status(500).json({ success: false, message: "Internal server error." });
  }
};
