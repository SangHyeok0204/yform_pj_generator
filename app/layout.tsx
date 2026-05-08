import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Y-PJ-FoRM 발표자료 생성기",
  description:
    "논문 PDF·DOCX를 학회 공통 템플릿 기반 PPTX로 자동 변환합니다.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
