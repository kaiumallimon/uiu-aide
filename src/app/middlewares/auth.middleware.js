const supabase = require('../configs/supabase.config');


// This middleware function checks if the user is authenticated by verifying the JWT token in the request headers. If the token is valid, it attaches the user information to the request object; otherwise, it sends an unauthorized response.
async function authMiddleware(req, res, next) {
    const token = req.headers['authorization']?.split(' ')[1]; // Extract the token from the Authorization header

    if (!token) {
        return res.status(401).json({
            status: 'error',
            message: 'Unauthorized - No token provided'
        });
    }

    try {
        const { data, error } = await supabase.auth.getUser(token);

        if (error) {
            return res.status(401).json({
                status: 'error',
                message: 'Unauthorized - Invalid token'
            });
        }

        req.user = data.user; // Attach user information to the request object
        next(); // Call the next middleware or route handler
    } catch (error) {
        return res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
}


module.exports = authMiddleware;