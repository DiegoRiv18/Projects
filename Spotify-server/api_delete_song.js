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

/**
 * Add a favorite song to the database.
 */
exports.delete_song = async (req, res) => {
    console.log("**Call to post /delete_song...");

  try {
    // Extract song data from request body
    const { userid, songname, artistname } = req.body;

    // Validate input
    if (!userid || !songname || !artistname) {
      return res.status(400).json({ success: false, message: "Missing arguments." });
    }

    const sql = 'DELETE FROM songs WHERE userid = ? AND songname = ? AND artistname = ?';
    const results = await query_database(musicapp_db, sql, [userid, songname, artistname]);

    if (results.affectedRows === 1) {
        return res.status(200).json({
          success: true, message: "Successful deletion"
        });
      }
    else {
        return res.status(400).json({
            success: false, message: "Song not in favorites!"
          });
    }
  } 
  catch (err) {
    console.error("**Error in /delete_song:", err.message);
    res.status(500).json({ success: false, message: "Internal server error." });
  }
};
