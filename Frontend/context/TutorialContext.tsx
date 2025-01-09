"use client";

import React, { createContext, useRef, ReactNode } from "react";

interface TutorialContextProps {
  languageRef: React.RefObject<HTMLElement>;
  chatInputRef: React.RefObject<HTMLInputElement>;
}

export const TutorialContext = createContext<TutorialContextProps | undefined>(
  undefined
);

export const TutorialProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const languageRef = useRef<HTMLElement>(null);
  const chatInputRef = useRef<HTMLInputElement>(null);
  const pTagInputRef = useRef<HTMLParagraphElement>(null);

  return (
    <TutorialContext.Provider
      value={{ languageRef, chatInputRef, pTagInputRef }}
    >
      {children}
    </TutorialContext.Provider>
  );
};
