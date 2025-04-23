const {GoogleGenerativeAI} = require('@google/generative-ai');

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);


// This function generates embeddings for a given text using the Google Generative AI API.
const generateEmbedding = async (text)=>{
    try{
        const model = genAI.getGenerativeModel({ model: 'embedding-001' }); 
        const response = await model.embedContent(text);
        return response.embedding.values;

    }catch(error){
        console.error('Error generating embedding:', error);
        throw new Error('Failed to generate embedding');    
    }
}


module.exports = {
    generateEmbedding
}