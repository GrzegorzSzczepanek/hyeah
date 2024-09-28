"use client";

import React, { useState, useEffect, KeyboardEvent } from "react";
import { io, Socket } from "socket.io-client";
import Image from 'next/image';

const socket: Socket = io("http://localhost:5000");

interface Message {
  message: string;
  sender: "user" | "bot";
}

const ChatbotComponent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [currentBotMessage, setCurrentBotMessage] = useState<string>("");

  useEffect(() => {
    socket.on("message_chunk", (data: { message: string }) => {
      setCurrentBotMessage((prev) => prev + data.message);
    });

    socket.on("message_done", () => {
      if (currentBotMessage.trim()) {
        const botMessage: Message = {
          message: currentBotMessage,
          sender: "bot",
        };
        console.log(botMessage);
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setCurrentBotMessage("");
      }
    });

    return () => {
      socket.off("message_chunk");
      socket.off("message_done");
    };
  }, [currentBotMessage]);

  const sendMessage = () => {
    if (input.trim()) {
      const userMessage: Message = { message: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      setCurrentBotMessage("");
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
    <div className="flex flex-col items-center w-full mx-auto p-3 h-screen">
      <div className="w-full bg-white shadow-md rounded-lg p-4 h-full overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <>
            {msg.sender === "bot" && (
              <div style={{ width: '40px', height: '40px', position: 'relative' }}>
                <Image
                  src="/herb.png"
                  alt="Bot"
                  layout="fill"
                  className="rounded-full border-2 border-gray2"
                  objectFit="cover"
                />
              </div>
            )}
            <div
              key={index}
              className={`mb-2 p-2 rounded-lg ${msg.sender === "user"
                ? "bg-primary text-white self-end"
                : "bg-secondary text-black self-start"
                }`}
            >
              {msg.message}
            </div>
          </>
        ))}

        {currentBotMessage && (
          <>
            <div style={{ width: '40px', height: '40px', position: 'relative' }}>
              <Image
                src="/herb.png"
                alt="Bot"
                layout="fill"
                className="rounded-full border-2 border-gray2"
                objectFit="cover"
              />
            </div>
            <div className="mb-2 p-2 rounded-lg bg-secondary text-black self-start">
              {currentBotMessage}
            </div>
          </>
        )}
      </div>

      <div className="w-full flex">
        <input
          type="text"
          className="flex-grow text-primary p-2 border rounded-l-lg border-gray2 focus:outline-none focus:ring focus:border-primary"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Twoja wiadomość..."
        />
        <button
          onClick={sendMessage}
          className="p-2 bg-accent text-white rounded-r-lg hover:bg-red-600"
        >
          Wyślij
        </button>
      </div>
    </div>
  );
};

export default ChatbotComponent;
