const {registerUser, loginUser} = require('../services/auth.service');


// This function handles the registration of a new user. It extracts the email, password, and full name from the request body and calls the registerUser service function. If successful, it sends a success response; otherwise, it sends an error response.
async function register(req, res) {
    const {email, password, full_name} = req.body;
    try {
        const user = await registerUser(email, password, full_name);
        return res.status(201).json({
            status: 'success',
            message: 'User registered successfully',
            data: user
        });
    } catch (error) {
        return res.status(400).json({
            status: 'error',
            message: error.message
        });
    }
}


// This function handles user login. It extracts the email and password from the request body and calls the loginUser service function. If successful, it sends a success response with the user data; otherwise, it sends an error response.
async function login(req, res) {
    const {email, password} = req.body;
    try {
        const user = await loginUser(email, password);
        return res.status(200).json({
            status: 'success',
            message: 'User logged in successfully',
            data: user
        });
    } catch (error) {
        return res.status(401).json({
            status: 'error',
            message: error.message
        });
    }
}


module.exports = {
    register,
    login
};