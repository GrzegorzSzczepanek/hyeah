"use client";
import React, { useState } from "react";
import ChatbotComponent from "@/components/ChatbotComponent";
import FormView from "@/components/FormView";

export default function Home() {
  const [formData, setFormData] = useState<any>(null);

  const [error, setError] = useState<string | null>(null);

  return (
    <main className="flex w-full" style={{ height: "calc(100vh - 56px)" }}>
      <div className="w-1/2 flex flex-col bg-secondary">
        <FormView formData={formData} error={error} />
      </div>
      <div className="w-1/2 flex flex-col bg-gray overflow-hidden">
        <ChatbotComponent setFormData={setFormData} setError={setError} />
      </div>
    </main>
  );
}
