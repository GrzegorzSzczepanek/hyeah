// app/layout.tsx
"use client";

import "./globals.css";
import { Inter } from "next/font/google";
import { ReactNode } from "react";
import Navbar from "@/components/Navbar";
import CssBaseline from "@mui/material/CssBaseline";
import { I18nextProvider } from "react-i18next";
import i18n from "@/i18n";

const inter = Inter({ subsets: ["latin"] });

// export const metadata = {
//   title: "Podatki AI",
//   description: "Projekt na HackYeah",
// };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body className={`${inter.className} bg-secondary h-screen`}>
        <I18nextProvider i18n={i18n}>
          <CssBaseline />
          <Navbar />
          {children}
        </I18nextProvider>
      </body>
    </html>
  );
}
