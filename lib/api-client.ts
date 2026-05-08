export type GenerateRequest = {
  file: File;
  title: string;
  subtitle: string;
  memberLine: string;
  token: string;
};

export type GenerateResult = {
  blob: Blob;
  filename: string;
  slideCount: number | null;
};

export class GenerateError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "GenerateError";
  }
}

const FILENAME_RE = /filename="([^"]+)"/;

function fallbackFilename(title: string): string {
  const safe = title.replace(/[^\w\-가-힣]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 60);
  return `${safe || "deck"}.pptx`;
}

export async function generateDeck(req: GenerateRequest): Promise<GenerateResult> {
  const formData = new FormData();
  formData.append("file", req.file);
  formData.append("title", req.title);
  formData.append("subtitle", req.subtitle);
  formData.append("member_line", req.memberLine);

  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { Authorization: `Bearer ${req.token}` },
    body: formData,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (body?.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      try {
        detail = (await response.text()) || detail;
      } catch {
        // swallow
      }
    }
    throw new GenerateError(response.status, detail);
  }

  const disposition = response.headers.get("Content-Disposition") ?? "";
  const match = FILENAME_RE.exec(disposition);
  const filename = match?.[1] ? decodeURIComponent(match[1]) : fallbackFilename(req.title);

  const slideCountHeader = response.headers.get("X-Slide-Count");
  const slideCount = slideCountHeader ? Number.parseInt(slideCountHeader, 10) : null;

  const blob = await response.blob();
  return { blob, filename, slideCount };
}

export function triggerDownload(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
