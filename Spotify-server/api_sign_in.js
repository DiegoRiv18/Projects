const musicapp_db = require('./musicapp_db.js')
const crypto = require('crypto');

function query_database(db, sql, params = [])
{
  return new Promise((resolve, reject) => {
    try 
    {
      //
      // execute the query, and when we get the callback from
      // the database server, either resolve with the results
      // or error with the error object
      //
      db.query(sql, params, (err, results, _) => {
        if (err) {
          reject(err);
        }
        else {
          resolve(results);
        }
      });
    }
    catch (err) {
      reject(err);
    }
  });
}

// Function to hash a password using crypto's createHash
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

exports.sign_in = async (req, res) => {
  console.log("**Call to POST /signin...");

  try {
    let data = req.body;
    let { username, password } = data;
    console.log(data)

    console.log("Sign-in attempt for username:", username);

    // Query the database for the user by username
    let sql = 'SELECT password FROM users WHERE username = ?';
    let result = await query_database(musicapp_db, sql, [username]);

    if (result.length === 0) {
      console.log("User not found:", username);
      return res.status(200).json({ success: false });
    }

    // Extract the hashed password from the result
    let storedHashedPassword = result[0].password;

    // Hash the input password and compare
    let inputHashedPassword = hashPassword(password);

    if (inputHashedPassword === storedHashedPassword) {
      console.log("Sign-in successful for:", username);
      sql = 'SELECT userid FROM users WHERE password = ?';
      let results = await query_database(musicapp_db, sql, [inputHashedPassword]);
      
      let userid = results.length ? results[0].userid : null;

      if (!userid) {
        return res.status(500).json({ message: "Unable to fetch userid." });
      }
      
      return res.status(200).json({ message: "success", userid: userid }); // Send userid as a plain value
    }
    else {
      return res.status(200).json({ message: `"Invalid password for ${username}` });
    }
  } catch (err) {
    console.log("**Error in /signin");
    console.log(err.message);

    res.status(500).json({
      message: err.message,
    });
  }
};
