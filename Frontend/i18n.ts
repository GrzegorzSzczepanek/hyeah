// src/i18n.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Translation resources
const resources = {
  pl: {
    translation: {
      home: "Strona Główna",
      about: "O Nas",
      contact: "Kontakt",
      language: "Język",
      welcome_message: "Witaj w Mojej Aplikacji!",
      // Add more translations as needed
    },
  },
  en: {
    translation: {
      home: "Home",
      about: "About",
      contact: "Contact",
      language: "Language",
      welcome_message: "Welcome to My App!",
      // Add more translations as needed
    },
  },
  ua: {
    // Ukrainian language code is 'uk', but to prevent conflict with 'ua' country code, using 'ua'
    translation: {
      home: "Головна",
      about: "Про нас",
      contact: "Контакт",
      language: "Мова",
      welcome_message: "Ласкаво просимо до моєї програми!",
      // Add more translations as needed
    },
  },
};

i18n
  .use(initReactI18next) // Passes i18n down to react-i18next
  .init({
    resources,
    lng: "pl", // Default language
    fallbackLng: "pl",

    interpolation: {
      escapeValue: false, // React already safes from xss
    },
  });

export default i18n;
