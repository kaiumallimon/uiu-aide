// config/weaviateClient.js
const weaviate = require('weaviate-client');

const client = weaviate.client({
  scheme: 'https',
  host: process.env.WEAVIATE_URL, // Replace with your Weaviate endpoint
  apiKey: process.env.WEAVIATE_API_KEY,
  timeout: 5000,
});

module.exports = client;
