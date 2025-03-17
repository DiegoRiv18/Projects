const axios = require('axios');
const musicapp_db = require('./musicapp_db.js');

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

// Query the database to get all songs for a user
async function get_user_songs(userid) {
  const sql = 'SELECT songid FROM songs WHERE userid = ?';  // Modify as needed for your table structure
  const results = await query_database(musicapp_db, sql, [userid]);
  return results.map(result => result.songid);  // Extracting only the songid
}

// Get song duration from Spotify API
async function get_song_duration(songid, token) {
  try {
    // Make a request to the Spotify API for track details
    const url = `https://api.spotify.com/v1/tracks/${songid}`;
    const response = await axios.get(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    // The duration is provided in milliseconds
    const durationMs = response.data.duration_ms;
    return Math.floor(durationMs / 1000); // Convert to seconds
  } 
  catch (error) {
    console.error('Error fetching track from Spotify API:', error);
    throw error; // Re-throw to be caught in the calling function
  }
}

// Format duration in seconds to hours:minutes:seconds
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
  
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }

// Endpoint to calculate total time
exports.calc_time = async (req, res) => {
  console.log("**Call to post /calc_time...");

  try {
    const { token, userid } = req.body;

    // Get all song IDs for the given user
    const songIds = await get_user_songs(userid);

    // Calculate total duration
    let totalDuration = 0;

    for (let songid of songIds) {
        const duration = await get_song_duration(songid, token);
        totalDuration += duration;
      }

    // Format the total duration in hours:minutes:seconds
    const formattedDuration = formatDuration(totalDuration);

    console.log(`Total Duration (hours: minutes: seconds): ${formattedDuration}`);
    res.status(200).json({ success: true, total_duration: formattedDuration });
  } catch (err) {
    console.error("**Error in /calc_time:", err.message);
    res.status(500).json({ success: false, message: "Internal server error." });
  }
};
