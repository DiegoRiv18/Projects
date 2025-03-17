//
// app.put('/user', async (req, res) => {...});
//
// Inserts a new user into the database, or if the
// user already exists (based on email) then the
// user's data is updated (name and bucket folder).
// Returns the user's userid in the database.
//
const musicapp_db = require('./musicapp_db.js');
const crypto = require('crypto');

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

// Function to hash a password using crypto's createHash
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

exports.put_user = async (req, res) => {
  console.log("**Call to put /user...");

  try {
    let data = req.body;
    let { email, lastname, firstname, username, password } = data;

    console.log({ email, lastname, firstname, username, password });

    // Check if the email already exists
    let sql = 'SELECT userid FROM users WHERE email = ?';
    let result = await query_database(musicapp_db, sql, [email]);
    console.log(result)

    const hashedPassword = hashPassword(password);

    if (result.length === 0) {
      // Insert a new user
      console.log("Inserting new user")
      sql = `INSERT INTO users (email, lastname, firstname, username, password)
             VALUES (?, ?, ?, ?, ?)`;

      result = await query_database(musicapp_db, sql, [email, lastname, firstname, username, hashedPassword]);

      if (result.affectedRows === 1) {
        return res.status(200).json({
          "message": "inserted",
          "userid": result.insertId
        });
      }
    } else {
      // Update an existing user
      console.log("Updating user data")
      let user_id = result[0].userid;

      sql = `UPDATE users SET lastname = ?, firstname = ?, username = ?, password = ?
             WHERE email = ?`;

      result = await query_database(musicapp_db, sql, [lastname, firstname, username, hashedPassword, email]);

      if (result.affectedRows === 1) {
        return res.status(200).json({
          "message": "updated",
          "userid": user_id
        });
      }
    }
  } catch (err) {
    console.log("**Error in /user");
    console.log(err.message);

    res.status(500).json({
      "message": err.message,
      "userid": -1
    });
  }
};