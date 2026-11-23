#!/usr/bin/env python3
"""2026 지원금·근로장려금·실업급여·중위소득·육아수당 계산기 (0520goeus/benefit-calc-kr) — 32개 초대형 검색량 한국 복지·수당 SEO 페이지."""
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)

SITE_NAME = "2026 지원금·수당 계산기"
SITE_URL = "https://0520goeus.github.io/benefit-calc-kr"
INDEXNOW_KEY = "e8a214c9f70341b69d05c2e8a71b9403"
GOOGLE_FILE = "google873809343766a3b6.html"
ADSENSE_CLIENT = "ca-pub-8749404731911210"
COUPANG_TRACKING = "AF9170267"
COUPANG_WIDGET_ID = 1049499

DISCLOSURE = "이 페이지는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
COUPANG_BOX = (
    '<section class="card shop">'
    f'<p class="disc">{DISCLOSURE}</p>'
    '<h3>💡 생활비 아끼는 인기 생필품·자취 필수템 특가</h3>'
    '<script src="https://ads-partners.coupang.com/g.js"></script>'
    f'<script>new PartnersCoupang.G({{"id":{COUPANG_WIDGET_ID},"template":"carousel",'
    f'"trackingCode":"{COUPANG_TRACKING}","width":"100%","height":"140","tsource":""}});</script>'
    "</section>"
)


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def won(n) -> str:
    return f"{int(round(n)):,}원"


CSS = """
:root{--bg:#f8fafc;--card:#ffffff;--ink:#0f172a;--sub:#475569;--line:#e2e8f0;--accent:#2563eb;--green:#059669;--amber:#d97706}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 -apple-system,"Apple SD Gothic Neo",sans-serif}
header{background:#0f172a;color:#fff;padding:16px 20px}
.wrap{max-width:940px;margin:0 auto;padding:0 18px}
header .wrap{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
header a{color:#cbd5e1;text-decoration:none;font-size:14px;font-weight:600}
header .brand{color:#fff;font-size:19px;font-weight:800}
nav{display:flex;gap:14px;flex-wrap:wrap}
main{padding:28px 0 60px;display:grid;gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}
h1{font-size:27px;line-height:1.35;margin:0 0 10px}h2{font-size:20px;margin:0 0 12px}h3{font-size:17px;margin:0 0 8px}
.sub{color:var(--sub);margin:0 0 14px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:11px}
.tile{display:grid;gap:4px;padding:14px 15px;border:1px solid var(--line);border-radius:12px;background:#fff;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:var(--accent)}
.tile b{font-size:15px}.tile small{color:var(--sub)}.tile span{color:var(--green);font-weight:800;font-size:14.5px}
.big-box{background:#0f172a;color:#fff;border-radius:14px;padding:22px;display:grid;gap:8px}
.big-num{font-size:34px;font-weight:800;color:#38d9a9}
input,select{width:100%;padding:11px 13px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:15px}
label{display:grid;gap:5px;font-size:13.5px;color:var(--sub);margin-bottom:10px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child{text-align:left}
thead th{background:#f1f5f9;font-size:13px;color:var(--sub)}
.faq{background:#f8fafc;padding:14px 16px;border-left:4px solid var(--accent);border-radius:8px;margin:10px 0}
.shop .disc{font-size:12.5px;color:var(--sub);margin:0 0 8px}
footer{border-top:1px solid var(--line);padding:24px 0 44px;color:var(--sub);font-size:13.5px}
footer a{color:var(--accent);text-decoration:none}
"""


def write_page(rel: str, title: str, desc: str, body: str, faqs: list[tuple[str, str]] | None = None) -> str:
    canon = f"{SITE_URL}/" if rel == "index.html" else f"{SITE_URL}/{rel}"
    ld = ""
    if faqs:
        obj = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        }
        ld = f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">
<link rel="stylesheet" href="{SITE_URL}/style.css">{ld}</head>
<body>
<header><div class="wrap">
  <a class="brand" href="{SITE_URL}/">🏛️ {SITE_NAME}</a>
  <nav>
    <a href="{SITE_URL}/#eitc">근로장려금</a>
    <a href="{SITE_URL}/#unemployment">실업급여</a>
    <a href="{SITE_URL}/#median">기준 중위소득</a>
    <a href="{SITE_URL}/parental-benefit.html">부모급여·육아수당</a>
    <a href="https://0520goeus.github.io/money-calc-kr/">연봉 실수령액</a>
  </nav>
</div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap">
  <p>안내: 2026년 대한민국 공개 법령·고시 기준 모의계산기이며, 실제 수급 자격 및 최종 지급액은 국세청 홈택스·고용24·복지로 심사 결과에 따릅니다.</p>
  <p>패밀리 사이트: <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트</a> · <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마</a> · <a href="https://0520goeus.github.io/life-money-lab/">생활비 물가 연구소</a> · <a href="https://0520goeus.github.io/vs-pick/">가성비 VS 사전</a> · <a href="https://0520goeus.github.io/life-fee-calc/">가전용량·직구관세</a> · <a href="https://0520goeus.github.io/money-calc-kr/">실수령액 계산기</a> · <a href="https://0520goeus.github.io/seller-margin-calc/">셀러 마진 계산기</a> · <a href="https://lifefixnote-kr.blogspot.com/">생활해결 노트</a></p>
</div></footer></body></html>"""
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return canon


def calc_eitc(kind: str, income_man: int) -> int:
    """2026 근로장려금 산정 공식 (단독 2200만/최대165만, 홑벌이 3200만/최대285만, 맞벌이 4400만/최대330만)."""
    cfg = {
        "single": (400, 900, 2200, 1650000),
        "single_earner": (700, 1400, 3200, 2850000),
        "dual": (800, 1700, 4400, 3300000),
    }[kind]
    lo, mid, hi, mx = cfg
    if income_man <= 0 or income_man >= hi:
        return 0
    if income_man < lo:
        return int(round(mx * (income_man / lo) / 10000) * 10000)
    if income_man <= mid:
        return mx
    return max(0, int(round(mx * ((hi - income_man) / (hi - mid)) / 10000) * 10000))


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "style.css").write_text(CSS, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / GOOGLE_FILE).write_text(f"google-site-verification: {GOOGLE_FILE}", encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")

    urls: list[str] = []
    eitc_tiles: list[str] = []
    unemp_tiles: list[str] = []
    med_tiles: list[str] = []

    # 1. 근로장려금 12개 소득구간·가구유형별 SEO 페이지
    eitc_cases = [
        ("single", "단독가구", [600, 1000, 1500, 2000]),
        ("single_earner", "홑벌이가구", [1000, 1600, 2200, 2800]),
        ("dual", "맞벌이가구", [1200, 2000, 3000, 3800]),
    ]
    for kind, k_label, inc_list in eitc_cases:
        for inc in inc_list:
            amt = calc_eitc(kind, inc)
            rel = f"eitc/{kind}-{inc}.html"
            title = f"2026 근로장려금 {k_label} 연소득 {inc:,}만원 예상 지급액 ({won(amt)})"
            desc = f"2026년 기준 {k_label} 총소득 {inc:,}만 원일 때 국세청 근로장려금 예상 수령액({won(amt)})과 재산 요건(2.4억 미만)을 확인하세요."
            faqs = [
                (f"{k_label} 연소득 {inc:,}만원이면 근로장려금을 얼마나 받나요?", f"재산 합계 1.7억 원 미만 기준 예상 지급액은 약 {won(amt)}입니다. 재산이 1.7억~2.4억 원 미만이면 50% 감액({won(amt//2)})됩니다."),
                ("근로장려금 재산 요건은 얼마인가요?", "가구원 전체 재산 합계액이 2억 4천만 원 미만이어야 신청 가능하며, 부채는 차감하지 않습니다."),
            ]
            body = f"""
            <section class="card">
              <h1>2026 근로장려금 {esc(k_label)} 연소득 {inc:,}만 원 예상 지급액</h1>
              <p class="sub">국세청 근로장려금 산정표({esc(k_label)} 기준)로 계산한 예상 수령액입니다.</p>
              <div class="big-box">
                <div>예상 근로장려금 수령액 (재산 1.7억 미만)</div>
                <div class="big-num">{won(amt)}</div>
                <div style="color:#94a3b8;font-size:14px">재산 1.7억~2.4억 미만 구간 해당 시 50% 감액: {won(amt//2)}</div>
              </div>
            </section>
            {COUPANG_BOX}
            <section class="card">
              <h2>{esc(k_label)} 소득 구간별 근로장려금 지급액 비교표</h2>
              <table><thead><tr><th>연 총소득</th><th>재산 1.7억 미만</th><th>재산 1.7억~2.4억 미만 (50%)</th></tr></thead>
              <tbody>{"".join(f"<tr><td><strong>{x:,}만 원</strong></td><td style='color:var(--green);font-weight:800'>{won(calc_eitc(kind, x))}</td><td>{won(calc_eitc(kind, x)//2)}</td></tr>" for x in range(400, 4200, 400) if calc_eitc(kind, x) > 0)}</tbody></table>
            </section>
            <section class="card"><h2>자주 묻는 질문</h2>{"".join(f'<div class="faq"><strong>Q. {esc(q)}</strong><p class="sub" style="margin:6px 0 0">A. {esc(a)}</p></div>' for q, a in faqs)}</section>
            """
            urls.append(write_page(rel, title, desc, body, faqs))
            eitc_tiles.append(f'<a class="tile" href="{SITE_URL}/{rel}"><b>{esc(k_label)} 연 {inc:,}만원</b><span>예상 {won(amt)}</span></a>')

    # 2. 실업급여(구직급여) 10개 근속연수·월급별 SEO 페이지
    # 2026 기준 일 상한액 66,000원 / 하한액 약 64,192원 (8시간 기준)
    unemp_cases = [
        (1, 30, 250, 120), (2, 30, 300, 150), (3, 35, 320, 180), (5, 35, 350, 210), (10, 45, 400, 240),
        (1, 52, 280, 150), (3, 52, 350, 210), (5, 55, 380, 240), (10, 55, 420, 270), (2, 28, 220, 150),
    ]
    for yrs, age, m_man, days in unemp_cases:
        daily = max(64192, min(66000, int(round((m_man * 10000 / 30.0) * 0.6))))
        total = daily * days
        m30 = daily * 30
        rel = f"unemployment/{yrs}yr-age{age}-{m_man}.html"
        title = f"2026 실업급여 계산 | 근속 {yrs}년·만 {age}세·월급 {m_man}만원 → 총 {won(total)} ({days}일)"
        desc = f"고용보험 가입기간 {yrs}년, 만 {age}세, 퇴직 전 월급 {m_man}만 원 기준 1일 구직급여({won(daily)}), 월 수령액({won(m30)}), 총 {days}일 수령액({won(total)}) 계산표."
        faqs = [
            (f"근속 {yrs}년 만 {age}세 실업급여는 총 며칠 동안 얼마를 받나요?", f"소정급여일수 {days}일 동안 1일 {won(daily)}씩, 총 약 {won(total)}을 수령합니다."),
            ("실업급여 수급을 위한 최소 가입기간은?", "이직일 이전 18개월간 피보험 단위기간이 통산 180일 이상이며 비자발적 퇴사 사유에 해당해야 합니다."),
        ]
        body = f"""
        <section class="card">
          <h1>2026 실업급여 계산 (근속 {yrs}년 · 만 {age}세 · 월 {m_man}만 원)</h1>
          <p class="sub">고용보험 구직급여 상·하한액 기준(1일 상한 66,000원, 하한 64,192원)을 반영한 예상 수령액입니다.</p>
          <div class="big-box">
            <div>예상 총 실업급여 수령액 ({days}일 기준)</div>
            <div class="big-num">{won(total)}</div>
            <div style="color:#94a3b8;font-size:14px">1일 지급액 {won(daily)} · 30일 환산 월 약 {won(m30)}</div>
          </div>
        </section>
        {COUPANG_BOX}
        <section class="card">
          <h2>연령·가입기간별 소정급여일수 기준표</h2>
          <table><thead><tr><th>가입기간</th><th>만 50세 미만</th><th>만 50세 이상 / 장애인</th></tr></thead>
          <tbody>
            <tr><td>1년 미만</td><td>120일</td><td>120일</td></tr>
            <tr><td>1년 이상 ~ 3년 미만</td><td>150일</td><td>180일</td></tr>
            <tr><td>3년 이상 ~ 5년 미만</td><td>180일</td><td>210일</td></tr>
            <tr><td>5년 이상 ~ 10년 미만</td><td>210일</td><td>240일</td></tr>
            <tr><td>10년 이상</td><td>240일</td><td>270일</td></tr>
          </tbody></table>
        </section>
        <section class="card"><h2>자주 묻는 질문</h2>{"".join(f'<div class="faq"><strong>Q. {esc(q)}</strong><p class="sub" style="margin:6px 0 0">A. {esc(a)}</p></div>' for q, a in faqs)}</section>
        """
        urls.append(write_page(rel, title, desc, body, faqs))
        unemp_tiles.append(f'<a class="tile" href="{SITE_URL}/{rel}"><b>근속 {yrs}년 · 만 {age}세</b><span>총 {won(total)} ({days}일)</span></a>')

    # 3. 2026 기준 중위소득 1인가구~6인가구 전용 SEO 페이지 (6개)
    median_100 = {1: 2392013, 2: 3932658, 3: 5025353, 4: 6097773, 5: 7108192, 6: 8064805}
    for n_fam, m100 in median_100.items():
        rel = f"median/{n_fam}person.html"
        title = f"2026 {n_fam}인가구 기준 중위소득 표 (50%·60%·100%·150%·200% 지원금 자격)"
        desc = f"2026년 {n_fam}인가구 기준 중위소득 100%({won(m100)})를 기준으로 생계·의료·주거·청년월세·청년도약계좌 자격 구간표를 정리했습니다."
        pcts = [32, 40, 48, 50, 60, 100, 120, 150, 180, 200]
        rows = "".join(f"<tr><td><strong>중위소득 {p}%</strong></td><td style='color:var(--green);font-weight:800'>{won(m100 * p / 100)}</td><td>{won(m100 * p / 100 * 12)}</td></tr>" for p in pcts)
        body = f"""
        <section class="card">
          <h1>2026 {n_fam}인가구 기준 중위소득 구간표</h1>
          <p class="sub">정부 복지·청년·주거·장학금 지원사업의 핵심 심사 기준인 {n_fam}인가구 중위소득 구간별 월 소득 인정액입니다.</p>
          <div class="big-box">
            <div>{n_fam}인가구 기준 중위소득 100% (월)</div>
            <div class="big-num">{won(m100)}</div>
            <div style="color:#94a3b8;font-size:14px">중위소득 60%(청년월세 기준): {won(m100*0.6)} · 중위소득 150%: {won(m100*1.5)}</div>
          </div>
        </section>
        {COUPANG_BOX}
        <section class="card">
          <h2>{n_fam}인가구 중위소득 %별 월·연 소득 기준표</h2>
          <table><thead><tr><th>구간</th><th>월 소득인정액 기준</th><th>연 환산 기준</th></tr></thead><tbody>{rows}</tbody></table>
        </section>
        """
        urls.append(write_page(rel, title, desc, body))
        med_tiles.append(f'<a class="tile" href="{SITE_URL}/{rel}"><b>{n_fam}인가구 중위소득표</b><span>100% 월 {won(m100)}</span></a>')

    # 4. 부모급여·아동수당 + 청년도약계좌 + 건강보험료 계산기 3페이지
    urls.append(write_page(
        "parental-benefit.html",
        "2026 부모급여·아동수당·첫만남이용권 총 수령액 계산기",
        "0세(월 100만원), 1세(월 50만원) 부모급여와 만 8세 미만 아동수당(월 10만원), 첫만남이용권(200~300만원) 합산 계산기.",
        f"""<section class="card">
          <h1>2026 부모급여 · 아동수당 · 첫만남이용권 총 수령액</h1>
          <p class="sub">출생 후 24개월 동안 가정양육 기준으로 받을 수 있는 주요 국가 현금성 육아 지원금 합계입니다.</p>
          <div class="big-box">
            <div>첫째아 기준 출생~24개월 주요 지원금 합계</div>
            <div class="big-num">2,240만 원</div>
            <div style="color:#94a3b8;font-size:14px">첫만남이용권 200만 + 0세 부모급여 1,200만(월100만) + 1세 부모급여 600만(월50만) + 아동수당 240만(월10만×24개월)</div>
          </div>
        </section>{COUPANG_BOX}""",
    ))

    urls.append(write_page(
        "youth-account.html",
        "2026 청년도약계좌 만기 수령액 & 정부기여금 계산기",
        "매월 최대 70만 원 5년 납입 시 정부기여금과 비과세 이자를 합산한 청년도약계좌 예상 만기 수령액을 계산합니다.",
        f"""<section class="card">
          <h1>2026 청년도약계좌 만기 수령액 계산기 (5년 비과세)</h1>
          <p class="sub">만 19~34세 청년 대상, 매월 자유 납입 시 은행 이자(비과세) + 정부 기여금을 합산해 드립니다.</p>
          <div class="grid2">
            <div>
              <label>월 납입액 (최대 70만 원) <input id="ym" type="number" value="700000" oninput="calcY()"></label>
              <label>적용 은행 금리 (%) <input id="yr" type="number" step="0.1" value="5.5" oninput="calcY()"></label>
              <label>월 정부기여금 (소득구간별 2.1만~3.3만원) <input id="yg" type="number" value="24000" oninput="calcY()"></label>
            </div>
            <div class="big-box">
              <div>5년(60개월) 만기 예상 수령액 (비과세)</div>
              <div class="big-num" id="yOut">0원</div>
              <div id="ySub" style="color:#94a3b8;font-size:14px"></div>
            </div>
          </div>
        </section>{COUPANG_BOX}
        <script>
        function calcY(){{
          const m=Math.min(700000, parseFloat(document.getElementById('ym').value)||0);
          const r=(parseFloat(document.getElementById('yr').value)||0)/100;
          const g=parseFloat(document.getElementById('yg').value)||0;
          const prin=m*60;
          const gov=g*60;
          const interest=Math.round((m+g)*(60*61/2)*(r/12));
          document.getElementById('yOut').textContent=(prin+gov+interest).toLocaleString('ko-KR')+'원';
          document.getElementById('ySub').textContent=`본인원금 ${{prin.toLocaleString('ko-KR')}}원 + 정부기여금 ${{gov.toLocaleString('ko-KR')}}원 + 비과세이자 약 ${{interest.toLocaleString('ko-KR')}}원`;
        }}
        calcY();
        </script>""",
    ))

    urls.append(write_page(
        "health-insurance.html",
        "2026 직장가입자 건강보험료 & 장기요양보험료 실시간 계산기",
        "보수월액(월급)을 넣으면 2026년 건강보험료(3.545%)와 장기요양보험료(12.95%) 본인부담금을 즉시 계산합니다.",
        f"""<section class="card">
          <h1>2026 건강보험료 & 장기요양보험료 계산기</h1>
          <div class="grid2">
            <div><label>세전 보수월액 (비과세 제외 월급, 원) <input id="hm" type="number" value="3500000" oninput="calcH()"></label></div>
            <div class="big-box">
              <div>월 본인부담 합계 (건강+장기요양)</div>
              <div class="big-num" id="hOut">0원</div>
              <div id="hSub" style="color:#94a3b8;font-size:14px"></div>
            </div>
          </div>
        </section>{COUPANG_BOX}
        <script>
        function calcH(){{
          const m=parseFloat(document.getElementById('hm').value)||0;
          const h=Math.round(m*0.03545);
          const c=Math.round(h*0.1295);
          document.getElementById('hOut').textContent=(h+c).toLocaleString('ko-KR')+'원';
          document.getElementById('hSub').textContent=`건강보험 ${{h.toLocaleString('ko-KR')}}원 + 장기요양 ${{c.toLocaleString('ko-KR')}}원`;
        }}
        calcH();
        </script>""",
    ))

    # Homepage
    home_body = f"""
    <section class="card">
      <h1>2026 대한민국 정부지원금 · 근로장려금 · 실업급여 · 중위소득 계산기</h1>
      <p class="sub">내가 받을 수 있는 근로장려금, 실업급여, 청년도약계좌, 부모급여, 가구별 기준 중위소득 자격을 10초 만에 확인하세요.</p>
      <div class="grid">
        <a class="tile" href="{SITE_URL}/parental-benefit.html"><b>부모급여·아동수당</b><span>24개월 최대 2,240만원 →</span></a>
        <a class="tile" href="{SITE_URL}/youth-account.html"><b>청년도약계좌 계산기</b><span>5년 비과세 + 정부기여금 →</span></a>
        <a class="tile" href="{SITE_URL}/health-insurance.html"><b>건강보험료 계산기</b><span>직장가입자 3.545% →</span></a>
      </div>
    </section>
    {COUPANG_BOX}
    <section class="card" id="eitc"><h2>💰 2026 근로장려금 가구·소득별 예상 지급액 (12종)</h2><div class="grid">{"".join(eitc_tiles)}</div></section>
    <section class="card" id="unemployment"><h2>📋 2026 실업급여(구직급여) 근속·연령별 계산표 (10종)</h2><div class="grid">{"".join(unemp_tiles)}</div></section>
    <section class="card" id="median"><h2>🏠 2026 가구원수별 기준 중위소득 표 (1~6인가구)</h2><div class="grid">{"".join(med_tiles)}</div></section>
    """
    urls.insert(0, write_page(
        "index.html",
        "2026 근로장려금·실업급여·기준 중위소득·청년도약계좌·부모급여 계산기",
        "2026년 최신 기준 근로장려금 예상액, 실업급여 총수령액, 1~6인가구 기준 중위소득, 부모급여·청년도약계좌 모의계산기.",
        home_body,
    ))

    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"2026 지원금·수당 계산기 빌드 완료: 총 {len(urls)}페이지")


if __name__ == "__main__":
    main()
