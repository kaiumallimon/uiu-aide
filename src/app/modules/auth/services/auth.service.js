const supabase = require('../../../configs/supabase.config');


// This function is used to register a new user in the Supabase authentication system.  
async function registerUser(email,password,full_name) {
    const {data,error} = await supabase.auth.signUp({
        email,
        password,
        options:{
            data: {full_name, role: 'student'}
        }
    })
    
    if (error) {
        console.error('Registration error:', error.message);
        throw new Error(error.message);
    }

    console.log('User registered successfully:', data.user);
    return data;
}


// This function is used to log in a user to the Supabase authentication system.    

async function loginUser(email,password) {
    const {data,error} = await supabase.auth.signInWithPassword({
        email,
        password
    })
    
    if (error) {
        console.error('Login error:', error.message);
        throw new Error(error.message);
    }

    console.log('User logged in successfully:', data.user);
    return data;
}


module.exports = {
    registerUser,
    loginUser
}