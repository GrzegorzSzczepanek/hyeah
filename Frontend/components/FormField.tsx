"use client";

import React from "react";

interface FormFieldProps {
  name: string;
  value: string;
}

const FormField: React.FC<FormFieldProps> = ({ name, value }) => {
  return (
    <div>
      <p className="mt-6 text-textPrimary">
        <span className="font-bold">{name}</span>
      </p>
      <div
        className="mb-2 border border-gray2 rounded-lg text-right px-5 text-primary bg-gray3"
        style={{ boxShadow: "2px 2px 0px 0px #cccccc" }}
      >
        {value}
      </div>
    </div>
  );
};

export default FormField;
