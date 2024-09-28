"use client";

import React, { useState, useEffect, KeyboardEvent } from "react";
import { io, Socket } from "socket.io-client";

const socket: Socket = io("http://localhost:5000");

interface Message {
  message: string;
  sender: "user" | "bot";
}

const ChatbotComponent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  useEffect(() => {
    socket.on("message", (data: { message: string }) => {
      const botMessage: Message = { message: data.message, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    });

    return () => {
      socket.off("message");
    };
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      const userMessage: Message = { message: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      socket.emit("message", { message: input });

      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-md mx-auto mt-6">
      <div className="w-full bg-white shadow-md rounded-lg p-4 h-80 overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-2 p-2 rounded-lg ${
              msg.sender === "user"
                ? "bg-primary text-white self-end"
                : "bg-secondary text-black self-start"
            }`}
          >
            {msg.message}
          </div>
        ))}
      </div>

      <div className="w-full flex">
        <input
          type="text"
          className="flex-grow text-primary p-2 border rounded-l-lg border-gray-300 focus:outline-none focus:ring focus:border-primary"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          className="p-2 bg-accent text-white rounded-r-lg hover:bg-red-600"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatbotComponent;
