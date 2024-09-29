"use client";

import React, { useState, useEffect } from "react";
import FormField from "./FormField";

const FormView: React.FC = () => {
  const [formData, setFormData] = useState<any>(null); // Set initial state as null
  const [error, setError] = useState<string | null>(null); // For error handling

  useEffect(() => {
    fetch("http://localhost:5000/") // Ensure this matches your backend port
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch data");
        }
        return res.json();
      })
      .then((data) => {
        setFormData(data); // Correctly set the fetched data
        setError(null); // Clear any previous errors
      })
      .catch((err) => {
        console.error(err);
        setError("An error occurred while fetching data.");
      });
  }, []);

  // Recursive function to render only fields that have name, xml_name, and valid data
  const renderFormFields = (data: any) => {
    return Object.entries(data).map(([key, value]: [string, any]) => {
      if (
        typeof value === "object" &&
        !Array.isArray(value) &&
        value !== null &&
        value.name &&
        value.xml_name &&
        value.data // Ensure valid data exists
      ) {
        // Render only fields with name, xml_name, and valid data
        return (
          <FormField
            key={key}
            name={value.name}
            value={value.data}
            xmlName={value.xml_name}
          />
        );
      } else if (
        typeof value === "object" &&
        !Array.isArray(value) &&
        value !== null
      ) {
        // Recursively render nested fields if the current value is another object (e.g., sections)
        return renderFormFields(value);
      } else {
        return null; // Skip if it's not an object or doesn't have valid data
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
