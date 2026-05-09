# Density Caps & Overflow Policy

> 본 문서는 슬라이드 한 장의 분량 한계와 본문 overflow 처리 정책을 정의한다.
> `design_system.md`의 *Body Density Strategy*가 "어떻게 채울지"를 다루는 반면,
> 본 문서는 "얼마까지만 채울 수 있는지"의 하드 캡과 그 캡을 넘었을 때의 동작을 정의한다.

## 1. 한 슬라이드 하드 캡 (기획 단계 — Pydantic validator)

`api/_lib/schema.py`의 `Slide` 모델은 다음 4개 캡을 강제한다. 어느 하나라도 위반하면
`ValidationError`로 슬라이드 생성이 중단되며, 작성자(LLM 또는 사람)는 슬라이드를 분할하거나
내용을 줄여야 한다.

| 캡 | 한도 | 측정 대상 | 위반 시 |
|---|---|---|---|
| **본문 총 글자 수** | ≤ 1,100자 | 모든 블록의 `text` 합 (헤딩/단락/리스트/캡션 텍스트 포함; `gap` 제외) | `ValidationError("본문 총 글자 N > 1100")` |
| **헤딩(`h`) 블록 수** | ≤ 4 | `kind == "h"` 블록 개수 | `ValidationError("헤딩 블록 N > 4")` |
| **리스트 아이템(`li`) 수** | ≤ 9 | `kind == "li"` 블록 개수 | `ValidationError("리스트 아이템 N > 9")` |
| **단락 평균 길이** | ≤ 180자 | `kind == "p"` 블록 텍스트 평균 길이 (블록이 0개면 검사 생략) | `ValidationError("단락 평균 N > 180")` |

**왜 이 4개인가:**
- 본문 총 글자 — 본문 영역(13.09" × 5.58")이 18pt ExtraLight 한국어로 수용 가능한 대략적 상한.
- 헤딩 ≤ 4 — *한 슬라이드 = 한 덩어리* 원칙상 sub-section은 최대 3~4개. 그 이상이면 슬라이드 분리 신호.
- 리스트 ≤ 9 — 9개를 넘으면 시청자가 한눈에 파악할 수 없음. 분리하거나 표로 전환.
- 단락 평균 ≤ 180 — 평균이 180을 초과하면 한 단락이 4줄을 넘기므로 본문이 산만해진다.

**캡은 한도이지 목표가 아니다.** 평균 슬라이드는 캡의 60~70% 수준에서 머무는 것이 이상적이다.

## 2. 자동 축소 (렌더 단계 — `engine.py`)

`api/_lib/engine.py:build_content`는 슬라이드 본문을 그리기 전 추정 높이를 계산하여
필요 시 본문 폰트 크기를 자동으로 줄인다. 캡 ① 통과 후의 *2차 안전망*이다.

**축소 사다리 (head_size, body_size 쌍):**

| 단계 | head_size | body_size | 비고 |
|---|---|---|---|
| 기본 | 20pt | 18pt | `design_system.md`의 권장 |
| 1단 축소 | 18pt | 16pt | 본문이 살짝 넘칠 때 |
| 2단 축소 | 16pt | 14pt | 마지막 가능 단계 — 더 줄이지 않음 |

**알고리즘 (`engine._fit_body_size`):**
1. body_size = 18pt로 추정 높이 계산.
2. 추정 ≤ body_h(=5.58") 이면 그대로 사용.
3. 초과 시 body_size = 16pt 재시도.
4. 그래도 초과 시 body_size = 14pt 재시도.
5. 14pt에서도 초과면 `SlideOverflowError`(아래 §3) raise.

**높이 추정 휴리스틱 (`engine._estimate_blocks_height`):**
- 한국어/CJK 글자: `font_size × 1.0` (em-square)
- 라틴 알파벳/숫자: `font_size × 0.55`
- 그 외 구두점·기호: `font_size × 0.50`
- 한 줄 너비 = box_w_pt; 줄 수 = `ceil(총 글자 너비 / 한 줄 너비)`
- 줄 높이 = `font_size × 1.18` (line_spacing)
- 블록별 `space_before`/`space_after` 추가
- 약 ±10% 오차 — 보수적으로 추정해 false-overflow를 false-pass보다 선호한다.

**블록의 명시 `size`는 자동 축소 대상이 아니다.** `caption.size = 12` 처럼 작성자가
직접 지정한 크기는 축소 사다리와 무관하게 그대로 유지된다.

## 3. Overflow 오류 — Fail-Fast

```python
class SlideOverflowError(Exception):
    """슬라이드 본문이 14pt까지 줄여도 본문 영역에 들어가지 않을 때 raise."""
```

**오류 메시지 형식 (한국어, 사람·LLM 모두 진단 가능):**

```
슬라이드 'N. Section Name' 본문 추정 높이 X.XX" > 본문 최대 Y.YY".
14pt까지 줄여도 안 맞음 — 슬라이드를 분할하거나 본문을 줄여 주세요.
```

**대응 절차:**
1. 슬라이드 제목·부제로 어떤 슬라이드인지 식별한다.
2. `slide_planning.md`의 *Stage 2 — Slide Plan*으로 돌아가 해당 슬라이드를 두 장으로 분할한다.
3. 분할 후 각 슬라이드의 `one_idea`가 명확히 다른지 검증한다 (그렇지 않으면 단순 텍스트 축약이 더 적절).
4. 다시 Stage 3을 돌려 새 `Slide` 객체를 생성한다.

**침묵 overflow는 절대 허용하지 않는다.** PowerPoint는 본문이 슬라이드를 벗어나도 오류를
발생시키지 않으므로, 렌더 단계에서 명시적으로 fail-fast하지 않으면 결함 슬라이드가
사용자에게 그대로 전달된다.

## 4. 캡 위반의 흔한 원인 & 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 본문 글자 > 1,100 | 한 슬라이드에 두 sub-section이 합쳐짐 | Stage 2에서 두 슬라이드로 분할 |
| 헤딩 > 4 | 작은 단위 sub-heading을 남발함 | 일부 헤딩을 본문 첫 문장으로 흡수 |
| 리스트 > 9 | 항목별 1줄짜리를 나열만 함 | 데이터 표 또는 두 슬라이드 분할 |
| 단락 평균 > 180 | 한 단락에 두 가지 이상의 의미가 섞임 | 단락을 분리, 또는 sub-heading + 짧은 단락 두 개로 |
| 14pt까지 줄여도 overflow | 글자 수는 캡 내인데 헤딩·리스트가 너무 많아 spacing 누적 | 헤딩 1개 줄이거나 인접 li를 한 단락으로 통합 |
