"""Build the KOSPI200 Option Market Making deck from the docx outline.

Reads samples/kospi200_mm_project_outline.docx, derives slide structure,
and emits a PPTX matching reference/master_deck_1.pptx (cover + TOC) and
the design_system.md anchors for content slides.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api._lib.engine import render_deck
from api._lib.schema import (
    CaptionBlock,
    Cover,
    DeckContent,
    GapBlock,
    HeadingBlock,
    ListItemBlock,
    ParagraphBlock,
    Slide,
)


def H(text: str, size: int | None = None) -> HeadingBlock:
    return HeadingBlock(text=text, size=size)


def P(text: str, size: int | None = None) -> ParagraphBlock:
    return ParagraphBlock(text=text, size=size)


def LI(text: str, num: str | None = None, label: str | None = None, size: int | None = None) -> ListItemBlock:
    return ListItemBlock(num=num, label=label, text=text, size=size)


def G(pt: int = 6) -> GapBlock:
    return GapBlock(pt=pt)


def C(text: str, size: int | None = None) -> CaptionBlock:
    return CaptionBlock(text=text, size=size)


# ============================================================
# Cover + TOC
# ============================================================
COVER = Cover(
    title="KOSPI200 Options Market Making",
    subtitle="KOSPI200 ATM 옵션 시장조성 — A-S(2008) Net Delta 확장 시뮬레이션",
    member_line="Y-FoRM 39th 박상혁",
)

TOC = [
    "Overview",
    "Market Making Mechanism",
    "Prior Research",
    "Methodology",
    "Result",
    "Conclusion",
    "Appendix",
]

# ============================================================
# 1. Overview — 1 slide
# ============================================================
SLIDE_1_OVERVIEW = Slide(
    title="1. Overview",
    subtitle="1.1 연구 동기 & 핵심 기여",
    blocks=[
        H("연구 배경"),
        P("KOSPI200 ATM 옵션 Market Making 환경에서 Avellaneda–Stoikov(2008) 모델을 현실화할 때 어떤 요소를 바꿔야 하는지를 정량적으로 검증한다."),
        G(4),
        H("이론 기반"),
        P("A-S(2008) 원논문 + Stoikov & Saglam(2009) Net Delta 이론 + Muravyev(2025) KOSPI200 OMM 실증을 단일 시뮬레이터에 통합한다."),
        G(4),
        H("핵심 기여"),
        LI("Net Delta 기반 재고 측정으로 RP(Reservation Price) 조정의 정밀화", num="1."),
        LI("3×3 다중 호가 레벨과 워터폴 체결 로직으로 재고 해소 속도 향상", num="2."),
        LI("방향성 Bucket 체결 모델로 추세 시장에서의 재고 자연 해소 구현", num="3."),
        LI("즉시체결(δ≤0)과 mid price 집행을 통한 누적 재고 즉시 해소 구현", num="4."),
        G(4),
        H("논의 중"),
        P("동적 σ 설정 — 장 막판 (T−t)→0 시 재고 조정력이 소멸하는 구조적 한계의 해결 방안 검토 중."),
    ],
)

# ============================================================
# 2. Market Making Mechanism — 4 slides
# ============================================================
SLIDE_2_1 = Slide(
    title="2. Market Making Mechanism",
    subtitle="2.1 MM / LP의 역할과 수익 구조",
    blocks=[
        H("역할"),
        P("bid·ask 양방향 호가를 상시 제시하여 거래 상대방 없이도 즉시 거래가 성사되도록 시장 유동성과 적정가격을 형성한다. KRX는 시장조성자에게 호가 제출 빈도, 허용 최대 스프레드, 의무 위반 시 패널티를 명시적으로 부과한다."),
        G(6),
        H("수익 구조"),
        P("양방향 호가가 동시에 체결되면 (ask 체결가 − bid 체결가)만큼의 스프레드가 수익으로 누적된다. 하루 수백~수천 회 반복되며 누적된다."),
        LI("ATM 콜옵션 mid=5.00pt → bid 4.95 / ask 5.05 제시 → 양방향 체결 시 +0.10pt = 1,000원/계약", label="예시"),
        G(6),
        H("현실의 어려움"),
        P("한쪽 방향만 체결되면 재고가 누적되어 방향성 노출이 발생하고, 시장이 추세적으로 움직일 때 P&L 변동성이 폭발적으로 증가한다. 따라서 MM의 핵심 과제는 스프레드 수익 추구와 재고 리스크 관리의 동시 달성이다."),
    ],
)

SLIDE_2_2 = Slide(
    title="2. Market Making Mechanism",
    subtitle="2.2 KOSPI200 옵션 시장 — 상품 구조와 유동성",
    blocks=[
        H("기본 상품 구조"),
        LI("기초자산 KOSPI200 지수 / 계약 승수 250,000원/pt / 결제 방식 현금 결제", num="·"),
        LI("만기 매월 두 번째 목요일 — 연간 12개 만기 + 장기 옵션 존재", num="·"),
        LI("행사가 2.5pt 간격 — 지수 수준에 따라 행사가 범위가 동적으로 조정", num="·"),
        G(6),
        H("Tick Size 구조"),
        P("옵션 가격 3pt 이상은 0.05pt(=KRW 12,500/tick), 3pt 미만은 0.01pt가 적용된다. ATM 옵션은 통상 3pt 이상 영역에서 거래되어 0.05pt tick이 사용된다."),
        G(6),
        H("시장 규모와 ATM 집중"),
        P("KOSPI200 옵션은 글로벌 최상위 거래량 옵션 시장 중 하나이며 OMM 43개사가 활동한다(Muravyev 2025). 높은 유동성 덕분에 초단기 재고 해소가 가능하고, 당일 내 포지션을 정리하는 관행이 형성되어 있다."),
        LI("delta ≈ 0.5로 안정 → Net Delta와 계약 수의 차이가 최소 → 모델 설계 단순화", num="·"),
        LI("ATM 옵션이 가장 거래 활발 → MM 호가 의무 이행이 용이하고 실증 데이터가 풍부", num="·"),
        G(4),
        C("장 운영 시간 09:00~15:30 (6.5h) — 본 프로젝트 T=1 정규화의 실제 기준."),
    ],
)

SLIDE_2_3 = Slide(
    title="2. Market Making Mechanism",
    subtitle="2.3 Inventory Risk — MM 딜레마의 본질",
    blocks=[
        H("핵심 리스크"),
        P("단방향 시장에서는 한쪽 호가만 반복 체결되며 재고가 일방향으로 누적된다. 이 누적이 방향성 노출을 만들고, 추가 가격 변동에 따라 P&L 변동성이 폭발적으로 증가한다."),
        G(6),
        H("시나리오"),
        P("상승장에서 ask만 반복 체결 → 대규모 숏 옵션 재고 → 추가 상승 시 mark-to-market 손실이 급격히 누적되는 비대칭 손실 구조가 형성된다."),
        G(6),
        H("실증 — Muravyev (2025)"),
        P("KOSPI200 OMM이 보유한 재고의 38~48%가 5분 이내에 반전된다는 사실이 직접 관측되었다. 이는 OMM이 얼마나 공격적으로 재고를 즉시 해소하려 하는지에 대한 직접 증거이며, 본 프로젝트의 다중 호가·즉시체결 설계의 실증 근거가 된다."),
    ],
)

SLIDE_2_4 = Slide(
    title="2. Market Making Mechanism",
    subtitle="2.4 옵션 MM의 특수성 — Net Delta와 비헷징 전략",
    blocks=[
        H("주식 MM vs 옵션 MM"),
        P("주식 MM에서는 1계약이 곧 1단위의 방향성 노출이지만(선형, 단순), 옵션 MM에서는 1계약의 노출이 해당 옵션의 delta에 따라 완전히 달라진다."),
        LI("콜 10계약 숏, Δ=0.3 → 노출 3단위 / Δ=0.8 → 노출 8단위 — 같은 계약 수에 2.7배 리스크 차이", label="예시"),
        G(4),
        H("Delta의 동적 변동"),
        P("Delta는 거래가 없어도 Gamma(가격 변동), Charm(시간 경과), Vanna(IV 변화)로 인해 실시간으로 변동한다. 따라서 Net Delta = Σ(계약 수 × 해당 시점 delta)가 실제 방향성 리스크를 측정하는 올바른 단위이다."),
        G(6),
        H("KOSPI200 시장의 비헷징 전략"),
        P("이론적으로 S&S(2009) Theorem 1은 완전 시장(continuous hedge)에서는 재고가 호가에 무관함을 보인다. 역으로 hedge가 어려운 불완전 시장에서는 Net Delta 기반 RP 조정이 최적 전략이 된다."),
        LI("KOSPI200 OMM 43개사 중 39개(91%)가 비헷징 전략 — hedge하는 4개사조차 선물 비중 1.4%에 불과", num="·"),
        LI("호가 조절(RP·Spread)만으로 재고 관리 — 본 프로젝트 설계 방향과 정확히 일치", num="·"),
    ],
)

# ============================================================
# 3. Prior Research — 5 slides
# ============================================================
SLIDE_3_1 = Slide(
    title="3. Prior Research",
    subtitle="3.1 Avellaneda & Stoikov (2008) — 핵심 프레임워크",
    blocks=[
        H("목적함수"),
        P("기대 이윤 극대화 s.t. 재고 리스크 최소화. HJB 방정식을 통해 최적 제어 문제를 풀어 호가 정책을 도출한다."),
        G(6),
        H("모델 가정"),
        LI("가격 동학 dS = σdW (GBM 가정)", num="·"),
        LI("체결 강도 λ(δ) = A·exp(−k·δ) (포아송 프로세스)", num="·"),
        G(6),
        H("Reservation Price"),
        P("r = s − q · γ · σ² · (T−t). 재고 q의 방향과 반대로 내부 기준가격을 이동시켜 호가 비대칭을 만든다."),
        LI("q > 0 (롱) → r < mid → ask가 mid보다 낮게 → 매도 체결 유도", num="·"),
        LI("q < 0 (숏) → r > mid → bid가 mid보다 높게 → 매수 체결 유도", num="·"),
        G(6),
        H("Optimal Spread & 최종 호가"),
        P("S = γσ²(T−t) + (2/γ)·ln(1 + γ/k). 첫째 항은 리스크 보상, 둘째 항은 체결확률 보정이다. 최종 호가는 bid = r − S/2, ask = r + S/2."),
    ],
)

SLIDE_3_2 = Slide(
    title="3. Prior Research",
    subtitle="3.2 A-S 모델의 한계 — 옵션·현실 적용 시 4가지 문제",
    blocks=[
        LI("재고 단위 — 계약 수 q를 사용 → delta 가중치를 무시 → 같은 계약 수여도 실제 리스크가 다름", num="①", label="한계"),
        LI("단일 호가 — 각 방향에 호가 1개뿐 → 실제 MM은 다양한 거리에 복수 호가를 동시 제시", num="②", label="한계"),
        LI("체결 확률 단방향 — λ(δ)는 거리만 반영하고 가격 방향성을 무시 → 추세 시장에서 비현실적", num="③", label="한계"),
        LI("시간 지평 T — 논문은 옵션 만기를 가정 → 실제 OMM은 당일 내 포지션을 대부분 정리함", num="④", label="한계"),
        G(8),
        H("구조적 한계 — 장 막판 조정력 소멸"),
        P("σ 고정 시 (T−t) → 0이 되면 RP 조정량 q·γσ²(T−t) 자체가 0으로 수렴한다. 장 막판 재고가 누적되어 있어도 RP가 mid에 수렴하여 호가 비대칭이 사라지고 재고 해소가 불가능해진다. 이는 본 프로젝트의 동적 σ 논의의 출발점이다."),
    ],
)

SLIDE_3_3 = Slide(
    title="3. Prior Research",
    subtitle="3.3 Stoikov & Saglam (2009) — Net Delta의 이론적 기반",
    blocks=[
        H("배경"),
        P("A-S 원저자 Stoikov가 직접 옵션 MM 설정으로 확장한 후속 논문이다. delta hedge가 불가능한 불완전 시장(incomplete market) 가정을 명시적으로 도입한다."),
        G(6),
        H("Theorem 1 — 완전 시장"),
        P("hedge로 노출을 제거할 수 있는 완전 시장에서는 최적 호가가 재고에 무관하다. 즉, 헷지가 가능하면 RP 조정 자체가 불필요하다는 것을 수학적으로 증명한다."),
        G(6),
        H("Theorem 2 — 불완전 시장"),
        P("hedge가 불가능한 불완전 시장에서는 최적 RP 조정량이 (q_stock + q_option × Δ) = Net Delta에 비례한다."),
        LI("계약 수 q가 아닌 delta 가중 노출이 실제 리스크의 단위임을 수학적으로 증명", num="·"),
        LI("Develop 모드의 RP 수식 r = s − q_delta·γσ²(T−t) 의 직접적 이론 근거", num="·"),
        G(4),
        H("ATM 단순화"),
        P("ATM 영역에서는 Δ ≈ 0.5이므로 Net Delta ≈ q × 0.5 (상수 배 관계)이지만, 이론적 완결성을 위해 Net Delta를 명시적으로 누적·구현한다."),
    ],
)

SLIDE_3_4 = Slide(
    title="3. Prior Research",
    subtitle="3.4 Muravyev et al. (2025) — KOSPI200 OMM 실증",
    blocks=[
        H("연구 환경"),
        P("KOSPI200 OMM 43개사의 실제 주문 흐름을 직접 관측한 working paper이다. 본 프로젝트와 동일한 시장·동일한 상품을 다루어 실증적 직결성이 매우 높다."),
        G(6),
        H("핵심 관측 — 비헷징 전략의 보편성"),
        LI("OMM 43개사 중 39개사(91%)가 비헷징 전략을 채택", num="·"),
        LI("hedge하는 4개사조차 선물 비중이 1.4%에 불과 → 호가 조절이 주된 재고 관리 수단", num="·"),
        G(6),
        H("핵심 관측 — 당일 내 포지션 정리"),
        LI("오버나이트 평균 재고 4,431계약 vs 일중 평균 거래량 206,864계약 → 거래량 대비 0.02% 수준", num="·"),
        LI("→ T = 당일 장 마감 설정의 실증적 근거", num="·"),
        G(6),
        H("기타 관측"),
        P("재고 충격 후 방향성 역체결 비대칭이 관측되어 본 프로젝트의 bucket 승수 모델의 근거가 되며, 옵션 상품명세(Tick size 0.05pt 등)도 직접 인용되어 있다."),
    ],
)

SLIDE_3_5 = Slide(
    title="3. Prior Research",
    subtitle="3.5 선행 연구 → 프로젝트 설계 매핑",
    blocks=[
        H("Net Delta 재고"),
        P("이론적으로 S&S Theorem 2의 Net Delta 결과 + 실증적으로 Muravyev의 OMM delta exposure 관리 관행 — 두 근거 모두 직접 반영. (구현 완료)"),
        G(6),
        H("다중 호가 3×3"),
        P("A-S 한계 ②(단일 호가)의 직접 해결 + 실제 LOB 구조 반영. (구현 완료)"),
        G(6),
        H("방향성 Bucket 체결 확률"),
        P("A-S 한계 ③(단방향 체결)의 직접 해결 + Muravyev 실증의 방향성 비대칭 관측을 모델에 반영. (구현 완료)"),
        G(6),
        H("즉시 체결 + mid price"),
        P("A-S 한계 ③의 보강 — δ ≤ 0 발생 시 즉시 체결 + mid 집행으로 누적 재고를 즉시 해소. (구현 완료)"),
        G(6),
        H("T = 당일 장 마감 + 동적 σ"),
        P("A-S 한계 ④와 구조적 한계의 해결. T = 당일 설정은 Muravyev 실증으로 정당화(구현 완료), 동적 σ는 S&S 장 막판 민감도 논의를 기반으로 검토 중(미정)."),
    ],
)

# ============================================================
# 4. Methodology — 8 slides
# ============================================================
SLIDE_4_1 = Slide(
    title="4. Methodology",
    subtitle="4.1 Paper Baseline — 원논문 충실 재현",
    blocks=[
        H("Baseline 파라미터"),
        P("S₀ = 100, σ = 2.0 (고정), dt = 0.005, n_steps = 200, γ = 0.1, A = 140, k = 1.5. (구현 완료)"),
        G(6),
        H("σ = 2.0 고정 채택 이유"),
        P("KOSPI200 IV ≈ 20% 기반 시 γσ² ≈ 0.006 vs 고정 σ = 2.0일 때 γσ² = 0.4 → 64배 차이. IV 기반은 RP 조정량이 tick size 이하로 수렴하여 의미 있는 호가 조절이 불가능하다."),
        G(6),
        H("재고 정의 & 체결 모델"),
        LI("재고 — 정수 계약 수 q (delta = 1 고정 가정)", num="·"),
        LI("체결 — 기본 포아송 강도 λ(δ) = A·exp(−k·δ) 단일 호가", num="·"),
        G(6),
        H("Baseline의 역할"),
        P("Develop 모드의 4가지 확장(Net Delta, 다중 호가, Bucket, 즉시체결)이 만들어내는 차이를 정량적으로 측정하기 위한 비교 기준선을 확보하기 위한 충실 재현 단계이다."),
    ],
)

SLIDE_4_2 = Slide(
    title="4. Methodology",
    subtitle="4.2 Develop ① Net Delta 재고 — S&S Theorem 2 구현",
    blocks=[
        H("이중 상태 추적"),
        P("두 가지 상태를 병렬로 추적한다 — contracts(정수 계약 수)와 net_delta(실수 delta 노출)."),
        LI("bid 체결 시 — contracts += 1, net_delta += option_delta_at_fill", num="·"),
        LI("ask 체결 시 — contracts -= 1, net_delta -= option_delta_at_fill", num="·"),
        G(6),
        H("RP 수식 변경"),
        P("Paper r = s − q·γσ²τ → Develop r = s − q_delta·γσ²τ. S&S Theorem 2가 직접 정당화하는 변경이다."),
        G(6),
        H("ATM 시나리오 예시 — delta 변동의 영향"),
        LI("t = 0 매수 (Δ = 0.48) → c = 1, q_δ = 0.48", num="·"),
        LI("t = 1 매수 (Δ = 0.52) → c = 2, q_δ = 1.00", num="·"),
        LI("t = 2 매도 (Δ = 0.50) → c = 1, q_δ = 0.50", num="·"),
        G(6),
        H("Paper와의 차이"),
        P("Paper는 동일 시나리오에서 inventory = 1로 고정되어 RP 조정이 실제 delta 노출을 과소·과대 반영할 수 있는 반면, Develop은 q_delta = 0.50으로 실제 노출에 정확히 비례한 조정이 가능하다."),
    ],
)

SLIDE_4_3 = Slide(
    title="4. Methodology",
    subtitle="4.3 Develop ② 3×3 다중 호가 + 워터폴 체결 로직",
    blocks=[
        H("배경 & 구조"),
        P("A-S 원모델은 각 방향에 단일 호가만 두지만, 실제 MM은 LOB의 여러 거리에 복수 호가를 동시 제시한다. 본 프로젝트는 bid 3레벨 + ask 3레벨 = 총 6호가를 동시에 운용한다."),
        LI("bid_1·bid_2·bid_3 — δ 작음 → 큼 (가까움 → 멀음)", num="·"),
        LI("ask_1·ask_2·ask_3 — δ 작음 → 큼 (가까움 → 멀음)", num="·"),
        G(6),
        H("레벨별 독립 체결 확률"),
        P("P_i = A·exp(−k·δ_i)·dt — 거리 δ_i가 클수록 체결 확률은 낮아진다. δ_1 < δ_2 < δ_3 → P_1 > P_2 > P_3."),
        G(6),
        H("워터폴 집행 로직 — 핵심 설계"),
        P("멀리 있는 레벨이 체결되면 그보다 가까운 레벨은 이미 체결된 것으로 간주한다. 시장 참여자가 bid_3 가격을 수용했다면 bid_1·bid_2도 이미 치고 지나간 것이기 때문이다."),
        LI("P_3 체결 → bid_1·bid_2·bid_3 모두 체결", num="·"),
        LI("P_3 불발·P_2 체결 → bid_1·bid_2 체결", num="·"),
        LI("P_2 불발·P_1 체결 → bid_1만 체결", num="·"),
        G(4),
        H("효과"),
        P("단일 step에서 최대 3계약 체결 — Paper(step당 최대 1계약) 대비 재고 전환 속도 최대 3배 향상."),
    ],
)

SLIDE_4_4 = Slide(
    title="4. Methodology",
    subtitle="4.4 Develop ③ 즉시 체결(δ≤0) & mid price 집행",
    blocks=[
        H("발동 조건"),
        P("어느 레벨이든 δ ≤ 0(해당 호가가 mid를 역전)이면 P(fill) = 1.0으로 즉시 체결을 확정한다. (구현 완료)"),
        G(6),
        H("체결 가격"),
        P("fill_price = mid if δ ≤ 0 else quote_price. 즉, mid를 cross하는 호가는 시장가(mid)로 집행된다."),
        G(6),
        H("의미와 효과"),
        P("Net Delta 누적으로 q_delta가 커지면 RP가 mid에서 크게 벗어나 일부 레벨의 δ가 음수로 떨어질 수 있다. 이 경우 즉시 체결로 누적 재고를 강제로 해소하여 방향성 노출의 폭발을 차단한다."),
        G(6),
        H("설계 정당성"),
        P("실제 MM은 mid를 cross하는 호가를 시장가 주문에 가깝게 처리하므로 본 메커니즘은 현실의 집행 관행을 직접 반영한다."),
    ],
)

SLIDE_4_5 = Slide(
    title="4. Methodology",
    subtitle="4.5 Develop ④ 방향성 Bucket 체결 확률 모델",
    blocks=[
        H("실증 근거"),
        P("KOSPI200 OMM이 재고 충격 이후 방향성 역체결을 유도한다는 사실이 직접 관측되었다(Muravyev 2025)."),
        G(6),
        H("Bucket 구현"),
        P("모든 레벨에 동일 bucket 승수를 적용 — mu_pct = (s_next − s) / s × 100. (구현 완료)"),
        G(6),
        H("Bucket 구간 (KOSPI200 1분 변동률 분포 기반)"),
        LI("|Δ%| < 0.02% → 승수 ×1.0 (66%)", num="·"),
        LI("0.02 ~ 0.05% → 승수 ×1.5 (30%)", num="·"),
        LI("0.05 ~ 0.10% → 승수 ×2.5 (3.7%)", num="·"),
        LI(">0.10% → 승수 ×3.5 (0.1%)", num="·"),
        G(6),
        H("양방향 적용"),
        P("mu > 0이면 ask 레벨 전체에 승수를 곱하고 bid 레벨 전체를 승수로 나눈다. mu < 0이면 반대 방향. 다중 호가와 결합하면 상승장에서 ask_1·ask_2·ask_3 모두 승수가 적용되어 워터폴 체결 확률이 폭발적으로 상승한다."),
    ],
)

SLIDE_4_6 = Slide(
    title="4. Methodology",
    subtitle="4.6 시간 지평 재정의 & 1 Step Lag",
    blocks=[
        H("시간 지평"),
        P("T = 당일 장 마감, dt = 1/n_steps, T = 1 정규화. 논문 파라미터를 단위 변환 없이 재사용 가능하다(Muravyev 2025 실증으로 정당화, 구현 완료)."),
        G(6),
        H("1 Step Lag — 정보·집행 분리"),
        P("t − 1 정보만으로 t 시점 호가를 결정하여 look-ahead bias를 차단한다."),
        LI("t 스냅샷 (mid·delta 등) 기록", num="①"),
        LI("t − 1 시점에 결정된 호가로 체결·집행", num="②"),
        LI("체결 결과로 contracts·net_delta 상태 업데이트", num="③"),
        LI("t 시점의 mid를 기준으로 새 호가 계산 — 다음 step에서 사용", num="④"),
        G(6),
        H("의미"),
        P("실제 MM 시스템의 정보·집행 비동기성을 직접 반영하여, 시뮬레이션의 P&L이 비현실적으로 부풀려지는 것을 방지한다."),
    ],
)

SLIDE_4_7 = Slide(
    title="4. Methodology",
    subtitle="4.7 동적 σ — 장 막판 조정력 소멸 문제 (논의 중)",
    blocks=[
        H("문제 정의"),
        P("σ = 2.0 고정 시 (T−t) → 0이 될수록 RP 조정량 q_delta·γ·σ²·(T−t) → 0, Spread = γσ²(T−t) + 상수항도 상수항만 남아 좁아진다. 장 막판 재고가 많이 쌓여 있어도 호가 비대칭이 사라져 재고 해소가 불가능하다."),
        G(6),
        H("해결 아이디어"),
        LI("σ_eff(t) = σ_base / √(T−t) → γ·σ_eff²·(T−t) = γ·σ_base² 상수 유지", num="A.", label="방안"),
        LI("τ_eff = max(τ, 1/6) — 장 막판에만 임계값 발동(Indicator), 구현 단순", num="B.", label="방안"),
        LI("장 막판 전용 별도 파라미터 구간을 따로 설정", num="C.", label="방안"),
        G(6),
        H("이론적 배경"),
        P("S&S(2009) Figure 1·2에서 장 초반 호가 민감도는 거의 0, 장 막판에서는 민감도가 폭발적으로 증가하는 패턴이 제시되어 있다. 모델은 이 패턴을 반영해야 한다."),
        G(6),
        H("논의 사항"),
        P("어떤 방안을 선택할 것인가, 구현 가능한 시간적 여유가 있는가, 발표에서 어떻게 표현할 것인가가 미정 상태이다."),
    ],
)

SLIDE_4_8 = Slide(
    title="4. Methodology",
    subtitle="4.8 Paper vs Develop 설계 비교 & Monte Carlo 설정",
    blocks=[
        H("설계 비교"),
        LI("재고 — Paper: 계약 수 q / Develop: Net Delta q_delta", num="·"),
        LI("RP — Paper: r = s − qγσ²τ / Develop: r = s − q_delta·γσ²τ", num="·"),
        LI("호가 — Paper: 단일 bid·ask / Develop: 3레벨 bid·ask + 워터폴", num="·"),
        LI("체결 — Paper: 기본 포아송 / Develop: δ≤0 즉시 체결 + bucket 승수", num="·"),
        G(8),
        H("Monte Carlo 설계"),
        P("두 모드를 동일 drift 조건과 동일 seed로 실행하여 공정한 비교를 보장한다."),
        LI("drift = 0 — 베이스라인 시나리오", num="·"),
        LI("drift = 15 — 추세 시장 시나리오 (방향성 효과 극대화)", num="·"),
        LI("1,000회 Monte Carlo, 동일 seed로 stochastic noise를 제거하여 모형 효과만을 분리", num="·"),
    ],
)

# ============================================================
# 5. Result — 4 slides
# ============================================================
SLIDE_5_1 = Slide(
    title="5. Result",
    subtitle="5.1 단일 시뮬레이션 — 전략 작동 메커니즘 시각화",
    blocks=[
        H("Mid Price + 3×3 호가 레벨 밴드"),
        P("Paper(단일 bid·ask) vs Develop(3레벨 bid·ask) 비교 시각화. 재고 누적 구간에서 Net Delta 기반 RP가 이동하면서 bid_1~3·ask_1~3가 비대칭으로 배치되는 구간을 강조 표시한다."),
        C("Figure placeholder — Paper vs Develop 호가 밴드 overlay"),
        G(6),
        H("Net Delta vs Contracts 경로 비교"),
        P("두 상태를 병렬로 시각화 — delta가 변동하는 구간(특히 가격 변동이 큰 구간)에서 두 값이 의미 있게 달라지는 순간을 강조한다."),
        C("Figure placeholder — net_delta(실선) vs contracts(점선) 시계열"),
        G(6),
        H("P&L 누적 경로"),
        P("Realized / Mark-to-Market / Total P&L을 분리하여 Paper와 Develop을 overlay 비교. 재고 해소 속도 차이가 누적 P&L에 어떻게 반영되는지를 정성적으로 확인한다."),
        C("Figure placeholder — P&L 분해 시계열, Paper vs Develop"),
    ],
)

SLIDE_5_2 = Slide(
    title="5. Result",
    subtitle="5.2 다중 호가 효과 — 체결 통계",
    blocks=[
        H("레벨별 체결 빈도"),
        P("level_1 / level_2 / level_3 각각의 단독 체결 빈도와 워터폴(다중 레벨 동시) 체결 비율을 막대 그래프로 비교한다. 워터폴 체결이 전체 체결의 어느 비중을 차지하는지를 정량 확인한다."),
        C("Figure placeholder — 레벨별 체결 빈도 bar chart"),
        G(6),
        H("Step당 평균 체결 계약 수"),
        P("Paper(≤1계약) vs Develop(≤3계약)의 step당 체결량 분포를 히스토그램으로 비교한다. Develop의 분포가 우측으로 이동(높은 체결량 비중 증가)하는 정도를 측정한다."),
        C("Figure placeholder — step당 체결량 히스토그램"),
        G(6),
        H("해석"),
        P("워터폴 체결이 실제로 재고 해소 속도를 몇 배 높이는지를 정량적으로 확인하여 다중 호가 설계의 효과를 입증한다."),
    ],
)

SLIDE_5_3 = Slide(
    title="5. Result",
    subtitle="5.3 체결 모델 검증 — Bucket·즉시체결 통계",
    blocks=[
        H("즉시 체결(δ ≤ 0) 발생 통계"),
        P("전체 체결 중 즉시 체결(crossing quote) 비율과 발생 빈도를 측정한다. 어떤 시장 상황(드리프트, 재고 누적 수준)에서 즉시 체결이 주로 발생하는지 분석한다."),
        C("Figure placeholder — 즉시체결 비율 bar"),
        G(6),
        H("Bucket 승수 적용 분포"),
        P("×1.0 / ×1.5 / ×2.5 / ×3.5 각 구간의 적용 빈도를 시뮬레이션 데이터로 검증한다. 설계 기준(KOSPI200 1분 변동률 66/30/3.7/0.1%)과 시뮬레이션 결과 분포를 비교한다."),
        C("Figure placeholder — bucket 적용 분포 bar chart"),
        G(6),
        H("방향성 비대칭 검증"),
        P("실제 ask:bid 체결 비율을 측정하여 기본 포아송 예상치(1:1)와 비교한다. 추세 시장에서 방향성 비대칭이 정량적으로 얼마나 발생하는지를 확인한다."),
    ],
)

SLIDE_5_4 = Slide(
    title="5. Result",
    subtitle="5.4 1000회 Monte Carlo & 우리의 기여",
    blocks=[
        H("정량 비교"),
        LI("P&L 분포 (drift = 0) — mean·std 비교", num="·"),
        LI("P&L 분포 (drift = 15) — 추세 시장 차이 극대화", num="·"),
        LI("최종 net_delta 분포 — Develop이 더 좁은 분포를 갖는지 검증", num="·"),
        LI("종합 지표 테이블 — P&L mean·std / net_delta mean·std / 즉시체결 건수 / 워터폴 비율 / bucket 적용 비율", num="·"),
        G(8),
        H("기여 정리"),
        LI("Net Delta RP 조정의 정밀화 — 같은 계약 수라도 delta 차이를 반영하여 실제 노출에 정확히 비례한 RP 조정 실현", num="①", label="기여"),
        LI("다중 호가로 재고 해소 속도 향상 — 워터폴 체결로 step당 최대 3계약 → 재고 해소 최대 3배, 특히 trending market에서 효과 극대화", num="②", label="기여"),
        LI("체결 모델의 현실화 — bucket 승수로 방향성 비대칭화 → 추세 방향 체결이 더 자주 발생 → 재고가 자연스럽게 해소", num="③", label="기여"),
        G(4),
        P("세 논문(A-S 2008 + S&S 2009 + Muravyev 2025)을 단일 시뮬레이터에 통합하여 이론·실증 양면을 모두 갖춘 구현을 완성하였다."),
    ],
)

# ============================================================
# 6. Conclusion — 2 slides
# ============================================================
SLIDE_6_1 = Slide(
    title="6. Conclusion",
    subtitle="6.1 핵심 기여 정리",
    blocks=[
        H("A-S 원모델 대비 4가지 동시 확장"),
        LI("Net Delta 재고 — S&S Theorem 2 직접 구현", num="·"),
        LI("3×3 다중 호가 + 워터폴 체결 — A-S 한계 ②·③ 동시 해결", num="·"),
        LI("방향성 Bucket 승수 — Muravyev 실증 직접 반영", num="·"),
        LI("즉시 체결(δ≤0) + mid price — 누적 재고의 강제 해소 메커니즘", num="·"),
        G(8),
        H("이론·실증 완비 구조"),
        P("S&S Thm.2 (Net Delta), Muravyev (비헷징·방향성·당일 T) — 모든 설계 결정에 이론적 또는 실증적 근거를 명시적으로 부여한다."),
        G(8),
        H("실증적 성과"),
        P("Monte Carlo 결과에서 Develop이 Paper 대비 재고 분산 X% 감소, P&L XX% 향상 — 수치는 시뮬레이션 완료 후 채워 어필. 특히 추세 시장(drift=15) 조건에서 차이가 극대화된다."),
    ],
)

SLIDE_6_2 = Slide(
    title="6. Conclusion",
    subtitle="6.2 한계 & 향후 방향",
    blocks=[
        H("장 막판 조정력 소멸"),
        P("(T−t) → 0 시 RP·Spread 모두 약화되어 재고 해소력이 사라진다. 동적 σ 논의의 결과(방안 A·B·C 중 선택)에 따라 해결 예정."),
        G(6),
        H("GBM 가정의 한계"),
        P("실제 KOSPI200 5일분 ATM 데이터를 적용할 경우 점프와 변동성 클러스터링을 반영해야 한다. GBM 가정은 일중 변동성을 단순화한 근사이다."),
        G(6),
        H("ATM 가정의 한계"),
        P("만기에 접근할수록 Charm effect로 delta가 급변한다. 실제 운용에서는 만기 가까운 옵션의 roll 전략이 별도로 필요하다."),
        G(6),
        H("향후 방향"),
        LI("단기 — 동적 σ 도입, 실제 KOSPI200 데이터 적용", num="·"),
        LI("장기 — 강화학습(RL) 기반 동적 γ 조정 메커니즘 도입", num="·"),
    ],
)

# ============================================================
# 7. Appendix — 4 slides
# ============================================================
SLIDE_A_1 = Slide(
    title="7. Appendix",
    subtitle="A.1 다중 호가 워터폴 로직 수식화",
    blocks=[
        H("레벨별 체결 확률"),
        P("P_i = A·exp(−k·δ_i) · dt · bucket_multiplier  (i = 1, 2, 3)"),
        G(8),
        H("워터폴 체결 판정 — bid 방향 의사코드"),
        LI("fills = []", num="·"),
        LI("if rand() < P_3:  fills = [1, 2, 3]   # 3레벨 체결 시 1·2도 자동 체결", num="·"),
        LI("elif rand() < P_2:  fills = [1, 2]", num="·"),
        LI("elif rand() < P_1:  fills = [1]", num="·"),
        G(8),
        H("체결 시 net_delta 업데이트"),
        P("for i in fills:  net_delta += delta_i"),
        G(8),
        H("ask 방향"),
        P("부호만 반대로 동일한 절차를 적용한다 — fills 목록에 대해 net_delta -= delta_i."),
    ],
)

SLIDE_A_2 = Slide(
    title="7. Appendix",
    subtitle="A.2 동적 σ 방안 상세 (논의용)",
    blocks=[
        H("방안 A — 시간 의존 σ"),
        P("σ_eff(t) = σ_base / √(T − t) → γ·σ_eff²·(T − t) = γ·σ_base² 상수 유지. 장 막판에도 RP 조정력이 보존된다."),
        LI("σ → ∞로 발산 가능 → 상한 clip 필요", label="주의"),
        G(6),
        H("방안 B — Indicator Function"),
        P("τ_eff = max(τ, 1/6) — 장 초반·중반에 τ > 1/6이면 그대로 사용, 막판에만 1/6으로 고정. 구현이 단순하고 부작용이 적다."),
        LI("임계값 1/6의 선택 근거 필요 (장 운영시간 6.5h 기준 약 1시간)", label="주의"),
        G(6),
        H("방안 C — 별도 파라미터 구간"),
        P("장 막판(예: 마감 30분 전)에 별도 σ·γ·k 파라미터를 적용. 단순하지만 파라미터 수가 늘어나 일관성 검증이 필요하다."),
    ],
)

SLIDE_A_3 = Slide(
    title="7. Appendix",
    subtitle="A.3 파라미터 설계 근거 & ATM 수식",
    blocks=[
        H("σ = 2.0 채택 근거"),
        P("KOSPI200 IV ≈ 20% → IV 기반 시 γσ² ≈ 0.006 vs 고정 σ = 2.0 일 때 γσ² = 0.4 → 64배 차이. IV 기반은 RP 조정량이 tick size 이하로 수렴하여 호가 비대칭을 만들 수 없다."),
        G(6),
        H("ATM Delta 정의"),
        P("Δ = N(d₁), d₁ ≈ 0 at ATM → N(0) = 0.5. 일중 변동 범위는 약 0.45 ~ 0.55 수준이다."),
        G(6),
        H("Bucket 경계 근거"),
        P("KOSPI200 1분 변동률 분포의 실증 관측 결과(66 / 30 / 3.7 / 0.1%) 구간을 그대로 채택하여 시뮬레이션의 현실 정합성을 확보한다."),
    ],
)

SLIDE_A_4 = Slide(
    title="7. Appendix",
    subtitle="A.4 참고문헌",
    blocks=[
        LI("Avellaneda, M. & Stoikov, S. (2008). High-frequency trading in a limit order book. Quantitative Finance, 8(3), 217–224.", num="·"),
        LI("Stoikov, S. & Saglam, M. (2009). Option market making under inventory risk. Review of Derivatives Research, 12(1), 55–79.", num="·"),
        LI("Muravyev, D. et al. (2025). How do options market makers manage inventory? Working Paper.", num="·"),
        LI("KRX. 주가지수옵션 상품명세 / 시장조성자 법적 의무. https://rule.krx.co.kr", num="·"),
    ],
)

ALL_SLIDES: list[Slide] = [
    SLIDE_1_OVERVIEW,
    SLIDE_2_1, SLIDE_2_2, SLIDE_2_3, SLIDE_2_4,
    SLIDE_3_1, SLIDE_3_2, SLIDE_3_3, SLIDE_3_4, SLIDE_3_5,
    SLIDE_4_1, SLIDE_4_2, SLIDE_4_3, SLIDE_4_4, SLIDE_4_5, SLIDE_4_6, SLIDE_4_7, SLIDE_4_8,
    SLIDE_5_1, SLIDE_5_2, SLIDE_5_3, SLIDE_5_4,
    SLIDE_6_1, SLIDE_6_2,
    SLIDE_A_1, SLIDE_A_2, SLIDE_A_3, SLIDE_A_4,
]

OUT = ROOT / "reference" / "past_outputs" / "Y-PJ-FoRM_KOSPI200_MarketMaking.pptx"


def main():
    deck = DeckContent(cover=COVER, toc=TOC, slides=ALL_SLIDES)
    pptx_bytes = render_deck(deck)
    OUT.write_bytes(pptx_bytes)
    print(
        f"rendered {len(pptx_bytes):,} bytes -> {OUT.relative_to(ROOT)} "
        f"({len(deck.slides) + 2} slides)"
    )


if __name__ == "__main__":
    main()
