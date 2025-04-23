const express = require('express');
const app = express();
const userRoutes = require('../src/app/modules/test-supabase/routes/test.route');
const authRoutes = require('../src/app/modules/auth/routes/auth.route');
require('dotenv').config();

app.use(express.json());

app.use('/api/v1/users', userRoutes);
app.use('/api/v1/auth', authRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
