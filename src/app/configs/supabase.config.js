// services/supabaseClient.js
require('dotenv').config(); // <-- Load environment variables from .env
const { createClient } = require('@supabase/supabase-js');

// Load values from environment
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

// Optional: Add check to ensure variables are loaded
if (!supabaseUrl || !supabaseKey) {
  throw new Error('Missing Supabase environment variables');
}

const supabase = createClient(supabaseUrl, supabaseKey);

if (!supabase) {
  throw new Error('Failed to create Supabase client');
}else{
    console.log('Supabase client created successfully');
}

module.exports = supabase;
