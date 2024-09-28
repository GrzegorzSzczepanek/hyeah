// src/i18n.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Translation resources
const resources = {
  pl: {
    translation: {
      home: "Strona główna",
      about: "O nas",
      contact: "Kontakt",
      tutorial: "Tutorial",
      tutorial_ai_title: "Narzędzie AI",
      tutorial_ai_description:
        "To narzędzie AI pomaga w efektywnym wypełnianiu formularzy podatkowych. Prowadzi Cię przez każdy krok, zapewniając dokładność.",
      tutorial_chat_title: "Funkcja Czat",
      tutorial_chat_description:
        "Użyj czatu, aby komunikować się z naszym asystentem AI. Może on odpowiadać na Twoje pytania i zapewniać pomoc w czasie rzeczywistym.",
      tutorial_language_title: "Zmiana Języka",
      tutorial_language_description:
        "Kliknij ikonę języka w pasku nawigacji, aby zmienić język aplikacji na preferowany.",
      tutorial_chat_features_title: "Używanie Funkcji Czat",
      tutorial_chat_features_description:
        "Wpisz swoje pytanie w polu czatu i naciśnij 'Wyślij', aby otrzymać odpowiedź od naszego asystenta AI.",
      tutorial_tax_form_assist_title:
        "Pomoc w Wypełnianiu Formularzy Podatkowych",
      tutorial_tax_form_assist_description:
        "Wprowadź swoje dane w formularzu podatkowym, a nasz asystent AI pomoże Ci wypełnić wszystkie niezbędne pola.",
      next: "Dalej",
      finish: "Zakończ",
      skip: "Pomiń",
      dont_show_again: "Nie pokazuj tego tutorialu ponownie",
      your_message_placeholder: "Twoja wiadomość...",
      send: "Wyślij",
      // Add any additional translations needed
    },
  },
  en: {
    translation: {
      home: "Home",
      about: "About",
      contact: "Contact",
      tutorial: "Tutorial",
      tutorial_ai_title: "AI Tool",
      tutorial_ai_description:
        "This AI tool helps you efficiently fill out tax forms. It guides you through each step to ensure accuracy.",
      tutorial_chat_title: "Chat Feature",
      tutorial_chat_description:
        "Use the chat to communicate with our AI assistant. It can answer your questions and provide real-time assistance.",
      tutorial_language_title: "Language Change",
      tutorial_language_description:
        "Click the language icon in the navbar to change the application's language to your preference.",
      tutorial_chat_features_title: "Using the Chat Feature",
      tutorial_chat_features_description:
        "Type your question into the chat box and press 'Send' to receive a response from our AI assistant.",
      tutorial_tax_form_assist_title: "Assistance with Filling Tax Forms",
      tutorial_tax_form_assist_description:
        "Enter your information into the tax form, and our AI assistant will help you fill out all necessary fields.",
      next: "Next",
      finish: "Finish",
      skip: "Skip",
      dont_show_again: "Don't show this tutorial again",
      your_message_placeholder: "Your message...",
      send: "Send",
      // Add any additional translations needed
    },
  },
  uk: {
    translation: {
      home: "Головна",
      about: "Про нас",
      contact: "Контакт",
      tutorial: "Tutorial",
      tutorial_ai_title: "Інструмент AI",
      tutorial_ai_description:
        "Цей інструмент AI допомагає ефективно заповнювати податкові форми. Він проводить вас через кожен крок, забезпечуючи точність.",
      tutorial_chat_title: "Функція Чат",
      tutorial_chat_description:
        "Використовуйте чат для спілкування з нашим асистентом AI. Він може відповідати на ваші запитання та надавати допомогу в режимі реального часу.",
      tutorial_language_title: "Зміна Мови",
      tutorial_language_description:
        "Натисніть на іконку мови в навігаційній панелі, щоб змінити мову додатку на вашу преференцію.",
      tutorial_chat_features_title: "Використання Функції Чат",
      tutorial_chat_features_description:
        "Введіть своє запитання в поле чату та натисніть 'Надіслати', щоб отримати відповідь від нашого асистента AI.",
      tutorial_tax_form_assist_title: "Допомога у Заповненні Податкових Форм",
      tutorial_tax_form_assist_description:
        "Введіть свої дані у податкову форму, і наш асистент AI допоможе вам заповнити всі необхідні поля.",
      next: "Далі",
      finish: "Завершити",
      skip: "Пропустити",
      dont_show_again: "Не показувати цей туторіал знову",
      your_message_placeholder: "Ваша повідомлення...",
      send: "Надіслати",
      // Add any additional translations needed
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
      escapeValue: false, // React already protects from XSS
    },
  });

export default i18n;
