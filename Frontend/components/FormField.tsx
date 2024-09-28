"use client";

import React from "react";

const FormField: React.FC = () => {
  return (
    <div>
      <p className="mt-6 text-textPrimary">
        Okres, miejsce i cel składania deklaracji
      </p>
      <div
        className="mt-2 border border-gray2 rounded-lg p-1 text-right px-5 text-primary bg-gray3"
        style={{ boxShadow: "2px 2px 0px 0px #cccccc" }}
      >
        AI
      </div>
    </div>
  );
};

export default FormField;
