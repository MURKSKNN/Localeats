#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้างเมนูร้านบางเวลา ขนาด A3 (5 หน้า) เป็นไฟล์ HTML และ PDF

วิธีใช้:
    python3 build_menu.py                        # สร้าง HTML
    python3 build_menu.py --pdf                  # + PDF ขนาด A3 พอดีขอบ
    python3 build_menu.py --pdf --bleed          # เวอร์ชันโรงพิมพ์ ตัดตก 3 มม. + เส้นตัด
    python3 build_menu.py --pdf --bleed --cmyk   # + แปลงเป็น CMYK (ต้องมี ghostscript)

แก้ชื่ออาหาร/ราคา ได้ที่ลิสต์ด้านล่าง แล้วรันใหม่
วางรูปถ่ายชื่อ p1a, p1b, p2a … p5b ไว้ใน photos/ เพื่อใช้รูปจริงแทนภาพลายเส้น
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# ข้อมูลเมนู  ── (ชื่ออาหาร, ราคา[, หมายเหตุขนาด])
# --------------------------------------------------------------------------

SNACKS = [
    ("เอ็นไก่ทอด", "115"),
    ("ลาบทอด", "135"),
    ("เฟรนช์ฟราย", "95"),
    ("เม็ดมะม่วงหิมพานต์ทอด", "125"),
    ("ยำเม็ดมะม่วงหิมพานต์", "135"),
    ("ถั่วลิสงทอด", "95"),
    ("ยำถั่วลิสง", "115"),
    ("สะเก็ดระเบิด", "125"),
    ("ไก่กรอบซอสมะนาว", "155"),
    ("กุ้งชุบแป้งทอด", "145"),
    ("แหนมซี่โครงทอด", "135"),
    ("ปากเป็ดทอด", "155"),
    ("ข้าวเกรียบทอด", "95"),
    ("ปูอัดวาซาบิ", "135"),
]

FRIED = [
    ("ปลากะพงทอดน้ำปลา", "395"),
    ("ปลาทับทิมทอดกระเทียม", "335"),
    ("หมูสามชั้นทอดน้ำปลา", "145"),
    ("ปีกไก่ทอดน้ำปลา", "135"),
    ("หมูแดดเดียว", "135"),
    ("เนื้อแดดเดียว", "175"),
    ("ลาบหมูทอด", "135"),
    ("ไข่เจียวหมูสับ", "115"),
    ("ไข่เจียวกุ้งสับ", "135"),
    ("กุ้งคั่วพริกเกลือ", "195"),
    ("สามชั้นคั่วพริกเกลือ", "165"),
    ("กระดูกอ่อนคั่วพริกเกลือ", "175"),
]

SOMTAM = [
    ("ส้มตำไทย", "65"),
    ("ส้มตำปูปลาร้า", "65"),
    ("ตำข้าวโพดไข่เค็ม", "75"),
]

YUM = [
    ("ลาบหมู", "95"),
    ("ยำคอหมูย่าง", "125"),
    ("ยำคะน้ากุ้งสด", "155"),
    ("ยำรวมมิตรทะเล", "155"),
    ("ยำวุ้นเส้นทะเล", "155"),
    ("ยำวุ้นเส้นหมูสับ", "135"),
    ("ยำหมูยอ", "135"),
    ("ยำมาม่าทะเล", "155"),
    ("ยำมาม่าหมูสับ", "135"),
    ("ยำสามกรอบ", "165"),
    ("หมูมะนาว", "135"),
    ("กุ้งแช่น้ำปลา", "155"),
    ("ยำแซลม่อนแซ่บ", "165"),
    ("ยำทูน่า", "135"),
    ("เห่าดงหมู", "135"),
]

SOUP = [
    ("ต้มแซ่บกระดูกอ่อน", "165"),
    ("ต้มยำกุ้งแม่น้ำ <em>(หม้อ)</em>", "295"),
    ("ต้มยำทะเล <em>(หม้อ)</em>", "285"),
    ("ต้มยำทะเล <em>(ถ้วย)</em>", "185"),
    ("โป๊ะแตก <em>(หม้อ)</em>", "285"),
    ("โป๊ะแตก <em>(ถ้วย)</em>", "185"),
    ("ต้มยำปลากดคัง <em>(ถ้วย)</em>", "185"),
    ("ไข่ตุ๋น", "125"),
    ("ไข่ตุ๋นทะเล", "165"),
    ("ไข่ตุ๋นกุ้ง", "165"),
    ("ต้มจืดเต้าหู้หมูสับสาหร่าย", "135"),
]

CURRY = [
    ("แกงป่าหมู", "165"),
    ("แกงป่าเนื้อ", "185"),
    ("แกงปลากดคัง", "165"),
    ("แกงส้มชะอมกุ้ง", "185"),
    ("แกงส้มผักรวมกุ้ง", "165"),
]

STEAMED = [
    ("ปลากะพงนึ่งมะนาว", "395"),
    ("ปลากะพงนึ่งบ๊วย", "395"),
    ("ปลากะพงนึ่งซีอิ๊ว", "395"),
    ("ปลาหมึกนึ่งมะนาว", "265"),
]

STIRFRY = [
    ("ผัดฉ่าปลาคัง", "185"),
    ("ผัดฉ่าทะเล", "195"),
    ("หมึกผัดผงกะหรี่", "195"),
    ("กุ้งผัดผงกะหรี่", "195"),
    ("ทะเลผัดผงกะหรี่", "195"),
    ("ไก่ผัดเม็ดมะม่วงหิมพานต์", "185"),
    ("หมึกผัดไข่เค็ม", "185"),
    ("เย็นตาโฟผัดแห้ง", "185"),
    ("ผัดขี้เมาทะเล", "195"),
    ("ผัดขี้เมาหมู", "145"),
    ("กะหล่ำปลีผัดน้ำปลา", "115"),
]

RICE = [
    ("ข้าวผัดหมู", "85 / 195", "เล็ก / ใหญ่"),
    ("ข้าวผัดกุ้ง", "105 / 255", "เล็ก / ใหญ่"),
    ("ข้าวผัดทะเล", "105 / 255", "เล็ก / ใหญ่"),
    ("ข้าวกะเพราหมู", "85"),
    ("ข้าวกะเพราไก่", "85"),
    ("ข้าวกะเพรากุ้ง", "95"),
    ("ข้าวกะเพราเนื้อ", "105"),
    ("ข้าวหมูทอดกระเทียม", "85"),
    ("มาม่าผัดขี้เมาหมู", "125"),
    ("มาม่าผัดขี้เมาทะเล", "155"),
]

GRILLED = [
    ("คอหมูย่าง", "165"),
    ("เนื้อย่าง", "245"),
    ("เนื้อพิคานย่าง", "395"),
]

STEAK = [
    ("สลัดงาคั่วบางเวลา", "125"),
    ("ซีซาร์สลัด", "145"),
    ("แซลม่อนสเต็ก", "295"),
    ("ไส้กรอกรวมย่าง BBQ", "235"),
]

# --------------------------------------------------------------------------
# โครงหน้า — บล็อกในคอลัมน์
#   ("sec",   ไอคอน, ชื่อไทย, ชื่ออังกฤษ, รายการ)
#   ("photo", ชื่อไฟล์ใน photos/, ภาพลายเส้นสำรอง)
# --------------------------------------------------------------------------

PAGES = [
    dict(
        label="ของกินเล่น · ทอด",
        cols=[
            [("sec", "blossom", "ของกินเล่น", "Snacks &amp; Bites", SNACKS),
             ("photo", "p1a", "fried.svg")],
            [("sec", "pan", "ทอด", "Deep Fried", FRIED),
             ("photo", "p1b", "fish.svg")],
        ],
    ),
    dict(
        label="ส้มตำ · ยำ",
        cols=[
            [("sec", "chilli", "ส้มตำ", "Som Tam", SOMTAM),
             ("photo", "p2a", "somtam.svg"),
             ("sec", "leaf", "ยำ", "Thai Salads", YUM[:7])],
            [("sec", "leaf", "ยำ <em>(ต่อ)</em>", "Thai Salads", YUM[7:]),
             ("photo", "p2b", "yum.svg")],
        ],
    ),
    dict(
        label="ต้ม · แกง",
        cols=[
            [("sec", "bowl", "ต้ม", "Soups", SOUP),
             ("photo", "p3a", "tomyum.svg")],
            [("sec", "pot", "แกง", "Curries", CURRY),
             ("photo", "p3b", "curry.svg")],
        ],
    ),
    dict(
        label="นึ่ง · ผัด · จานข้าว",
        dense=True,
        cols=[
            [("sec", "steamer", "นึ่ง", "Steamed", STEAMED),
             ("photo", "p4a", "fish.svg"),
             ("sec", "wok", "ผัด", "Stir-fried", STIRFRY)],
            [("sec", "rice", "เมนูจานข้าว", "Rice Dishes", RICE),
             ("photo", "p4b", "riceplate.svg")],
        ],
    ),
    dict(
        label="ย่าง · สลัด · สเต็ก",
        cols=[
            [("sec", "flame", "ย่าง", "From the Grill", GRILLED)],
            [("sec", "cutlery", "สลัด / สเต็ก", "Salad &amp; Steak", STEAK)],
        ],
        bands=[("photo", "p5a", "grill.svg"), ("photo", "p5b", "steak.svg")],
    ),
]

TAGLINE = "เมนูหลากหลาย ให้ทุกมื้อเป็นมื้อพิเศษ"
CLOSING = "ความอร่อย ที่ลงตัว…ทุกเมนู"

# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------

CSS = """
@font-face{font-family:Kanit;src:url(fonts/Kanit-200.ttf) format("truetype");font-weight:200}
@font-face{font-family:Kanit;src:url(fonts/Kanit-300.ttf) format("truetype");font-weight:300}
@font-face{font-family:Kanit;src:url(fonts/Kanit-400.ttf) format("truetype");font-weight:400}
@font-face{font-family:Kanit;src:url(fonts/Kanit-500.ttf) format("truetype");font-weight:500}
@font-face{font-family:Kanit;src:url(fonts/Kanit-600.ttf) format("truetype");font-weight:600}
@font-face{font-family:Kanit;src:url(fonts/Kanit-700.ttf) format("truetype");font-weight:700}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-300.ttf) format("truetype");font-weight:300}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-400.ttf) format("truetype");font-weight:400}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-400i.ttf) format("truetype");font-weight:400;font-style:italic}
@font-face{font-family:Charm;src:url(fonts/Charmonman-400.ttf) format("truetype");font-weight:400}
@font-face{font-family:Charm;src:url(fonts/Charmonman-700.ttf) format("truetype");font-weight:700}

:root{
  --bg:#09090a;
  --ink:#ffffff;
  --dim:rgba(255,255,255,.55);
  --hair:rgba(255,255,255,.18);
  --gold:#cfa457;
}

@page{ size:297mm 420mm; margin:0 }

*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#2a2a2c}
body{font-family:Kanit,"Noto Sans Thai",sans-serif;-webkit-font-smoothing:antialiased}

.page{
  position:relative;
  width:297mm;height:420mm;
  margin:0 auto;
  padding:17mm 20mm 12mm;
  background:
    radial-gradient(76% 40% at 20% 6%, rgba(126,90,40,.17) 0%, transparent 62%),
    radial-gradient(120% 80% at 50% 24%, #17161a 0%, #0d0d0f 44%, var(--bg) 76%);
  color:var(--ink);
  display:flex;flex-direction:column;
  overflow:hidden;
  break-after:page;page-break-after:always;
}
.page:last-child{break-after:auto;page-break-after:auto}

/* ---------- หัวกระดาษ ---------- */
.head{flex:none;display:grid;grid-template-columns:auto 1fr auto;
  align-items:start;gap:8mm;padding-bottom:6mm;border-bottom:.3mm solid var(--hair)}
.head .mark .th{font-weight:700;font-size:15.5mm;line-height:1.05;letter-spacing:.01em}
.head .mark .sub{margin-top:1.4mm;padding-left:1mm;font-weight:300;font-size:6.6mm;
  line-height:1.15;letter-spacing:.03em;color:var(--gold)}
.head .mark .tag{margin-top:2.6mm;padding-left:1.5mm;font-weight:200;font-size:3.7mm;
  letter-spacing:.14em;color:var(--dim)}
.head .script{align-self:center;justify-self:center;max-width:82mm;text-align:center;
  font-family:Charm,cursive;font-weight:400;font-size:6.2mm;line-height:1.55;
  color:var(--ink);transform:rotate(-3.2deg);opacity:.94}
.head .corner{text-align:right;font-family:Cormorant,serif;font-weight:400;
  font-size:3.7mm;line-height:1.85;letter-spacing:.42em;text-indent:.42em;
  text-transform:uppercase;color:var(--ink);padding-top:2mm}
.head .corner i{display:block;height:.3mm;width:26mm;margin:2.8mm 0 0 auto;
  background:var(--gold);opacity:.85}

/* ---------- เนื้อหา ---------- */
.body{flex:1 1 auto;min-height:0;margin-top:9mm;
  display:grid;grid-template-columns:1fr 1fr;gap:0 13mm}
.col{display:flex;flex-direction:column;min-width:0}
.col+.col{border-left:.3mm solid rgba(255,255,255,.12);padding-left:13mm}

.sec{flex:none;max-width:105mm}
.sec+.sec{margin-top:11mm}
.sec-h{display:flex;align-items:center;gap:3.4mm;margin-bottom:6mm}
.sec-h .ico{flex:none;width:8.6mm;height:8.6mm;color:var(--gold)}
.sec-h .ico svg{display:block;width:100%;height:100%}
.sec-h .th{font-weight:500;font-size:8mm;line-height:1.25;white-space:nowrap}
.sec-h .th em{font-style:normal;font-weight:300;font-size:.58em;color:var(--dim)}
.sec-h .rule{flex:1 1 auto;height:.3mm;background:var(--hair);min-width:5mm}

.item{display:flex;align-items:baseline;justify-content:space-between;
  gap:6mm;margin:0 0 4.3mm}
.item .n{font-weight:300;font-size:5.2mm;line-height:1.35}
.item .n em{font-style:normal;font-size:.82em;color:var(--dim)}
.item .p{font-weight:300;font-size:5.2mm;font-variant-numeric:tabular-nums;
  white-space:nowrap;text-align:right}
.item .sz{display:block;font-family:Cormorant,serif;font-style:italic;font-size:3.1mm;
  letter-spacing:.06em;color:var(--dim);margin-top:-.8mm}
.body.dense .item{margin-bottom:3.7mm}
.body.dense .sec+.sec{margin-top:9mm}

/* ---------- รูปอาหาร: ขอบละลายเข้าพื้นดำ ---------- */
.shot{margin:8mm 0 0;flex:1 1 auto;min-height:36mm;
  display:flex;align-items:center;justify-content:center;color:var(--gold)}
.shot img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;
  filter:saturate(.88) contrast(1.05) brightness(.97);
  -webkit-mask-image:radial-gradient(ellipse 66% 64% at 50% 50%,
    #000 46%, rgba(0,0,0,.64) 72%, rgba(0,0,0,.16) 88%, transparent 97%);
  mask-image:radial-gradient(ellipse 66% 64% at 50% 50%,
    #000 46%, rgba(0,0,0,.64) 72%, rgba(0,0,0,.16) 88%, transparent 97%)}
.shot svg{width:auto;height:100%;max-height:100%;max-width:90%;opacity:.9}

/* ---------- แบนด์ภาพเต็มความกว้าง (หน้าที่รายการน้อย) ---------- */
.body.hasbands{grid-template-rows:auto 1fr}
.bands{grid-column:1/-1;min-height:0;margin-top:11mm;
  display:flex;flex-direction:column;gap:9mm}
.band{flex:1 1 0;min-height:0;display:flex;align-items:center;justify-content:center;
  color:var(--gold);overflow:hidden}
.band img{width:100%;height:100%;object-fit:cover;
  filter:saturate(.88) contrast(1.05) brightness(.97);
  -webkit-mask-image:radial-gradient(ellipse 60% 78% at 50% 50%,
    #000 48%, rgba(0,0,0,.6) 74%, rgba(0,0,0,.14) 90%, transparent 99%);
  mask-image:radial-gradient(ellipse 60% 78% at 50% 50%,
    #000 48%, rgba(0,0,0,.6) 74%, rgba(0,0,0,.14) 90%, transparent 99%)}
.band svg{height:100%;width:auto;max-width:64%;opacity:.9}

/* ---------- ท้ายกระดาษ ---------- */
.foot{flex:none;margin-top:8mm;padding-top:4.5mm;
  border-top:.3mm solid var(--hair);
  display:flex;align-items:flex-end;justify-content:space-between;gap:10mm}
.foot .closing{font-family:Charm,cursive;font-size:5.8mm;line-height:1.4;
  color:var(--gold);transform:rotate(-2deg);transform-origin:left bottom}
.foot .meta{text-align:right;font-family:Cormorant,serif;font-size:3.2mm;
  letter-spacing:.32em;text-transform:uppercase;color:var(--dim);white-space:nowrap}
.foot .meta b{display:block;font-family:Kanit;font-weight:300;font-size:3.9mm;
  letter-spacing:.08em;text-transform:none;color:var(--ink);margin-bottom:1.4mm}
.foot .meta .no{color:var(--gold)}

/* ---------- โหมดโรงพิมพ์: ตัดตก 3 มม. + เส้นตัด ---------- */
.sheet{position:relative;width:317mm;height:440mm;background:#fff;overflow:hidden;
  display:flex;align-items:center;justify-content:center;
  break-after:page;page-break-after:always}
.sheet:last-child{break-after:auto;page-break-after:auto}
.sheet .page{width:303mm;height:426mm;padding:20mm 23mm 15mm;
  break-after:auto;page-break-after:auto;box-shadow:none}
.marks span{position:absolute;background:#000}
.marks .h{width:7mm;height:.25mm}
.marks .v{width:.25mm;height:7mm}
.marks .t{top:calc(10mm - .125mm)}
.marks .b{top:calc(430mm - .125mm)}
.marks .l{left:0}
.marks .r{left:310mm}
.marks .vl{left:calc(10mm - .125mm)}
.marks .vr{left:calc(307mm - .125mm)}
.marks .vt{top:0}
.marks .vb{top:433mm}
.slug{position:absolute;left:0;right:0;top:434.2mm;text-align:center;
  font-family:Cormorant,serif;font-size:2.4mm;letter-spacing:.28em;color:#666}

@media screen{
  body{padding:26px 0;display:flex;flex-direction:column;align-items:center;gap:26px}
  .page{box-shadow:0 18px 60px rgba(0,0,0,.75)}
}
"""

# --------------------------------------------------------------------------
# ประกอบ HTML
# --------------------------------------------------------------------------

MARKS = (
    '<div class="marks">'
    '<span class="h t l"></span><span class="h t r"></span>'
    '<span class="h b l"></span><span class="h b r"></span>'
    '<span class="v vl vt"></span><span class="v vr vt"></span>'
    '<span class="v vl vb"></span><span class="v vr vb"></span>'
    "</div>"
)


def read_svg(folder, name):
    with open(os.path.join(HERE, folder, name), encoding="utf-8") as fh:
        return fh.read()


def find_photo(stem):
    """คืน path ของรูปถ่ายใน photos/ ถ้ามี (รองรับ .jpg .jpeg .png .webp)"""
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".PNG"):
        rel = "photos/" + stem + ext
        if os.path.exists(os.path.join(HERE, rel)):
            return rel
    return None


def item_html(it):
    name, price = it[0], it[1]
    size = it[2] if len(it) > 2 else None
    sz = f'<span class="sz">{size}</span>' if size else ""
    return (
        '<div class="item">'
        f'<span class="n">{name}{sz}</span>'
        f'<span class="p">{price}.-</span>'
        "</div>"
    )


def section_html(icon, th, items):
    return (
        '<div class="sec">'
        '<div class="sec-h">'
        f'<span class="ico">{read_svg("icons", icon + ".svg")}</span>'
        f'<span class="th">{th}</span>'
        '<span class="rule"></span>'
        "</div>"
        + "".join(item_html(i) for i in items)
        + "</div>"
    )


def photo_html(stem, fallback, cls="shot"):
    shot = find_photo(stem)
    if shot:
        inner = f'<img src="{shot}" alt="">'
    else:
        inner = read_svg("art", fallback).replace(
            "<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1
        )
    return f'<figure class="{cls}">{inner}</figure>'


def block_html(block):
    if block[0] == "sec":
        return section_html(block[1], block[2], block[4])
    return photo_html(block[1], block[2])


def head_html():
    return f"""<header class="head">
    <div class="mark">
      <div class="th">เมนูอาหาร</div>
      <div class="sub">อาหารบางเวลา</div>
      <div class="tag">อร่อยได้…ในทุกช่วงเวลา</div>
    </div>
    <div class="script">{TAGLINE}</div>
    <div class="corner">Good Food<br>Good Mood<i></i></div>
  </header>"""


def page_html(idx, page, total, bleed=False):
    dense = " dense" if page.get("dense") else ""
    bands = page.get("bands") or []
    if bands:
        dense += " hasbands"
    cols = "".join(
        f'<div class="col">{"".join(block_html(b) for b in col)}</div>'
        for col in page["cols"]
    )
    if bands:
        cols += ('<div class="bands">'
                 + "".join(photo_html(b[1], b[2], "band") for b in bands)
                 + "</div>")
    sheet_open, sheet_close = "", ""
    if bleed:
        slug = (
            f'<div class="slug">BANGWELA · MENU A3 · P{idx:02d}/{total:02d} · '
            f"TRIM 297 × 420 MM · BLEED 3 MM</div>"
        )
        sheet_open = f'<div class="sheet">{MARKS}{slug}'
        sheet_close = "</div>"
    return (
        sheet_open
        + f"""<section class="page">
  {head_html()}
  <div class="body{dense}">{cols}</div>
  <footer class="foot">
    <div class="closing">{CLOSING}</div>
    <div class="meta"><b>{page['label']}</b>
      <span class="no">{idx:02d} / {total:02d}</span> · ราคาเป็นเงินบาท</div>
  </footer>
</section>"""
        + sheet_close
    )


def build_html(bleed=False):
    pages = "\n".join(page_html(i + 1, p, len(PAGES), bleed) for i, p in enumerate(PAGES))
    extra = "@page{size:317mm 440mm}\nbody{background:#fff}" if bleed else ""
    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>เมนู · ร้านบางเวลา</title>
<style>{CSS}
{extra}</style>
</head>
<body>
{pages}
</body>
</html>
"""


def build_pdf(html_path, pdf_path, size=("297mm", "420mm")):
    from playwright.sync_api import sync_playwright

    exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=exe if os.path.exists(exe) else None, args=["--no-sandbox"]
        )
        page = browser.new_page()
        page.goto("file://" + html_path)
        page.wait_for_timeout(1400)
        page.pdf(
            path=pdf_path,
            width=size[0],
            height=size[1],
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def to_cmyk(src, dst):
    """แปลงเป็น CMYK ด้วย Ghostscript (หมึกรวมสูงสุด ~295%) — ใช้เมื่อโรงพิมพ์ขอ"""
    import subprocess

    subprocess.run(
        ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
         "-dColorConversionStrategy=/CMYK", "-dProcessColorModel=/DeviceCMYK",
         "-dPDFSETTINGS=/prepress", "-sOutputFile=" + dst, src],
        check=True,
    )


def photo_slots():
    out = []
    for p in PAGES:
        for col in p["cols"]:
            out += [b[1] for b in col if b[0] == "photo"]
        out += [b[1] for b in (p.get("bands") or [])]
    return out


if __name__ == "__main__":
    bleed = "--bleed" in sys.argv
    stem = "bangwela-menu-print" if bleed else "bangwela-menu"
    html_path = os.path.join(HERE, stem + ".html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(build_html(bleed))
    print("wrote", html_path)

    slots = photo_slots()
    missing = [s for s in slots if not find_photo(s)]
    if missing:
        print(f"รูปถ่าย {len(slots) - len(missing)}/{len(slots)} ช่อง — ยังไม่มี: "
              + ", ".join(missing) + " (ใช้ภาพลายเส้นแทน)")
    else:
        print(f"ใช้รูปถ่ายจริงครบทั้ง {len(slots)} ช่อง")

    if "--pdf" in sys.argv:
        pdf_path = os.path.join(HERE, stem + ".pdf")
        size = ("317mm", "440mm") if bleed else ("297mm", "420mm")
        build_pdf(html_path, pdf_path, size)
        print("wrote", pdf_path)
        if "--cmyk" in sys.argv:
            cmyk_path = os.path.join(HERE, stem + "-cmyk.pdf")
            to_cmyk(pdf_path, cmyk_path)
            print("wrote", cmyk_path)
