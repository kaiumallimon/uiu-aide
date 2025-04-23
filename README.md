# 🧠 UIU AIDE – Adaptive Intelligent Digital Education
A LangChain-powered adaptive SaaS learning system with configurable agents, tools, and RAG-based knowledge.

## Theoretical Foundation (LangChain-based Agent System)
The AIDE system leverages LangChain's modular framework to build a robust, scalable, and adaptive learning platform. It extends beyond traditional LLM-based systems by integrating tools, retrieval mechanisms, and domain-specific configurations.

### Multi-Agent System

The AIDE system is designed as a multi-agent system, where each agent is implemented using LangChain's `Agent` and `Tool` abstractions. This enables modularity, parallelism, and specialization.

- **Agents** = LangChain `Agent` + Configuration (`PromptTemplate` + Tools + Data Sources).
- Each agent specializes in a specific domain/subject area via:
    - Custom `PromptTemplate` for system behavior.
    - Custom `Tool` integrations.
    - Custom Data Sources (e.g., textbooks, lecture notes, question banks) loaded into a vector database.
    - Optional tools for actions (e.g., search, calculator, code executor).

### RAG (Retrieval-Augmented Generation)
RAG is implemented using LangChain's `RetrievalQA` chain, combining retrieval-based and generation-based approaches for accurate and context-aware responses.

How does RAG work in AIDE?
1. User queries are processed by the agent.
2. Relevant documents are retrieved from a vector database (e.g., Pinecone, Weaviate, or FAISS) using embeddings.
3. The retrieved documents are passed as context to the LLM via LangChain's `RetrievalQA` chain.
4. The LLM generates a response based on the query and retrieved context.

### Toolformer-style Tools
Tools are implemented using LangChain's `Tool` abstraction. These tools allow agents to perform specific tasks or actions, such as searching, calculating, or executing code.

### Tool Integration Examples

Here are some examples of tools integrated into the AIDE system:
- Tools are registered with the agent.
- The agent dynamically selects and invokes tools based on the user's query.

## System Architecture

### High-Level Overview

The AIDE system is built on a modular architecture that integrates LangChain's components with external services for storage, authentication, and vector search. The architecture ensures scalability, maintainability, and adaptability to various educational use cases.

### Core Components

1. **Authentication & User Management:**
    - Handled via Django's built-in authentication system.
    - Supports role-based access control (e.g., Admin, Student).

2. **Agent Engine:**
    - Stores agent configurations, including `PromptTemplate`, tools, and data sources.
    - Provides APIs to create, edit, and delete agents.
    - Manages agent lifecycle and runtime execution.

3. **Vector Database:**
    - Stores embeddings of knowledge sources (e.g., textbooks, lecture notes).
    - Supports vector similarity search for document retrieval.
    - Examples: Pinecone, Weaviate, or FAISS.

4. **RAG Layer:**
    - Combines retrieval and generation for context-aware responses.
    - Dynamically fetches relevant documents and integrates them into the LLM's prompt.

5. **Tool Management:**
    - Tools are registered and managed using LangChain's `Tool` abstraction.
    - Tools are invoked dynamically based on user queries and agent configurations.

6. **Dashboards:**
    - **Admin Dashboard:**
        - Create and configure agents.
        - Monitor system performance and usage analytics.
    - **Student Dashboard:**
        - Chat interface for interacting with agents.
        - View learning progress and usage history.

### Detailed Workflow

1. **Agent Configuration:**
    - Admins define agents by specifying `PromptTemplate`, tools, and data sources.
    - Data sources are preprocessed and stored as embeddings in the vector database.

2. **Query Processing:**
    - A user query is routed to the appropriate agent based on the context.
    - The agent retrieves its configuration and tools.

3. **Document Retrieval:**
    - The query is embedded and matched against the vector database.
    - Relevant documents are retrieved and passed to the agent.

4. **Response Generation:**
    - The agent combines the `PromptTemplate`, user query, and retrieved documents.
    - LangChain's `RetrievalQA` chain generates a response.

5. **Tool Invocation:**
    - If the query requires specific actions (e.g., calculations), the agent invokes the appropriate tool.
    - Tool results are integrated into the final response.

6. **Response Delivery:**
    - The generated response is returned to the user via the chat interface.

### Deployment Architecture

- **Frontend:**
    - Built with React.js for dynamic dashboards and chat interfaces.
    - Communicates with the backend via REST or GraphQL APIs.

- **Backend:**
    - Python Django-based backend using Django REST Framework (DRF).
    - Integrates LangChain for agent execution and RAG processing.

- **Database:**
    - PostgreSQL for user management and agent configurations.
    - Vector database for document retrieval.

By leveraging LangChain's modular components and integrating Django's robust backend capabilities, the AIDE system provides a comprehensive and adaptive solution for digital education.
