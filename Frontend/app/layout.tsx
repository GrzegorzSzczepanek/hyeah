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

  return (
    <html lang="pl">
      <body
        className={`${inter.className} bg-secondary`}
        style={{ height: "calc(100vh - 56px)" }}
      >
        <I18nextProvider i18n={i18n}>
          <CssBaseline />
          <TutorialProvider>
            <Navbar openTutorial={openTutorial} />
            {children}
            <Tutorial open={isTutorialOpen} onClose={closeTutorial} />
          </TutorialProvider>
        </I18nextProvider>
      </body>
    </html>
  );
}
