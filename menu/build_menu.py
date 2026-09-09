#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้างเมนูร้านบางเวลา ขนาด A3 (5 หน้า) เป็นไฟล์ HTML และ PDF

วิธีใช้:
    python3 build_menu.py            # สร้าง bangwela-menu.html
    python3 build_menu.py --pdf      # สร้าง HTML + PDF (ต้องมี playwright)

แก้ชื่อเมนู/ราคา ได้ที่ตัวแปร PAGES ด้านล่างนี้ แล้วรันใหม่
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# ข้อมูลเมนู  ── (ชื่ออาหาร, ราคา, หมายเหตุขนาด)
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

YUM = [
    ("ส้มตำไทย", "65"),
    ("ส้มตำปูปลาร้า", "65"),
    ("ตำข้าวโพดไข่เค็ม", "75"),
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

PAGES = [
    dict(
        title_th="ของกินเล่น &amp; ทอด",
        title_en="Snacks &amp; Fried",
        art="fried.svg",
        art_w="66%",
        cols=[
            [("ของกินเล่น", "Snacks &amp; Bites", SNACKS)],
            [("ทอด", "Deep Fried", FRIED)],
        ],
    ),
    dict(
        title_th="ส้มตำ &amp; ยำ",
        title_en="Som Tam &amp; Thai Salads",
        art="somtam.svg",
        art_w="60%",
        cols=[
            [("ส้มตำ", "Som Tam", YUM[:3]), ("ยำ", "Thai Salads", YUM[3:10])],
            [("ยำ <em>(ต่อ)</em>", "Thai Salads · continued", YUM[10:])],
        ],
    ),
    dict(
        title_th="ต้ม &amp; แกง",
        title_en="Soups &amp; Curries",
        art="tomyum.svg",
        art_w="64%",
        cols=[
            [("ต้ม", "Soups", SOUP)],
            [("แกง", "Curries", CURRY)],
        ],
    ),
    dict(
        title_th="นึ่ง · ผัด · จานข้าว",
        title_en="Steamed · Stir-fried · Rice",
        art="fish.svg",
        art_w="78%",
        dense=True,
        cols=[
            [("นึ่ง", "Steamed", STEAMED), ("ผัด", "Stir-fried", STIRFRY)],
            [("เมนูจานข้าว", "Rice Dishes", RICE)],
        ],
    ),
    dict(
        title_th="ย่าง · สลัด · สเต็ก",
        title_en="Grilled · Salad · Steak",
        art="grill.svg",
        art_w="88%",
        cols=[
            [("ย่าง", "From the Grill", GRILLED)],
            [("สลัด / สเต็ก", "Salad &amp; Steak", STEAK)],
        ],
    ),
]

# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------

CSS = """
@font-face{font-family:Kanit;src:url(fonts/Kanit-200.ttf) format("truetype");font-weight:200;font-style:normal}
@font-face{font-family:Kanit;src:url(fonts/Kanit-300.ttf) format("truetype");font-weight:300;font-style:normal}
@font-face{font-family:Kanit;src:url(fonts/Kanit-400.ttf) format("truetype");font-weight:400;font-style:normal}
@font-face{font-family:Kanit;src:url(fonts/Kanit-500.ttf) format("truetype");font-weight:500;font-style:normal}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-300.ttf) format("truetype");font-weight:300;font-style:normal}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-400.ttf) format("truetype");font-weight:400;font-style:normal}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-400i.ttf) format("truetype");font-weight:400;font-style:italic}

:root{
  --bg:#0a0a0b;
  --ink:#ffffff;
  --dim:rgba(255,255,255,.52);
  --faint:rgba(255,255,255,.20);
  --gold:#c9a24d;
}

@page{ size:297mm 420mm; margin:0 }

*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#2a2a2c}
body{ font-family:Kanit,"Noto Sans Thai",sans-serif; -webkit-font-smoothing:antialiased }

.page{
  position:relative;
  width:297mm; height:420mm;
  margin:0 auto;
  padding:19mm 22mm 14mm;
  background:
    radial-gradient(115% 78% at 50% 16%, #191a1d 0%, #0e0e10 46%, var(--bg) 78%);
  color:var(--ink);
  display:flex; flex-direction:column;
  overflow:hidden;
  break-after:page; page-break-after:always;
}
.page:last-child{break-after:auto;page-break-after:auto}

/* กรอบเส้นบาง + มุมทอง */
.frame{position:absolute;inset:11mm;border:.35mm solid rgba(201,162,77,.28);pointer-events:none}
.frame span{position:absolute;width:9mm;height:9mm;border:.8mm solid var(--gold);opacity:.8}
.frame span:nth-child(1){top:-1.1mm;left:-1.1mm;border-right:0;border-bottom:0}
.frame span:nth-child(2){top:-1.1mm;right:-1.1mm;border-left:0;border-bottom:0}
.frame span:nth-child(3){bottom:-1.1mm;left:-1.1mm;border-right:0;border-top:0}
.frame span:nth-child(4){bottom:-1.1mm;right:-1.1mm;border-left:0;border-top:0}

/* ---------- หัวกระดาษ ---------- */
.head{text-align:center;flex:none}
.head .th{font-weight:200;font-size:12.5mm;line-height:1.05;letter-spacing:.14em;text-indent:.14em}
.head .en{margin-top:2.6mm;font-family:Cormorant,serif;font-weight:400;font-size:3.3mm;
  letter-spacing:.72em;text-indent:.72em;text-transform:uppercase;color:var(--gold)}
.head .est{margin-top:2.2mm;font-weight:200;font-size:3.5mm;
  letter-spacing:.30em;text-indent:.30em;color:var(--dim)}

.rule{display:flex;align-items:center;justify-content:center;gap:3mm;margin:6mm 0 0;flex:none}
.rule i{display:block;height:.3mm;width:26mm;background:linear-gradient(90deg,transparent,rgba(201,162,77,.75))}
.rule i+i{background:linear-gradient(90deg,rgba(201,162,77,.75),transparent)}
.rule b{width:2.2mm;height:2.2mm;background:var(--gold);transform:rotate(45deg)}

/* ---------- ชื่อหน้า ---------- */
.ptitle{text-align:center;flex:none;margin-top:8mm}
.ptitle .th{font-weight:300;font-size:11.5mm;line-height:1.2;letter-spacing:.05em}
.ptitle .en{margin-top:1mm;font-family:Cormorant,serif;font-style:italic;font-size:4.6mm;
  letter-spacing:.34em;text-indent:.34em;color:var(--gold);text-transform:uppercase}

/* ---------- เนื้อหา ---------- */
.body{flex:none;margin-top:11mm;display:grid;grid-template-columns:1fr 1fr;gap:0 14mm}
.col+.col{border-left:.3mm solid rgba(255,255,255,.13);padding-left:14mm}

.sec{margin-bottom:5mm}
.sec+.sec{margin-top:10mm}
.sec-h{margin-bottom:5.5mm}
.sec-h .th{font-weight:400;font-size:6.8mm;letter-spacing:.06em;line-height:1.3}
.sec-h .th em{font-style:normal;font-weight:300;font-size:.66em;color:var(--dim)}
.sec-h .en{margin-top:.6mm;font-family:Cormorant,serif;font-size:3.2mm;letter-spacing:.42em;
  text-transform:uppercase;color:var(--gold)}
.sec-h .bar{margin-top:2.6mm;height:.3mm;background:linear-gradient(90deg,rgba(201,162,77,.85),rgba(201,162,77,0))}

.item{display:flex;align-items:baseline;gap:2.5mm;margin:0 0 4.8mm}
.body.dense .item{margin-bottom:4.0mm}
.body.dense .sec+.sec{margin-top:8mm}
.item .n{font-weight:300;font-size:5.4mm;line-height:1.35;white-space:nowrap}
.item .n em{font-style:normal;font-size:.82em;color:var(--dim)}
.item .dots{flex:1 1 auto;height:.28mm;background:repeating-linear-gradient(90deg,var(--faint) 0 .5mm,transparent .5mm 2mm);
  transform:translateY(-1.1mm);min-width:6mm}
.item .p{font-weight:300;font-size:5.4mm;font-variant-numeric:tabular-nums;white-space:nowrap}
.item .sz{display:block;font-family:Cormorant,serif;font-style:italic;font-size:3.1mm;
  letter-spacing:.06em;color:var(--dim);margin-top:-.6mm}
.item .p .sz{text-align:right}

/* ---------- ภาพประกอบ ---------- */
.art{flex:1 1 auto;min-height:62mm;display:flex;align-items:center;justify-content:center;
  padding:10mm 0 2mm;color:var(--gold);opacity:.9}
.art svg{width:auto;height:100%;max-height:100%;object-fit:contain}

/* ---------- ท้ายกระดาษ ---------- */
.tail{flex:none;display:flex;align-items:center;justify-content:center;gap:2.6mm;margin:0 0 7mm}
.tail i{width:1.1mm;height:1.1mm;border-radius:50%;background:var(--gold);opacity:.55}
.tail b{width:1.9mm;height:1.9mm;background:var(--gold);transform:rotate(45deg);opacity:.85}
.foot{flex:none;display:flex;align-items:center;justify-content:space-between;
  border-top:.3mm solid rgba(255,255,255,.13);padding-top:4mm;
  font-family:Cormorant,serif;font-size:3.2mm;letter-spacing:.34em;
  text-transform:uppercase;color:var(--dim)}
.foot .no{color:var(--gold)}
.foot .mid{font-style:italic;letter-spacing:.12em;text-transform:none}

@media screen{
  body{padding:26px 0;display:flex;flex-direction:column;align-items:center;gap:26px}
  .page{box-shadow:0 18px 60px rgba(0,0,0,.75)}
}
"""

# --------------------------------------------------------------------------
# ประกอบ HTML
# --------------------------------------------------------------------------


def item_html(it):
    name, price = it[0], it[1]
    size = it[2] if len(it) > 2 else None
    sz_n = f'<span class="sz">{size}</span>' if size else ""
    return (
        '<div class="item">'
        f'<span class="n">{name}{sz_n}</span>'
        '<span class="dots"></span>'
        f'<span class="p">{price}</span>'
        "</div>"
    )


def section_html(sec):
    th, en, items = sec
    head = ""
    if th:
        head = (
            '<div class="sec-h">'
            f'<div class="th">{th}</div>'
            f'<div class="en">{en}</div>'
            '<div class="bar"></div>'
            "</div>"
        )
    return f'<div class="sec">{head}{"".join(item_html(i) for i in items)}</div>'


def head_html():
    return (
        '<header class="head">'
        '<div class="th">บางเวลา</div>'
        '<div class="en">Bangwela</div>'
        '<div class="est">อาหารไทย · ต้ม ยำ ทำ แกง</div>'
        "</header>"
        '<div class="rule"><i></i><b></b><i></i></div>'
    )


def page_html(idx, page, total):
    art_path = os.path.join(HERE, "art", page["art"])
    with open(art_path, encoding="utf-8") as fh:
        art = fh.read()
    art = art.replace(
        "<svg ", f'<svg preserveAspectRatio="xMidYMid meet" style="max-width:{page["art_w"]}" ', 1
    )
    dense = " dense" if page.get("dense") else ""
    cols = "".join(
        f'<div class="col">{"".join(section_html(s) for s in col)}</div>'
        for col in page["cols"]
    )
    return f"""<section class="page">
  <div class="frame"><span></span><span></span><span></span><span></span></div>
  {head_html()}
  <div class="ptitle">
    <div class="th">{page['title_th']}</div>
    <div class="en">{page['title_en']}</div>
  </div>
  <div class="body{dense}">{cols}</div>
  <div class="art">{art}</div>
  <div class="tail"><i></i><b></b><i></i></div>
  <footer class="foot">
    <span>Bangwela · บางเวลา</span>
    <span class="mid">ราคาเป็นเงินบาท</span>
    <span class="no">{idx:02d} / {total:02d}</span>
  </footer>
</section>"""


def build_html():
    pages = "\n".join(page_html(i + 1, p, len(PAGES)) for i, p in enumerate(PAGES))
    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>เมนู · ร้านบางเวลา</title>
<style>{CSS}</style>
</head>
<body>
{pages}
</body>
</html>
"""


def build_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright

    exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=exe if os.path.exists(exe) else None, args=["--no-sandbox"]
        )
        page = browser.new_page()
        page.goto("file://" + html_path)
        page.wait_for_timeout(1200)
        page.pdf(
            path=pdf_path,
            width="297mm",
            height="420mm",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


if __name__ == "__main__":
    html_path = os.path.join(HERE, "bangwela-menu.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(build_html())
    print("wrote", html_path)
    if "--pdf" in sys.argv:
        pdf_path = os.path.join(HERE, "bangwela-menu.pdf")
        build_pdf(html_path, pdf_path)
        print("wrote", pdf_path)
