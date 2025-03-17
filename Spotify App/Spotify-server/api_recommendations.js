const axios = require('axios');

// Spotify API Base URL
const SPOTIFY_API_URL = "https://api.spotify.com/v1/recommendations";

exports.get_recommendations = async (req, res) => {
  console.log("**Call to POST /recommendations...");

  try {
    // Extract data from the request body
    const { token, genres, artists } = req.body;

    //If token or inputs failed to send
    if (!token || (!genres && !artists)) {
      return res.status(400).json({ success: false, message: "Missing required parameters." });
    }

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    // Prepare query parameters for the Spotify API request
    const params = {
      seed_genres: genres ? genres.join(',') : '',
      seed_artists: artists ? artists.join(',') : '',
      limit: 10,
    };

    console.log("Requesting Spotify recommendations with params:", params);

    // Make a GET request to the Spotify API
    const response = await axios.get(SPOTIFY_API_URL, { headers, params });

    if (response.status !== 200) {
      return res.status(response.status).json({
        success: false,
        message: response.data.error.message || "Spotify API error",
      });
    }

    // Map the response data to simplify the recommendations format
    const recommendations = response.data.tracks.map(track => ({
      name: track.name,
      artists: track.artists.map(artist => artist.name),
      url: track.external_urls.spotify,
    }));

    // Send the formatted recommendations back to the client
    return res.status(200).json({ success: true, recommendations });
  } 
  catch (err) {
    console.error("Error in /recommendations:", err.message);
    return res.status(500).json({ success: false, message: err.message });
  }
};
