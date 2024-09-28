import ChatbotComponent from "@/components/ChatbotComponent";
import FormView from "@/components/FormView";

export default function Home() {
  return (
    <main className="flex w-full h-screen">
      <div className="w-1/2 h-full bg-secondary">
        <FormView />
      </div>
      <div className="w-1/2 h-full bg-gray">
        <ChatbotComponent />
      </div>
    </main>
  );
}
