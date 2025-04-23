const {register, login}= require('../controllers/auth.controller');
const express = require('express');
const router = express.Router();


// Define the routes for user registration and login
router.post('/register', register);
router.post('/login', login);

module.exports = router;