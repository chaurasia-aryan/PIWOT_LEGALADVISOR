import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PIWOT \\ LEGAL ADVISOR — Local-First Contract Intelligence",
  description: "Offline-capable legal contract analysis, clause classification, and explainable risk quantification.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="bg-canvas">
      <body className={`${inter.className} bg-canvas text-ink min-h-screen flex flex-col antialiased selection:bg-surface-warm selection:text-ink`}>
        <Navbar />
        <main className="flex-1 w-full">
          {children}
        </main>
      </body>
    </html>
  );
}
