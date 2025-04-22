const express = require('express');
const router = express.Router();
const userController = require('../controllers/test.controller');

router.get('/', userController.listUsers);
router.post('/add', userController.addUser);

module.exports = router;
