const supabase = require("../../../configs/supabase.config");


async function getAllUsers() {
  const { data, error } = await supabase.from('test_users').select('*');
  if (error) throw error;
  return data;
}

async function createUser(userData) {
  const { data, error } = await supabase.from('test_users').insert([userData]).select();
  if (error) throw error;
  return data;
}

module.exports = {
  getAllUsers,
  createUser,
};
