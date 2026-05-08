"use client";

import { triggerDownload, type GenerateResult } from "@/lib/api-client";

type Props = {
  result: GenerateResult;
  sourceTitle: string;
  onAgain: () => void;
};

export function DownloadCard({ result, sourceTitle, onAgain }: Props) {
  function handleDownload() {
    triggerDownload(result.blob, result.filename);
  }

  const sizeMB = (result.blob.size / (1024 * 1024)).toFixed(1);

  return (
    <section className="rounded border border-[#E0E0E0] bg-white p-8">
      <h2 className="text-lg font-bold text-[#122B46]">생성 완료</h2>
      <p className="mt-1 text-sm text-[#7A7A7A]">
        &quot;{sourceTitle}&quot; deck이 준비되었습니다.
      </p>

      <dl className="mt-5 space-y-2 text-sm">
        <Row k="파일명" v={result.filename} />
        <Row k="크기" v={`${sizeMB} MB`} />
        {result.slideCount && <Row k="슬라이드 수" v={`${result.slideCount}장`} />}
      </dl>

      <div className="mt-6 flex flex-col gap-2 sm:flex-row">
        <button
          type="button"
          onClick={handleDownload}
          className="flex-1 rounded bg-[#122B46] px-4 py-3 font-bold text-white transition hover:bg-[#1d3e5e]"
        >
          PPTX 다운로드
        </button>
        <button
          type="button"
          onClick={onAgain}
          className="flex-1 rounded border border-[#122B46] bg-white px-4 py-3 font-bold text-[#122B46] transition hover:bg-[#122B46] hover:text-white"
        >
          새로 만들기
        </button>
      </div>

      <p className="mt-6 text-xs text-[#7A7A7A] leading-relaxed">
        💡 PowerPoint에서 열어 폰트가 맞지 않으면, <code>public/fonts/</code>의
        Pretendard 9종을 설치하거나 학회 공유 폴더에서 받아 설치하세요.
      </p>
    </section>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex">
      <dt className="w-24 text-[#7A7A7A]">{k}</dt>
      <dd className="text-[#000]">{v}</dd>
    </div>
  );
}
