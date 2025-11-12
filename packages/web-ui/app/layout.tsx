import type { Metadata } from "next";
import "./globals.css";
import Providers from "./providers";
import Navbar from "../components/Navbar";

export const metadata: Metadata = {
  title: "Project Orchestra",
  description: "Personal AI Command Center",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="bg-slate-950 text-slate-100">
      <body className="min-h-screen antialiased">
        <Providers>
          <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1 px-4 py-10 sm:px-8 lg:px-16">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
