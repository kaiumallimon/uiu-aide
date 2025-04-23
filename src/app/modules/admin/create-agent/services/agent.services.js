// services/agentService.js
const { agentExecutor } = require('langchain');
const { generateText } = require('../config/geminiClient');  // Use Gemini for text generation
const { generateEmbedding } = require('../config/geminiClient');  // Use Gemini for embeddings
const { WeaviateRetriever } = require('langchain/vectorstores/weaviate');
const client = require('../config/weaviateClient');
const { createAgent } = require('../models/agentModel'); // Our database model to store agent metadata

const createDynamicAgent = async (agentConfig) => {
  try {
    const { name, prompt_template, tools, vector_namespace, created_by } = agentConfig;

    // 1. Generate embedding for the prompt template or agent-related content
    const embedding = await generateEmbedding(prompt_template);  // Example: Generating embedding for prompt template

    // 2. Store the generated vector in Weaviate
    await storeInWeaviate(embedding, name, prompt_template, vector_namespace);

    // 3. Set up Weaviate as the retriever
    const weaviateRetriever = new WeaviateRetriever(client, vector_namespace);

    // 4. Create a LangChain agent executor
    const agent = agentExecutor(
      [
        // Your agent tools, for example search, computation, etc.
        tools,
        // Custom LLM using Gemini API
        {
          type: 'llm',
          model: {
            generate: async (prompt) => {
              const response = await generateText(prompt);
              return response;
            },
          },
        },
        weaviateRetriever,
      ],
      {
        agentType: 'zero-shot-react-description', // Choose the right agent type
        verbose: true,
      }
    );

    // 5. Save the agent configuration in the database
    const newAgent = await createAgent({
      name,
      prompt_template,
      tools,
      vector_namespace,
      created_by,
    });

    return newAgent;
  } catch (error) {
    console.error('Error creating dynamic agent:', error);
    throw error;
  }
};

// Helper function to store embedding in Weaviate
const storeInWeaviate = async (embedding, title, content, vector_namespace) => {
  try {
    const response = await client.data.creator('Textbook')
      .withProperties({
        title,
        content,
        vector_namespace,
      })
      .withVector(embedding)
      .do();

    console.log('Successfully stored vector in Weaviate:', response);
    return response;
  } catch (error) {
    console.error('Error storing in Weaviate:', error);
    throw new Error('Failed to store vector in Weaviate');
  }
};

module.exports = { createDynamicAgent };
