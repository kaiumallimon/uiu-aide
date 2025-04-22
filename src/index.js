const express = require('express');
const app = express();
const userRoutes = require('../src/app/modules/test-supabase/routes/test.route');
require('dotenv').config();

app.use(express.json());

app.use('/api/users', userRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
