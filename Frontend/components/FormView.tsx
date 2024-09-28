"use client";

import React from "react";
import FormField from "@/components/FormField";

const FormView: React.FC = () => {
  return (
    <div className="flex flex-col w-full max-w-md mx-auto mt-6 p-3">
      <p className="font-bold text-textPrimary items-center">DEKLARACJA W SPRAWIE PODATKU OD CZYNNOŚCI CYWILNOPRAWNYCH</p>
      <FormField />
      <FormField />
      <FormField />
      <FormField />
      <FormField />
    </div>
  );
};

export default FormView;
