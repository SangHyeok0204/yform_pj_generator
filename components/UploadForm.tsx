"use client";

import { useEffect, useRef, useState } from "react";

const TOKEN_STORAGE_KEY = "ypjform.siteToken";

export type UploadFormValues = {
  file: File;
  title: string;
  subtitle: string;
  memberLine: string;
  token: string;
};

type Props = {
  onSubmit: (values: UploadFormValues) => void;
  disabled?: boolean;
};

export function UploadForm({ onSubmit, disabled }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [subtitle, setSubtitle] = useState("");
  const [memberLine, setMemberLine] = useState("");
  const [token, setToken] = useState("");
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const saved = window.localStorage.getItem(TOKEN_STORAGE_KEY);
    if (saved) setToken(saved);
  }, []);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (disabled) return;
    if (!file) {
      setError("파일을 선택해주세요.");
      return;
    }
    const filename = file.name.toLowerCase();
    if (!filename.endsWith(".pdf") && !filename.endsWith(".docx")) {
      setError(".pdf 또는 .docx 파일만 업로드할 수 있습니다.");
      return;
    }
    if (!title.trim() || !subtitle.trim() || !memberLine.trim() || !token.trim()) {
      setError("모든 항목을 입력해주세요.");
      return;
    }
    setError(null);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, token.trim());
    }
    onSubmit({
      file,
      title: title.trim(),
      subtitle: subtitle.trim(),
      memberLine: memberLine.trim(),
      token: token.trim(),
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <Field label="발표 제목" hint="표지 큰 글씨로 들어갑니다.">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="발표 제목을 넣어주세요"
          className="input"
          disabled={disabled}
        />
      </Field>

      <Field label="부제 (한 줄 설명)">
        <input
          type="text"
          value={subtitle}
          onChange={(e) => setSubtitle(e.target.value)}
          placeholder="부제를 넣어주세요"
          className="input"
          disabled={disabled}
        />
      </Field>

      <Field label="멤버 라인" hint="저자 / 발표자 / Reviewed by">
        <input
          type="text"
          value={memberLine}
          onChange={(e) => setMemberLine(e.target.value)}
          placeholder="38기 박상혁, 38기 이태주"
          className="input"
          disabled={disabled}
        />
      </Field>

      <Field label="논문 파일" hint=".pdf 또는 .docx (4 MB 이내 권장)">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="block w-full text-sm text-[#7A7A7A] file:mr-4 file:rounded file:border-0 file:bg-[#122B46] file:px-4 file:py-2 file:text-white file:cursor-pointer hover:file:bg-[#1d3e5e]"
          disabled={disabled}
        />
        {file && (
          <p className="mt-1 text-xs text-[#7A7A7A]">
            선택됨: {file.name} ({(file.size / 1024).toFixed(1)} KB)
          </p>
        )}
      </Field>

      <Field label="사전공유 토큰" hint="학회에서 받은 토큰. 한 번 입력하면 브라우저에 저장됩니다.">
        <input
          type="password"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="••••••••"
          className="input"
          disabled={disabled}
          autoComplete="off"
        />
      </Field>

      {error && (
        <p className="rounded border border-[#C00000]/30 bg-[#C00000]/5 px-3 py-2 text-sm text-[#C00000]">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={disabled}
        className="rounded bg-[#122B46] px-6 py-3 font-bold text-white transition hover:bg-[#1d3e5e] disabled:cursor-not-allowed disabled:opacity-50"
      >
        {disabled ? "생성 중..." : "개쩌는 딸깍 PPTX 생성 버튼"}
      </button>

      <style jsx>{`
        .input {
          display: block;
          width: 100%;
          border-radius: 0.25rem;
          border: 1px solid #e0e0e0;
          padding: 0.5rem 0.75rem;
          font-size: 0.95rem;
          color: #000;
          background: #fff;
        }
        .input:focus {
          outline: none;
          border-color: #122b46;
        }
      `}</style>
    </form>
  );
}

function Field({
  label,
  hint,
  children,
}: {
  label: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="block text-sm font-bold text-[#122B46]">{label}</span>
      {hint && <span className="block text-xs text-[#7A7A7A] mt-0.5 mb-1.5">{hint}</span>}
      {children}
    </label>
  );
}
