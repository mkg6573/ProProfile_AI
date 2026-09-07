import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!question.trim() || loading) {
      return;
    }

    const userQuestion = question.trim();

    // Show user's message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend error: ${response.status}`
        );
      }

      const data = await response.json();

      // Show AI response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error(
        "Error communicating with backend:",
        error
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Unable to connect to the backend. Please make sure FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  }

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="chat-header">
        <div className="header-content">
          <h3>Mohit Assistance</h3>
          <span>Ask about Mohit</span>
        </div>
      </header>


      {/* ================= MAIN CHAT ================= */}

      <main className="chat-container">

        {/* ================= MESSAGES ================= */}

        <section className="messages">

          {/* Welcome */}

          {messages.length === 0 && (
            <div className="welcome">
              <h2>Hi 👋</h2>

              <p>
                Ask me about Mohit.
              </p>
            </div>
          )}


          {/* Chat Messages */}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${
                message.role === "user"
                  ? "user-message"
                  : "assistant-message"
              }`}
            >

              {/* AI Avatar */}

              {message.role === "assistant" && (
                <div className="avatar">
                  AI
                </div>
              )}


              {/* Message Content */}

              <div className="message-content">
                <ReactMarkdown>
                  {message.content}
                </ReactMarkdown>
              </div>

            </div>
          ))}


          {/* Loading */}

          {loading && (
            <div className="message assistant-message">

              <div className="avatar">
                AI
              </div>

              <div className="message-content">
                <p>Thinking...</p>
              </div>

            </div>
          )}

        </section>


        {/* ================= INPUT ================= */}

        <div className="input-container">

          <input
            type="text"
            value={question}
            placeholder="Ask something about Mohit..."
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={
              loading || !question.trim()
            }
          >
            ➤
          </button>

        </div>

      </main>

    </div>
  );
}

export default App;