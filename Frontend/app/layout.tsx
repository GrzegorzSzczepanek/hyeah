// src/app/layout.tsx
"use client";

import "./globals.css";
import { Inter } from "next/font/google";
import { ReactNode, useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import CssBaseline from "@mui/material/CssBaseline";
import { I18nextProvider } from "react-i18next";
import i18n from "@/i18n";
import Tutorial from "@/components/Tutorial";
import { TutorialProvider } from "@/context/TutorialContext";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }: { children: ReactNode }) {
  const [isTutorialOpen, setIsTutorialOpen] = useState(false);

  useEffect(() => {
    const hasSeenTutorial = localStorage.getItem("hasSeenTutorial");
    const dontShowTutorial = localStorage.getItem("dontShowTutorial");
    if (!hasSeenTutorial && !dontShowTutorial) {
      setIsTutorialOpen(true);
      localStorage.setItem("hasSeenTutorial", "true");
    }
  }, []);

  const openTutorial = () => {
    setIsTutorialOpen(true);
  };

  const closeTutorial = () => {
    setIsTutorialOpen(false);
  };

  const exportToXML = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/to-xml");
      if (!response.ok) {
        throw new Error("Failed to fetch XML data");
      }

      const xmlData = await response.text();

      // Create a Blob from the XML data
      const blob = new Blob([xmlData], { type: "application/xml" });

      // Create a URL for the Blob
      const url = window.URL.createObjectURL(blob);

      // Create a link element and simulate a click to download the file
      const link = document.createElement("a");
      link.href = url;
      link.download = "form_data.xml"; // Default file name
      document.body.appendChild(link);
      link.click();

      // Clean up the URL object
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error exporting to XML:", error);
    }
  };

  return (
    <html lang="pl">
      <body
        className={`${inter.className} bg-secondary`}
        style={{ height: "calc(100vh - 56px)" }}
      >
        <I18nextProvider i18n={i18n}>
          <CssBaseline />
          <TutorialProvider>
            <Navbar openTutorial={openTutorial} exportToXML={exportToXML} />
            {children}
            <Tutorial open={isTutorialOpen} onClose={closeTutorial} />
          </TutorialProvider>
        </I18nextProvider>
      </body>
    </html>
  );
}
