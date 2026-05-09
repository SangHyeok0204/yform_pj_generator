# Slide Planning Pipeline — 3 Stages

> **Use:** 본 문서는 원문(논문·노트·docx)에서 PPTX 한 벌을 만들 때의
> 3단계 기획·작성 절차를 정의한다. `design_system.md`가 시각 계약을,
> `density_caps.md`가 분량 한계를 정한다면, 본 문서는 *그 둘 사이의
> 콘텐츠 설계 절차*를 정의한다.
>
> **핵심 원칙: 한 슬라이드 = 한 덩어리.** 한 슬라이드는 단 하나의 메시지(one_idea)를
> 전달한다. 두 가지를 전달하고 싶다면 두 장으로 분할한다.

## 파이프라인 한눈에

```
원문 (docx/pdf/text)
    │
    ▼
[Stage 1] Outline       → DeckPlan.sections : list[SectionOutline]
    │                     - 큰 번호 섹션과 각 섹션 권장 페이지 수 결정
    ▼
[Stage 2] Slide Plan    → DeckPlan.slides : list[SlidePlan]
    │                     - 섹션 안 슬라이드별 제목·부제·one_idea 결정
    ▼
[Stage 3] Content Fill  → DeckContent.slides : list[Slide]
                          - 각 SlidePlan을 blocks[]로 확장 (캡 준수)
```

각 단계의 결과물은 `api/_lib/schema.py`에 정의된 Pydantic 모델로 표현되며,
사람이 중간 단계에 개입해 검토·수정할 수 있다.

## Stage 1 — Outline (큰 목차 도출)

**입력:** 원문 텍스트, 표지 메타데이터(`title`, `subtitle`, `member_line`).

**출력:** `list[SectionOutline]`
```python
class SectionOutline(BaseModel):
    n: int                # 1, 2, 3, ...  — TOC 번호
    title_en: str         # "Methodology"  (영문 — section-title slot에 그대로 사용)
    summary: str          # 무엇을 다루는 섹션인가 (1~2문장 한국어)
    target_slides: int    # 권장 페이지 수 (3~8 권장; 1·2도 허용하나 합치는 것을 우선 검토)
```

**규칙:**
1. 섹션 수는 5~8개를 기본으로 한다. `Overview`(개요), `Conclusion`(결론), `Appendix`(부록)는 거의 항상 포함.
2. 각 섹션 `target_slides`는 **3~6장이 권장 범위**. 3장 미만이면 인접 섹션과 합치고, 8장 초과면 두 섹션으로 분할한다.
3. `title_en`은 짧고 명확한 영문 명사구. 마침표 없음. (예: `Methodology`, `Result`, `Prior Research`)
4. `summary`는 LLM 자기 점검용 — 슬라이드 본문에는 직접 쓰이지 않는다.
5. 전체 슬라이드 수 추정: `cover(1) + toc(1) + Σ target_slides`. 통상 20~35장이 적정.

**TOC와의 관계:** `SectionOutline.title_en` 목록이 곧 TOC 항목이 된다.

## Stage 2 — Slide Plan (섹션 → 페이지 배분)

**입력:** Stage 1의 `list[SectionOutline]` + 원문 텍스트.

**출력:** `list[SlidePlan]`
```python
class SlidePlan(BaseModel):
    section_n: int                # 소속 섹션 번호 (1, 2, ...)
    slide_idx_in_section: int     # 섹션 내 1, 2, 3 ...
    title: str                    # "N. Section Name" — 영문 그대로
    subtitle: str                 # "N.M Sub-section Name — 짧은 설명"
    one_idea: str                 # 이 슬라이드가 전달할 단 하나의 메시지 (한국어 1~2문장)
    source_refs: list[str]        # 원문 단락 번호·페이지 번호 등 출처
```

**규칙:**

1. **한 슬라이드 = 한 덩어리.** `one_idea`는 단일 명제로 작성한다.
   - ✓ "Net Delta는 계약 수가 아닌 delta 가중 노출이 실제 리스크 단위임을 S&S Theorem 2가 증명한다."
   - ✗ "Net Delta 정의와 다중 호가 워터폴, 그리고 즉시 체결 메커니즘을 설명한다." (세 덩어리 — 분할 필요)

2. **부제 번호 규칙.** `subtitle`은 `N.M ...` 형태이고 같은 섹션의 슬라이드들은
   M 번호가 단조 증가한다 (예: `4.1`, `4.2`, `4.2`(이어서), `4.3`). 한 sub-section이
   한 슬라이드에 안 들어가면 같은 `4.2`로 분할 슬라이드를 두 장 둔다.

3. **`title`은 영문 섹션 제목 그대로.** `4. Methodology` 처럼 번호+제목 형식.
   섹션이 끝나는 마지막 슬라이드까지 동일한 `title`이 유지된다.

4. **`source_refs`는 추적용.** 본문 작성 시 LLM이 어느 출처에서 끌어올지 알도록
   docx 단락 번호(`[042]`), pdf 페이지(`p.7`), 외부 URL 등을 적는다.

5. **검증 휴리스틱 (Stage 2 종료 시 권장 점검):**
   - 같은 sub-section에 슬라이드가 3장 이상 → 정말 분할이 필요한지 재검토.
   - 같은 섹션의 슬라이드 수가 9 이상 → 섹션 분할 검토.
   - 한 섹션의 첫 슬라이드 부제가 `N.1`이 아닐 경우 → 번호 누락 점검.

## Stage 3 — Content Fill (블록 확장)

**입력:** Stage 2의 단일 `SlidePlan`.

**출력:** 단일 `Slide`
```python
class Slide(BaseModel):
    title: str
    subtitle: Optional[str]
    blocks: list[Block]  # h, p, li, gap, caption
```

**규칙:**

1. **`one_idea`만 풀어낸다.** Stage 2의 `one_idea`를 lead 단락(또는 첫 헤딩)으로
   삼고, 나머지 블록은 그 명제를 뒷받침하거나 구체화한다. 다른 sub-section의
   내용은 절대 끼워 넣지 않는다.

2. **블록 사용 패턴 (권장):**
   - **단일 명제 + 근거.** lead `p` → 1~3개 sub-heading(`h`) + 각 헤딩 아래 1~2개 `p` 또는 `li`.
   - **번호 단계.** `h` → 3~5개 `li` (num="1.", "2.", ...)
   - **데이터 한 장.** lead `p` + `caption` (그림·표 placeholder).
   - 카드/박스/색칠 박스 등 시각 요소를 default scaffolding으로 쓰지 않는다.
     (`design_system.md`의 *Density Tactics* 참조)

3. **분량 캡 엄수.** `density_caps.md`의 4개 캡(글자 1100·헤딩 4·리스트 9·단락 평균 180)을
   준수한다. Pydantic validator가 자동 검증한다.

4. **자동 축소 활용.** 본문이 살짝 넘치면 `engine`이 18→16→14pt로 자동 축소한다.
   이를 활용해 18pt 한계까지만 채우려 하지 말고, 실제 메시지가 요구하는 분량으로 작성한다.

5. **빨강 금지·로고 금지·페이지 번호 금지** — `design_system.md`의 모든 금지 규칙은 본 단계에서도 동일.

## 단계 간 일관성

- **Stage 1 → 2:** `SectionOutline.target_slides`는 Stage 2에서 만들어진 SlidePlan 개수와 정확히 일치해야 한다. (강제 검증)
- **Stage 2 → 3:** 각 `SlidePlan`은 정확히 하나의 `Slide`로 확장된다. 분할이 필요하면 Stage 2로 돌아간다.
- **Stage 3 → render:** 모든 `Slide`가 `density_caps.md`의 캡을 통과해야 `DeckContent`가 만들어진다.

## 사람·LLM 협업 모델

| 단계 | 사람의 역할 | LLM의 역할 |
|---|---|---|
| Stage 1 | 섹션 수·이름 검토. 잘못된 분류 수정. | 원문에서 자연 섹션 도출, target_slides 제안. |
| Stage 2 | one_idea의 단일성 검토. 슬라이드 수 조정. | sub-section 분할 제안, 슬라이드별 핵심 명제 작성. |
| Stage 3 | 분량·표현 다듬기. | SlidePlan을 blocks[]로 충실히 확장 (캡 준수). |

**규칙:** 어느 단계든 결과가 마음에 들지 않으면 *그 단계로 돌아가서* 다시 한다.
중간 단계가 명시적이므로 LLM 호출 비용·시간을 최소화하며 반복할 수 있다.

## 빠른 참조 — 슬라이드 분할 신호

다음 신호가 한 슬라이드에서 둘 이상 나타나면 분할을 검토한다:

- 본문 글자 > 800 (캡 1100의 70%)
- 헤딩 > 3
- 리스트 > 7
- `one_idea`가 "그리고", "또한", "더불어"로 두 명제를 잇고 있음
- sub-section 번호(`N.M`)가 한 슬라이드 안에서 바뀜
