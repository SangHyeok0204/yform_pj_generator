"use client";

import { useEffect, useState } from "react";

const STAGES: { atSec: number; message: string }[] = [
  { atSec: 0, message: "논문 텍스트를 추출하는 중..." },
  { atSec: 8, message: "Claude Opus 4.7이 슬라이드 구조를 분석하는 중..." },
  { atSec: 60, message: "슬라이드별 본문을 채우는 중..." },
  { atSec: 180, message: "마무리 정리 중... (3~5분 소요됩니다)" },
  { atSec: 360, message: "거의 다 됐습니다... 잠시만 더 기다려주세요." },
];

function formatElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return m > 0 ? `${m}분 ${s.toString().padStart(2, "0")}초` : `${s}초`;
}

export function ProgressView() {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const start = Date.now();
    const id = window.setInterval(() => {
      setElapsed(Math.floor((Date.now() - start) / 1000));
    }, 1000);
    return () => window.clearInterval(id);
  }, []);

  const currentStage = [...STAGES].reverse().find((s) => elapsed >= s.atSec) ?? STAGES[0];

  return (
    <section className="rounded border border-[#E0E0E0] bg-white p-8 text-center">
      <div className="mx-auto mb-5 h-10 w-10 animate-spin rounded-full border-4 border-[#E0E0E0] border-t-[#122B46]" />
      <p className="text-sm font-bold text-[#122B46]">{currentStage.message}</p>
      <p className="mt-2 text-xs text-[#7A7A7A]">경과: {formatElapsed(elapsed)}</p>
      <p className="mt-6 text-xs text-[#7A7A7A] leading-relaxed">
        Opus 4.7이 디자인 시스템에 맞춰 7~9장의 본문 슬라이드를 작성합니다.
        <br />
        창을 닫지 말고 잠시만 기다려주세요.
      </p>
    </section>
  );
}
