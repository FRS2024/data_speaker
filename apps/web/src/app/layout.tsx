import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "data_speaker — Autonomous Conversational Data Analyst",
  description: "Enterprise Code-Interpreting Autonomous Analyst with Stateful Sandbox Execution and Real-Time Interactive Visualizations",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark h-full">
      <body className="h-full bg-studio-bg text-studio-text antialiased overflow-hidden">
        {children}
      </body>
    </html>
  );
}
