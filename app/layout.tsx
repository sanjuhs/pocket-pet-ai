import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { headers } from "next/headers";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host") ?? "localhost:3000";
  const protocol = requestHeaders.get("x-forwarded-proto") ?? (host.startsWith("localhost") ? "http" : "https");
  const base = new URL(`${protocol}://${host}`);
  const image = new URL("/og.png", base).toString();

  return {
    metadataBase: base,
    title: { default: "Pocket Pet AI — Private intelligence, physically yours", template: "%s · Pocket Pet AI" },
    description: "An open architecture for a frozen-model, low-bit, wearable personal AI that speaks, remembers, and acts locally.",
    keywords: ["edge AI", "ternary transformer", "wearable AI", "private AI", "FPGA inference", "BitNet"],
    icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
    openGraph: { title: "Pocket Pet AI", description: "A personal AI with a pulse — private, local, and physically yours.", type: "website", images: [{ url: image, width: 1730, height: 909, alt: "Pocket Pet AI private wearable intelligence system" }] },
    twitter: { card: "summary_large_image", title: "Pocket Pet AI", description: "Private intelligence, physically yours.", images: [image] },
  };
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className={`${geistSans.variable} ${geistMono.variable}`}>{children}</body></html>;
}
