"use client";

import { useState } from "react";

import { DownloadCard } from "@/components/DownloadCard";
import { ProgressView } from "@/components/ProgressView";
import { UploadForm, type UploadFormValues } from "@/components/UploadForm";
import { generateDeck, GenerateError, type GenerateResult } from "@/lib/api-client";

type Phase =
  | { kind: "idle" }
  | { kind: "generating" }
  | { kind: "done"; result: GenerateResult; sourceTitle: string }
  | { kind: "error"; message: string };

export default function Page() {
  const [phase, setPhase] = useState<Phase>({ kind: "idle" });

  async function handleSubmit(values: UploadFormValues) {
    setPhase({ kind: "generating" });
    try {
      const result = await generateDeck({
        file: values.file,
        title: values.title,
        subtitle: values.subtitle,
        memberLine: values.memberLine,
        token: values.token,
      });
      setPhase({ kind: "done", result, sourceTitle: values.title });
    } catch (e) {
      const message =
        e instanceof GenerateError
          ? `${e.status} — ${e.message}`
          : e instanceof Error
            ? e.message
            : "알 수 없는 오류가 발생했습니다.";
      setPhase({ kind: "error", message });
    }
  }

  function reset() {
    setPhase({ kind: "idle" });
  }

  return (
    <main className="min-h-screen flex flex-col items-center px-6 py-16">
      <div className="w-full max-w-xl">
        <header className="mb-10">
          <h1 className="text-3xl font-bold text-[#122B46] tracking-tight">
            Y-PJ-FoRM 발표자료 생성기
          </h1>
          <p className="mt-2 text-sm text-[#7A7A7A] leading-relaxed">
            프로젝트 내용을 정리한 PDF 또는 DOCX 파일을 업로드하면 학회
            템플릿에 맞추어 PPTX 를 자동으로 생성합니다.
          </p>
        </header>

        {phase.kind === "idle" && <UploadForm onSubmit={handleSubmit} />}

        {phase.kind === "generating" && <ProgressView />}

        {phase.kind === "done" && (
          <DownloadCard
            result={phase.result}
            sourceTitle={phase.sourceTitle}
            onAgain={reset}
          />
        )}

        {phase.kind === "error" && (
          <section className="rounded border border-[#C00000]/30 bg-[#C00000]/5 p-6">
            <h2 className="text-base font-bold text-[#C00000]">생성 실패</h2>
            <p className="mt-2 text-sm text-[#000] whitespace-pre-wrap break-words">
              {phase.message}
            </p>
            <button
              type="button"
              onClick={reset}
              className="mt-4 rounded border border-[#122B46] bg-white px-4 py-2 text-sm font-bold text-[#122B46] transition hover:bg-[#122B46] hover:text-white"
            >
              다시 시도
            </button>
          </section>
        )}

        <footer className="mt-10 text-xs text-[#7A7A7A]">
          학회원 전용 · 사전공유 토큰 인증
        </footer>
      </div>
    </main>
  );
}
