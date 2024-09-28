"use client";

import React, { useState, useEffect, KeyboardEvent } from "react";
import { io, Socket } from "socket.io-client";
import Image from 'next/image';
import Markdown from 'react-markdown';

const socket: Socket = io("http://localhost:5000");

interface Message {
  message: string;
  sender: "user" | "bot";
}

const ChatbotComponent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([{ message: "Witaj! Pomogę Ci w wypełnianiu wniosku!", sender: "bot" }]);
  const [input, setInput] = useState<string>("");
  const [currentBotMessage, setCurrentBotMessage] = useState<string>("");

  useEffect(() => {
    const handleMessageChunk = (data: { message: string }) => {
      setCurrentBotMessage((prev) => prev + data.message);
    };

    const handleMessageDone = () => {
      if (currentBotMessage.trim()) {
        const botMessage: Message = {
          message: currentBotMessage,
          sender: "bot",
        };
        console.log(botMessage);
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setCurrentBotMessage("");
      }
    };

    socket.on("message_chunk", handleMessageChunk);
    socket.on("message_done", handleMessageDone);

    return () => {
      socket.off("message_chunk", handleMessageChunk);
      socket.off("message_done", handleMessageDone);
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
      <div className="w-full bg-white shadow-md rounded-lg p-4 h-full overflow-y-auto mb-4 flex flex-col">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start mb-4 ${msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
          >
            {msg.sender === "bot" && (
              <div className="mr-2 flex-shrink-0" style={{ width: '40px', height: '40px', position: 'relative' }}>
                <Image
                  src="/herb.png"
                  alt="Bot"
                  layout="fill"
                  className="rounded-full border-2 border-gray-200"
                  objectFit="cover"
                />
              </div>
            )}
            <div
              className={`p-2 rounded-lg max-w-xs ${msg.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray3 text-black"
                }`}
            >
              <Markdown>
                {msg.message}
              </Markdown>
            </div>
          </div>
        ))}

        {currentBotMessage && (
          <div className="flex items-start mb-4 justify-start">
            <div className="mr-2 flex-shrink-0" style={{ width: '40px', height: '40px', position: 'relative' }}>
              <Image
                src="/herb.png"
                alt="Bot"
                layout="fill"
                className="rounded-full border-2 border-gray-200"
                objectFit="cover"
              />
            </div>
            <div className="p-2 rounded-lg bg-gray3 text-black animate-pulse max-w-xs">
              <Markdown>
                {currentBotMessage}
              </Markdown>
            </div>
          </div>
        )}
      </div>

      <div className="w-full flex">
        <input
          type="text"
          className="flex-grow text-gray-700 p-2 border border-gray2 rounded-l-lg border-gray-300 focus:outline-none focus:ring focus:border-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Twoja wiadomość..."
        />
        <button
          onClick={sendMessage}
          className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600"
        >
          Wyślij
        </button>
      </div>
    </div>
  );
};

export default ChatbotComponent;
