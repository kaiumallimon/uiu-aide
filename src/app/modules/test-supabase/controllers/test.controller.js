const userModel = require('../models/test.model');

async function listUsers(req, res) {
  try {
    const all_users = await userModel.getAllUsers();
    res.json({
      message: 'Users retrieved successfully',
      totalUsers: all_users.length,
      users: all_users
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

async function addUser(req, res) {
  try {
    console.log('Incoming request body:', req.body);
    const result = await userModel.createUser(req.body);
    
    // Supabase returns an array even for single insert
    const user = result[0];

    console.log('User added:', user);
    

    res.status(201).json({
      message: 'User added successfully',
      user: user
    });
  } catch (error) {
    console.error('Error adding user:', error);
    res.status(400).json({
      error: error.message || error.details || JSON.stringify(error)
    });
  }
}



module.exports = {
  listUsers,
  addUser,
};
