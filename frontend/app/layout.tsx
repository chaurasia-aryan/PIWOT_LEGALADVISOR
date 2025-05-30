import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
	title: "Contract Management Dashboard",
	description: "AI-powered contract analysis and management system",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode
}) {
	return (
		<html lang="en">
			<body className={`${inter.className} bg-neutral-900 text-white min-h-screen`}>
				<main className="container mx-auto px-4 py-8">
					{children}
				</main>
			</body>
		</html>
	);
}
