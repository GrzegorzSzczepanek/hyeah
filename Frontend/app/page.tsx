import ChatbotComponent from "@/components/ChatbotComponent";
import FormView from "@/components/FormView";

export default function Home() {
  return (
    <main className="flex w-full" style={{ height: "calc(100vh - 56px)" }}>
      <div className="w-1/2 flex flex-col bg-secondary ">
        <FormView />
      </div>
      <div className="w-1/2 flex flex-col bg-gray overflow-hidden">
        <ChatbotComponent />
      </div>
    </main>
  );
}
