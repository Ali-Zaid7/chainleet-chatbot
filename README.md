## How the Panaversity AI Assistant Works

This guide explains the main components and flow of the Panaversity AI Assistant, built using Chainlit and Gemini via an OpenAI-compatible interface.

---

### 1. Environment Setup

- **Environment Variables:** Sensitive data (like `GEMINI_API_KEY`) is loaded from a `.env` file using `dotenv`. This keeps secrets out of your codebase.
- **Validation:** The script checks for the presence of `GEMINI_API_KEY` and stops execution if it's missing.

---

### 2. Importing Dependencies

- **Chainlit:** Powers the chat UI and session management.
- **Agents SDK:** Provides abstractions for agents, runners, and model interfaces.
- **Type Casting:** Used for better editor support and type safety.

---

### 3. Session Initialization (`@cl.on_chat_start`)

- **External Client:** Initializes Gemini via an OpenAI-compatible wrapper.
- **Model Setup:** Wraps Gemini as a ChatGPT-style model.
- **Configuration:** Bundles model, provider, and tracing options.
- **Session State:** Stores chat history, config, and agent in the user session.
- **Welcome Message:** Sends an initial greeting to the user.

---

### 4. Message Handling (`@cl.on_message`)

- **Placeholder Message:** Shows "Thinking..." while processing.
- **Session Retrieval:** Loads agent, config, and chat history from session.
- **History Update:** Adds the new user message to history.
- **Agent Execution:** Runs the agent synchronously with full history.
- **Response Update:** Replaces the placeholder with the assistant's reply.
- **History Persistence:** Updates session with the latest conversation.
- **Logging:** Prints user and assistant messages for debugging.
- **Error Handling:** Displays errors to the user if something goes wrong.

---

### Key Concepts

| Concept                      | Why It's Important                                      |
|------------------------------|--------------------------------------------------------|
| Session state (`cl.user_session`) | Tracks config, agent, and history per user           |
| Agent object                 | Represents the LLM and its instructions                |
| `Runner.run_sync(...)`       | Executes the agent with full conversation history      |
| History handling             | Provides memory for contextual replies                 |
| Async message updates        | Improves chat responsiveness and user experience       |

---

This structure ensures a secure, responsive, and context-aware AI assistant experience.
