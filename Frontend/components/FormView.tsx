"use client";

import React, { useState, useEffect } from "react";
import FormField from "./FormField";

interface FormViewProps {
  formData: any;
  error: string | null;
}

const FormView: React.FC<FormViewProps> = ({ formData, error }) => {
  // const [formData, setFormData] = useState<any>(null);

  const renderFormFields = (data: any) => {
    return Object.entries(data).map(([key, value]: [string, any]) => {
      if (
        typeof value === "object" &&
        !Array.isArray(value) &&
        value !== null &&
        value.name &&
        value.xml_name &&
        value.data !== null &&
        value.data !== undefined &&
        value.data !== "" &&
        value.data !== " "
      ) {
        return <FormField key={key} name={value.name} value={value.data} />;
      } else if (
        typeof value === "object" &&
        !Array.isArray(value) &&
        value !== null
      ) {
        return renderFormFields(value);
      } else {
        return null;
      }
    });
  };

  return (
    <div className="flex flex-col w-full max-w-md mx-auto mt-6 p-3 overflow-y-scroll max-h-full">
      <p className="font-bold text-textPrimary items-center">
        DEKLARACJA W SPRAWIE PODATKU OD CZYNNOŚCI CYWILNOPRAWNYCH
      </p>
      {error && <p className="text-red-500">{error}</p>}
      {formData ? (
        <div>
          {/* Render the form fields */}
          {renderFormFields(formData)}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default FormView;
