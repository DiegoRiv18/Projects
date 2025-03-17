const musicapp_db = require('./musicapp_db.js');

function query_database(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.query(sql, params, (err, results, _) => {
            if (err) {
                reject(err);
            } else {
                resolve(results);
            }
        });
    });
}

// Query the database to get all genres for a user
async function get_user_genres(userid) {
    const sql = 'SELECT genres FROM songs WHERE userid = ?'; // Modify as needed
    const results = await query_database(musicapp_db, sql, [userid]);
    return results.map(result => result.genres); // Extracting only the genres
}

// Endpoint to calculate genre statistics
// Endpoint to calculate genre statistics
exports.calc_genres = async (req, res) => {
    console.log("**Call to get /calc_genres...");

    try {
        const { userid } = req.body;

        // Get all genres for the given user
        const genres = await get_user_genres(userid);

        // Flatten genres into a single array
        let allGenres = genres
            .flatMap(genreStr => genreStr.split(",").map(genre => genre.trim()));

        // Count occurrences of each genre
        let genreCounts = allGenres.reduce((acc, genre) => {
            acc[genre] = (acc[genre] || 0) + 1;
            return acc;
        }, {});

        // Sort and extract top 5 genres
        let topGenres = Object.entries(genreCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([genre, count]) => ({ genre, count }));

        res.status(200).json({ success: true, genres: allGenres, topGenres });
    } catch (err) {
        console.error("**Error in /calc_genres:", err.message);
        res.status(500).json({ success: false, message: "Internal server error." });
    }
};

