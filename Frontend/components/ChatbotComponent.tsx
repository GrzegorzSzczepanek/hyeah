// src/components/ChatbotComponent.tsx
"use client";

import React, { useState, useEffect, KeyboardEvent, useContext } from "react";
import { io, Socket } from "socket.io-client";
import Image from "next/image";
import Markdown from "react-markdown";
import { TutorialContext } from "@/context/TutorialContext";
import { Snackbar, Alert, TextField, Box, Button } from "@mui/material";
import { useTranslation } from "react-i18next";

const socket: Socket = io("http://localhost:5000");

interface Message {
  message: string;
  sender: "user" | "bot";
}

const ChatbotComponent: React.FC = () => {
  const { t, i18n } = useTranslation();
  const tutorialContext = useContext(TutorialContext);

  const [messages, setMessages] = useState<Message[]>([
    { message: t("welcome_message"), sender: "bot" },
  ]);
  const [input, setInput] = useState<string>("");
  const [currentBotMessage, setCurrentBotMessage] = useState<string>("");

  // States for Snackbars
  const [warningOpen, setWarningOpen] = useState<boolean>(false);
  const [sessionClosed, setSessionClosed] = useState<boolean>(false);
  const [sessionClosedSnackbarOpen, setSessionClosedSnackbarOpen] =
    useState<boolean>(false);

  useEffect(() => {
    // Event handlers
    const handleMessageChunk = (data: { message: string }) => {
      setCurrentBotMessage((prev) => prev + data.message);
      const contentContainer = document.getElementById('chat-box');
      contentContainer.scrollTop = contentContainer.scrollHeight;
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

    const handleWarning = (data: { message: string }) => {
      // Display a Snackbar warning
      setWarningOpen(true);
      // Optionally, you can also add the warning message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { message: data.message, sender: "bot" },
      ]);
    };

    const handleSessionClosed = (data: { message: string }) => {
      // Set session as closed and open the session closed Snackbar
      setSessionClosed(true);
      setSessionClosedSnackbarOpen(true);
      // Optionally, add the session closed message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { message: data.message, sender: "bot" },
      ]);
      // Optional: Disconnect the socket if needed
      // socket.disconnect();
    };

    // Register event listeners
    socket.on("message_chunk", handleMessageChunk);
    socket.on("message_done", handleMessageDone);
    socket.on("message", handleWarning); // Warning message
    socket.on("session_closed", handleSessionClosed); // Session closed message

    // Cleanup on unmount
    return () => {
      socket.off("message_chunk", handleMessageChunk);
      socket.off("message_done", handleMessageDone);
      socket.off("message", handleWarning);
      socket.off("session_closed", handleSessionClosed);
    };
  }, [currentBotMessage]);

  useEffect(() => {
    // Update welcome message when language changes
    setMessages((prevMessages) =>
      prevMessages.map((msg) =>
        msg.sender === "bot" ? { ...msg, message: t("welcome_message") } : msg
      )
    );
  }, [i18n.language, t]);

  const sendMessage = () => {
    if (sessionClosed) return; // Prevent sending messages if session is closed

    if (input.trim()) {
      const userMessage: Message = { message: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      setCurrentBotMessage("");
      socket.emit("message", { message: input });

      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Prevent form submission or other default behaviors
      sendMessage();
    }
  };

  // Handlers for Snackbars
  const handleWarningClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }
    setWarningOpen(false);
  };

  const handleSessionClosedClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }
    setSessionClosedSnackbarOpen(false);
  };

  return (
    <div className="flex flex-col items-center w-full mx-auto p-3 h-full">
      <div id="chat-box" className="w-full bg-white shadow-md rounded-lg p-4 h-full overflow-y-auto mb-4 flex flex-col">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start mb-4 ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.sender === "bot" && (
              <div
                className="mr-2 flex-shrink-0"
                style={{ width: "40px", height: "40px", position: "relative" }}
              >
                <Image
                  src="/herb.png"
                  alt="Bot"
                  layout="fill"
                  className="rounded-full border-2 border-gray3"
                  objectFit="cover"
                />
              </div>
            )}
            <div
              className={`p-2 rounded-lg max-w-lg ${
                msg.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray3 text-black"
              }`}
            >
              <Markdown>{msg.message}</Markdown>
            </div>
          </div>
        ))}

        {currentBotMessage && (
          <div className="flex items-start mb-4 justify-start">
            <div
              className="mr-2 flex-shrink-0"
              style={{ width: "40px", height: "40px", position: "relative" }}
            >
              <Image
                src="/herb.png"
                alt="Bot"
                layout="fill"
                className="rounded-full border-2 border-gray3"
                objectFit="cover"
              />
            </div>
            <div className="p-2 rounded-lg bg-gray3 text-black animate-pulse max-w-lg">
              <Markdown>{currentBotMessage}</Markdown>
            </div>
          </div>
        )}
      </div>
      <Box className="w-full" ref={tutorialContext?.chatInputRef}>
        <Box
          display="flex"
          alignItems="center"
          sx={{
            "& .MuiTextField-root": {
              flexGrow: 1,
              marginRight: "8px",
            },
          }}
        >
          <TextField
            id="chatInput"
            variant="outlined"
            fullWidth
            multiline={false}
            maxRows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t("your_message_placeholder")}
            disabled={sessionClosed} // Disable when session is closed
            InputProps={{
              style: {
                backgroundColor: sessionClosed ? "#f5f5f5" : "#fff", // Optional: change background when disabled
              },
            }}
            sx={{
              "& .MuiOutlinedInput-root": {
                borderRadius: "4px 0 0 4px",
                "& fieldset": {
                  borderColor: "#d1d5db", // Equivalent to border-gray-300
                },
                "&:hover fieldset": {
                  borderColor: "#3b82f6", // Equivalent to focus:border-blue-500
                },
                "&.Mui-focused fieldset": {
                  borderColor: "#3b82f6",
                  boxShadow: "0 0 0 2px rgba(59, 130, 246, 0.2)", // Similar to focus:ring
                },
              },
              "& .MuiInputBase-input": {
                color: "#4b5563", // Equivalent to text-gray-700
                padding: "8px 12px", // Equivalent to p-2
              },
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={sendMessage}
            disabled={sessionClosed} // Disable when session is closed
            sx={{
              borderTopLeftRadius: 0,
              borderBottomLeftRadius: 0,
              borderTopRightRadius: "4px",
              borderBottomRightRadius: "4px",
              cursor: sessionClosed ? "not-allowed" : "pointer", // Change cursor style when disabled
              minWidth: "80px", // Optional: set a minimum width
            }}
          >
            {t("send")}
          </Button>
        </Box>
      </Box>

      {/* Warning Snackbar */}
      <Snackbar
        open={warningOpen}
        autoHideDuration={15000} // Auto-hide after 15 seconds
        onClose={handleWarningClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={handleWarningClose}
          severity="warning"
          sx={{ width: "100%" }}
        >
          {t("inactivity_warning")}
        </Alert>
      </Snackbar>

      {/* Session Closed Snackbar */}
      <Snackbar
        open={sessionClosedSnackbarOpen}
        autoHideDuration={6000} // Auto-hide after 6 seconds
        onClose={handleSessionClosedClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={handleSessionClosedClose}
          severity="error"
          sx={{ width: "100%" }}
        >
          {t("session_closed_message")}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default ChatbotComponent;
