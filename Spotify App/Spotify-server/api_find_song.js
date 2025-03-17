const axios = require('axios');

// Spotify API Base URLs
const SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search";
const SPOTIFY_ARTIST_URL = "https://api.spotify.com/v1/artists";

exports.search_song = async (req, res) => {
  console.log("**Call to POST /search_song...");

  try {
    // Extract data from the request body
    const { token, query } = req.body;

    // If token or query is missing
    if (!token || !query) {
      return res.status(400).json({ success: false, message: "Missing required parameters." });
    }

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    // Prepare query parameters for the Spotify API request
    const params = {
      q: query, // The search query
      type: 'track', // Search for tracks
      limit: 10, // Limit the results to 10
    };

    console.log("Searching Spotify with query:", query);

    // Make a GET request to the Spotify API
    const response = await axios.get(SPOTIFY_SEARCH_URL, { headers, params });

    if (response.status !== 200) {
      return res.status(response.status).json({
        success: false,
        message: response.data.error.message || "Spotify API error",
      });
    }

    // Map the response data to simplify the song search format
    const songs = await Promise.all(
      response.data.tracks.items.map(async (track) => {
        const artistIds = track.artists.map(artist => artist.id);

        // Fetch genres for each artist
        const artistGenres = await Promise.all(
          artistIds.map(async (artistId) => {
            const artistResponse = await axios.get(`${SPOTIFY_ARTIST_URL}/${artistId}`, { headers });
            return artistResponse.data.genres; // Return the genres for the artist
          })
        );

        // Flatten genres and remove duplicates
        const uniqueGenres = [...new Set(artistGenres.flat())];

        return {
          id: track.id,
          name: track.name,
          artists: track.artists.map(artist => artist.name).join(', '),
          genres: uniqueGenres, // Include genres
        };
      })
    );

    // Send the formatted search results back to the client
    return res.status(200).json({ success: true, songs });
  } 
  catch (err) {
    console.error("Error in /search_song:", err.message);
    return res.status(500).json({ success: false, message: err.message });
  }
};
