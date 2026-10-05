# «Пластилиновые» иконки для роликов Ники. Использование: from clay_icons import DEFS, svg; svg("CAKE", 400) → <svg class="clay">
# DEFS (градиенты) уже вставлены в index.html внизу, повторно не нужны.
# «Пластилиновые» иконки: градиенты, блики, мягкая тень (CSS .clay), без чёрной обводки
DEFS='''<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="cPink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc2cf"/><stop offset="1" stop-color="#ef6a8a"/></linearGradient>
<linearGradient id="cCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6e2"/><stop offset="1" stop-color="#eec58c"/></linearGradient>
<linearGradient id="cRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6b7d"/><stop offset="1" stop-color="#b20a26"/></linearGradient>
<linearGradient id="cGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd98f"/><stop offset="1" stop-color="#d98f2e"/></linearGradient>
<linearGradient id="cSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8d8d99"/><stop offset="1" stop-color="#2b2b33"/></linearGradient>
<linearGradient id="cBar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f2f5"/><stop offset="1" stop-color="#9b9ba6"/></linearGradient>
<linearGradient id="cWhite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e6ded2"/></linearGradient>
<linearGradient id="cGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a6e89a"/><stop offset="1" stop-color="#2f9a52"/></linearGradient>
<linearGradient id="cOat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8e3bd"/><stop offset="1" stop-color="#d9a866"/></linearGradient>
<linearGradient id="cBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb2ff"/><stop offset="1" stop-color="#3f52c9"/></linearGradient>
<linearGradient id="cYellow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff09a"/><stop offset="1" stop-color="#f2b705"/></linearGradient>
<linearGradient id="cAqua" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9efff"/><stop offset="1" stop-color="#2f97dc"/></linearGradient>
<linearGradient id="cBread" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4c27a"/><stop offset="1" stop-color="#b8692a"/></linearGradient>
<linearGradient id="cSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2cf"/><stop offset="1" stop-color="#e6a585"/></linearGradient>
<linearGradient id="cChoc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a5f3c"/><stop offset="1" stop-color="#4a2615"/></linearGradient>
<linearGradient id="cDenim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb3e8"/><stop offset="1" stop-color="#2d5aa8"/></linearGradient>
<radialGradient id="cShade" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<filter id="hl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
</defs></svg>'''
HL=lambda cx,cy,rx,ry,o=.75,r=-20: f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" opacity="{o}" filter="url(#hl)" transform="rotate({r} {cx} {cy})"/>'
SV={
'CAKE':('0 0 320 280', '<ellipse cx="160" cy="262" rx="140" ry="14" fill="url(#cShade)"/>'
  '<path d="M28 236 Q24 132 40 124 L280 72 Q298 70 296 92 L292 200 Q290 214 276 218 L44 250 Q28 252 28 236Z" fill="url(#cCream)"/>'
  '<path d="M34 180 L290 140" stroke="#f59ab0" stroke-width="16" stroke-linecap="round"/><path d="M32 214 L290 176" stroke="#fff3df" stroke-width="10" stroke-linecap="round"/>'
  '<path d="M24 132 Q22 112 44 106 L278 56 Q300 52 302 74 L302 92 Q300 104 286 106 L46 150 Q24 154 24 132Z" fill="url(#cPink)"/>'
  '<path d="M80 142 q6 26 14 0 M170 124 q6 30 14 0 M236 112 q6 22 12 0" fill="url(#cPink)" stroke="#f07a96" stroke-width="10" stroke-linecap="round"/>'
  '<circle cx="246" cy="48" r="28" fill="url(#cRed)"/><path d="M250 22 Q262 0 284 -2" stroke="#3f8f45" stroke-width="7" fill="none" stroke-linecap="round"/>'
  +HL(236,38,9,6)+HL(110,112,60,10,.6,-12)),
'DONUT':('0 0 260 260', '<ellipse cx="130" cy="244" rx="104" ry="12" fill="url(#cShade)"/><circle cx="130" cy="124" r="108" fill="url(#cGold)"/>'
  '<path d="M38 116 Q40 40 130 28 Q220 40 222 116 Q224 150 196 158 Q172 140 150 162 Q128 144 104 164 Q84 146 62 160 Q36 152 38 116Z" fill="url(#cPink)"/>'
  '<circle cx="130" cy="120" r="32" fill="#f4f1ec"/><circle cx="130" cy="120" r="32" fill="none" stroke="#e4a54e" stroke-width="8"/>'
  '<g stroke-width="9" stroke-linecap="round"><path d="M74 86 l14 -6" stroke="#fff"/><path d="M170 66 l10 10" stroke="#ffd166"/><path d="M186 124 l14 4" stroke="#7fd6ff"/><path d="M96 56 l8 12" stroke="#7bd88f"/><path d="M138 54 l14 -2" stroke="#fff"/><path d="M70 138 l12 6" stroke="#ffd166"/></g>'
  +HL(90,56,26,10,.7,-30)),
'DUMBBELL':('0 0 380 200', '<ellipse cx="190" cy="186" rx="160" ry="12" fill="url(#cShade)"/><rect x="70" y="84" width="240" height="30" rx="15" fill="url(#cBar)"/>'
  '<rect x="34" y="28" width="62" height="146" rx="22" fill="url(#cSteel)"/><rect x="0" y="54" width="44" height="92" rx="16" fill="url(#cSteel)"/>'
  '<rect x="284" y="28" width="62" height="146" rx="22" fill="url(#cSteel)"/><rect x="336" y="54" width="44" height="92" rx="16" fill="url(#cSteel)"/>'
  +HL(56,60,10,26,.55,0)+HL(306,60,10,26,.55,0)+HL(190,92,60,4,.8,0)),
'CLOCK':('0 0 320 340', '<ellipse cx="160" cy="326" rx="120" ry="12" fill="url(#cShade)"/><circle cx="66" cy="66" r="44" fill="url(#cRed)"/><circle cx="254" cy="66" r="44" fill="url(#cRed)"/>'
  '<path d="M84 290 L60 322 M236 290 L260 322" stroke="#8a0a20" stroke-width="16" stroke-linecap="round"/>'
  '<circle cx="160" cy="186" r="140" fill="url(#cRed)"/><circle cx="160" cy="186" r="116" fill="url(#cWhite)"/>'
  '<path d="M160 186 V108 M160 186 L222 216" stroke="#2b2b33" stroke-width="15" stroke-linecap="round"/><circle cx="160" cy="186" r="14" fill="url(#cRed)"/>'
  '<g fill="#cfc4b6"><circle cx="160" cy="88" r="7"/><circle cx="160" cy="284" r="7"/><circle cx="62" cy="186" r="7"/><circle cx="258" cy="186" r="7"/></g>'
  +HL(54,52,14,8,.7)+HL(98,104,40,12,.7,-40)),
'BOWL':('0 0 380 280', '<ellipse cx="190" cy="264" rx="150" ry="14" fill="url(#cShade)"/>'
  '<path d="M20 110 H360 Q356 250 190 254 Q24 250 20 110Z" fill="url(#cWhite)"/><ellipse cx="190" cy="110" rx="170" ry="40" fill="url(#cOat)"/>'
  '<circle cx="120" cy="100" r="20" fill="url(#cBlue)"/><circle cx="150" cy="118" r="17" fill="url(#cBlue)"/><circle cx="104" cy="122" r="15" fill="url(#cBlue)"/>'
  '<circle cx="250" cy="98" r="26" fill="#fff4c8"/><circle cx="250" cy="98" r="10" fill="#f2d98a"/><circle cx="292" cy="118" r="22" fill="#fff4c8"/><circle cx="292" cy="118" r="8" fill="#f2d98a"/>'
  '<circle cx="200" cy="96" r="16" fill="url(#cRed)"/>'+HL(70,160,16,40,.75,20)+HL(116,92,6,4,.8)),
'PLATE':('0 0 400 260', '<ellipse cx="200" cy="246" rx="170" ry="12" fill="url(#cShade)"/><ellipse cx="200" cy="140" rx="190" ry="100" fill="url(#cWhite)"/><ellipse cx="200" cy="134" rx="140" ry="70" fill="#f7f2ea"/>'
  '<path d="M96 140 Q120 84 176 100 Q190 140 160 164 Q118 176 96 140Z" fill="url(#cCream)"/>'
  '<ellipse cx="250" cy="122" rx="62" ry="38" fill="url(#cGold)"/><path d="M216 112 L284 104 M222 132 L282 126" stroke="#c4782a" stroke-width="6" stroke-linecap="round" opacity=".6"/>'
  '<circle cx="190" cy="178" r="22" fill="url(#cGreen)"/><circle cx="226" cy="186" r="18" fill="url(#cGreen)"/><circle cx="160" cy="184" r="16" fill="url(#cGreen)"/>'
  +HL(250,108,24,8,.7,-8)+HL(110,80,40,10,.6,-15)),
}

SV.update({
'SALAD':('0 0 380 280', '<ellipse cx="190" cy="264" rx="150" ry="14" fill="url(#cShade)"/>'
  '<path d="M20 120 H360 Q356 250 190 254 Q24 250 20 120Z" fill="url(#cWhite)"/>'
  '<path d="M40 122 Q60 60 110 80 Q130 40 180 64 Q220 30 260 66 Q310 50 336 100 Q350 112 344 124Z" fill="url(#cGreen)"/>'
  '<circle cx="140" cy="96" r="24" fill="url(#cRed)"/><circle cx="236" cy="90" r="20" fill="url(#cRed)"/>'
  '<ellipse cx="190" cy="108" rx="30" ry="14" fill="#fff4c8"/><circle cx="290" cy="104" r="14" fill="#2b2b33"/>'
  +HL(70,160,16,40,.75,20)+HL(136,86,7,4,.8)+HL(232,82,6,4,.8)),
'PIZZA':('0 0 300 300', '<ellipse cx="150" cy="286" rx="100" ry="12" fill="url(#cShade)"/>'
  '<path d="M30 50 Q150 0 270 50 L150 280Z" fill="url(#cGold)"/><path d="M42 70 Q150 30 258 70 L150 262Z" fill="#ffd27a"/>'
  '<path d="M26 46 Q150 -6 274 46" stroke="#d98f2e" stroke-width="30" fill="none" stroke-linecap="round"/>'
  '<circle cx="110" cy="96" r="22" fill="url(#cRed)"/><circle cx="182" cy="104" r="20" fill="url(#cRed)"/><circle cx="148" cy="170" r="18" fill="url(#cRed)"/>'
  +HL(90,30,40,8,.7,-12)+HL(104,88,7,4,.8)),
'GIFT':('0 0 300 300', '<ellipse cx="150" cy="286" rx="120" ry="12" fill="url(#cShade)"/>'
  '<rect x="30" y="120" width="240" height="160" rx="22" fill="url(#cRed)"/><rect x="18" y="86" width="264" height="58" rx="18" fill="url(#cRed)"/>'
  '<rect x="132" y="86" width="36" height="194" fill="url(#cGold)"/>'
  '<path d="M150 88 Q100 20 74 52 Q60 84 150 88 Q240 84 226 52 Q200 20 150 88Z" fill="url(#cGold)"/>'
  +HL(70,104,40,8,.6,0)+HL(60,170,10,40,.5,0)),
'BALLOON':('0 0 200 340', '<path d="M100 236 Q90 280 110 300 Q130 320 100 340" stroke="#cfc4b6" stroke-width="5" fill="none"/>'
  '<ellipse cx="100" cy="116" rx="90" ry="112" fill="url(#cPink)"/><path d="M88 226 L112 226 L100 242Z" fill="#ef6a8a"/>'
  +HL(66,66,18,36,.8,-25)),
})

SV.update({
'BREAD':('0 0 380 240', '<ellipse cx="190" cy="226" rx="160" ry="12" fill="url(#cShade)"/>'
  '<path d="M30 200 Q14 90 100 60 Q190 20 280 60 Q366 90 350 200 Q350 214 334 214 H46 Q30 214 30 200Z" fill="url(#cBread)"/>'
  '<path d="M110 86 Q130 120 116 150 M180 70 Q200 110 186 146 M250 84 Q270 118 256 150" stroke="#f9dcae" stroke-width="12" fill="none" stroke-linecap="round"/>'
  +HL(120,70,60,10,.6,-12)),
'PASTA':('0 0 380 280', '<ellipse cx="190" cy="264" rx="150" ry="14" fill="url(#cShade)"/>'
  '<path d="M20 120 H360 Q356 250 190 254 Q24 250 20 120Z" fill="url(#cWhite)"/>'
  '<path d="M40 122 Q70 70 120 96 Q150 50 200 84 Q250 46 290 88 Q330 76 344 120Z" fill="#f6d06b"/>'
  '<g stroke="#e9b94a" stroke-width="7" fill="none" stroke-linecap="round"><path d="M70 112 q20 -30 40 0 t40 0"/><path d="M160 104 q20 -30 40 0 t40 0"/><path d="M230 112 q20 -26 40 0"/></g>'
  '<path d="M150 80 Q190 56 232 82 Q214 108 176 106 Q150 100 150 80Z" fill="url(#cRed)"/><path d="M196 62 q14 -22 30 -10 q-10 18 -30 10Z" fill="url(#cGreen)"/>'
  +HL(70,170,16,40,.75,20)+HL(180,72,14,5,.8)),
'BANANA':('0 0 340 260', '<ellipse cx="170" cy="246" rx="130" ry="12" fill="url(#cShade)"/>'
  '<path d="M30 70 Q60 210 190 220 Q290 224 320 150 Q300 176 200 176 Q90 170 64 60Z" fill="url(#cYellow)"/>'
  '<path d="M24 74 L38 48 L66 58 L62 76Z" fill="#8a6a2e"/><path d="M318 150 L332 140" stroke="#5a4520" stroke-width="10" stroke-linecap="round"/>'
  +HL(150,196,60,8,.7,8)),
'DROP':('0 0 240 320', '<ellipse cx="120" cy="306" rx="86" ry="12" fill="url(#cShade)"/>'
  '<path d="M120 10 Q210 140 214 196 Q218 290 120 292 Q22 290 26 196 Q30 140 120 10Z" fill="url(#cAqua)"/>'
  +HL(78,190,18,46,.8,15)+HL(94,110,8,16,.7,25)),
})

SV.update({
'BUCKWHEAT':('0 0 380 280', '<ellipse cx="190" cy="264" rx="150" ry="14" fill="url(#cShade)"/>'
  '<path d="M20 120 H360 Q356 250 190 254 Q24 250 20 120Z" fill="url(#cWhite)"/>'
  '<path d="M44 124 Q90 60 190 58 Q290 60 336 124Z" fill="url(#cBread)"/>'
  '<g fill="#8a4f1e" opacity=".55"><circle cx="110" cy="104" r="6"/><circle cx="150" cy="86" r="6"/><circle cx="200" cy="78" r="6"/><circle cx="240" cy="92" r="6"/><circle cx="280" cy="106" r="6"/><circle cx="180" cy="104" r="6"/><circle cx="220" cy="112" r="6"/><circle cx="130" cy="114" r="5"/></g>'
  '<path d="M250 70 q16 -26 34 -10 q-12 18 -34 10Z" fill="url(#cGreen)"/>'
  +HL(70,170,16,40,.75,20)+HL(160,70,40,8,.6,-6)),
'POTATO':('0 0 320 240', '<ellipse cx="160" cy="226" rx="120" ry="12" fill="url(#cShade)"/>'
  '<path d="M30 130 Q20 50 120 40 Q220 26 280 80 Q320 130 270 180 Q210 220 120 206 Q40 196 30 130Z" fill="url(#cOat)"/>'
  '<g fill="#b98444" opacity=".6"><circle cx="110" cy="100" r="7"/><circle cx="190" cy="80" r="6"/><circle cx="230" cy="150" r="7"/><circle cx="140" cy="170" r="6"/></g>'
  '<path d="M200 50 q20 -30 44 -14 q-16 22 -44 14Z" fill="url(#cGreen)"/>'
  +HL(110,70,50,12,.65,-10)),
'MOON':('0 0 300 300', '<path d="M190 20 A130 130 0 1 0 280 220 A110 110 0 0 1 190 20Z" fill="url(#cYellow)"/>'
  '<circle cx="110" cy="170" r="14" fill="#e9b94a" opacity=".6"/><circle cx="150" cy="230" r="9" fill="#e9b94a" opacity=".6"/>'
  +HL(80,120,14,40,.75,20)),
})

SV.update({
'PALM':('0 0 300 380', '<ellipse cx="150" cy="366" rx="100" ry="12" fill="url(#cShade)"/>'
  '<rect x="78" y="40" width="40" height="170" rx="20" fill="url(#cSkin)"/><rect x="122" y="20" width="40" height="190" rx="20" fill="url(#cSkin)"/>'
  '<rect x="166" y="32" width="40" height="178" rx="20" fill="url(#cSkin)"/><rect x="210" y="64" width="36" height="150" rx="18" fill="url(#cSkin)"/>'
  '<path d="M74 170 Q70 330 150 340 Q236 340 248 250 L248 170Z" fill="url(#cSkin)"/>'
  '<path d="M84 230 Q40 200 28 160 Q22 136 44 134 Q66 136 92 190Z" fill="url(#cSkin)"/>'
  '<path d="M120 260 Q160 280 210 250" stroke="#d99272" stroke-width="5" fill="none" stroke-linecap="round" opacity=".6"/>'
  +HL(136,70,8,40,.6,0)+HL(180,80,7,36,.5,0)+HL(130,230,30,10,.5,-10)),
'FIST':('0 0 320 300', '<ellipse cx="160" cy="286" rx="120" ry="12" fill="url(#cShade)"/>'
  '<path d="M40 110 Q40 60 90 60 H250 Q290 60 290 110 V200 Q290 262 220 266 H110 Q40 262 40 200Z" fill="url(#cSkin)"/>'
  '<g fill="url(#cSkin)" stroke="#e0997a" stroke-width="4"><circle cx="90" cy="76" r="34"/><circle cx="150" cy="70" r="36"/><circle cx="210" cy="72" r="35"/><circle cx="262" cy="86" r="30"/></g>'
  '<path d="M60 170 Q120 140 200 160 Q230 168 236 190" stroke="#e0997a" stroke-width="22" fill="none" stroke-linecap="round"/>'
  '<path d="M60 170 Q120 140 200 160 Q230 168 236 190" stroke="url(#cSkin)" stroke-width="14" fill="none" stroke-linecap="round"/>'
  +HL(150,56,20,8,.7,0)+HL(90,62,16,6,.6,0)),
'THUMB':('0 0 300 320', '<ellipse cx="160" cy="306" rx="110" ry="12" fill="url(#cShade)"/>'
  '<path d="M70 150 Q48 70 70 26 Q84 6 104 16 Q122 28 116 80 L112 150Z" fill="url(#cSkin)"/>'
  '<path d="M60 160 Q60 132 96 132 H200 Q230 132 230 160 V260 Q230 296 192 296 H104 Q60 296 60 256Z" fill="url(#cSkin)"/>'
  '<g fill="url(#cSkin)" stroke="#e0997a" stroke-width="4"><rect x="180" y="134" width="96" height="40" rx="20"/><rect x="186" y="174" width="92" height="40" rx="20"/><rect x="186" y="214" width="88" height="40" rx="20"/><rect x="180" y="254" width="80" height="38" rx="19"/></g>'
  '<path d="M80 40 Q90 26 104 30" stroke="#ffeee2" stroke-width="9" fill="none" stroke-linecap="round"/>'
  +HL(84,90,8,34,.6,-12)+HL(120,170,30,10,.5,0)),
'OIL':('0 0 200 340', '<ellipse cx="100" cy="326" rx="76" ry="12" fill="url(#cShade)"/>'
  '<rect x="78" y="10" width="44" height="40" rx="10" fill="url(#cGreen)"/><path d="M84 50 H116 L124 96 H76Z" fill="#fff4c8"/>'
  '<path d="M60 100 Q60 90 76 90 H124 Q140 90 140 100 L166 170 V300 Q166 320 146 320 H54 Q34 320 34 300 V170Z" fill="url(#cYellow)"/>'
  '<rect x="50" y="190" width="100" height="80" rx="16" fill="#fff"/><path d="M100 210 q16 18 0 40 q-16 -22 0 -40Z" fill="url(#cGreen)"/>'
  +HL(56,150,10,40,.7,10)),
})

SV.update({
'CHOCO':('0 0 420 260', '<ellipse cx="210" cy="246" rx="180" ry="12" fill="url(#cShade)"/><rect x="22" y="32" width="208" height="208" rx="16" fill="#3d1f10"/><rect x="30" y="40" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="38" y="46" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="94" y="40" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="102" y="46" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="158" y="40" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="166" y="46" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="30" y="104" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="38" y="110" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="94" y="104" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="102" y="110" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="158" y="104" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="166" y="110" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="30" y="168" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="38" y="174" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="94" y="168" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="102" y="174" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><rect x="158" y="168" width="58" height="58" rx="10" fill="url(#cChoc)"/><rect x="166" y="174" width="42" height="10" rx="5" fill="#b77a52" opacity=".55"/><path d="M222 26 H392 Q404 26 404 38 V230 Q404 242 392 242 H222 L236 210 L220 180 L238 150 L220 120 L236 90 L220 60 Z" fill="url(#cRed)"/><rect x="260" y="104" width="120" height="64" rx="14" fill="#fff"/><text x="320" y="148" text-anchor="middle" font-family="Unb" font-weight="900" font-size="28" fill="#c8102e">шоко</text>'+HL(310,60,60,8,.6,0)),
'CHOCOSQ':('0 0 260 180', '<ellipse cx="130" cy="168" rx="100" ry="10" fill="url(#cShade)"/><g transform="rotate(-10 70 90)"><rect x="20" y="40" width="96" height="96" rx="14" fill="url(#cChoc)"/><rect x="32" y="50" width="70" height="16" rx="8" fill="#b77a52" opacity=".55"/></g><g transform="rotate(12 180 90)"><rect x="140" y="30" width="96" height="96" rx="14" fill="url(#cChoc)"/><rect x="152" y="40" width="70" height="16" rx="8" fill="#b77a52" opacity=".55"/></g>'),
})

SV.update({
'SUITCASE':('0 0 300 340', '<ellipse cx="150" cy="326" rx="110" ry="12" fill="url(#cShade)"/><path d="M110 70 V40 Q110 24 126 24 H174 Q190 24 190 40 V70" stroke="#2b2b33" stroke-width="16" fill="none"/><rect x="40" y="66" width="220" height="246" rx="34" fill="url(#cRed)"/><rect x="88" y="66" width="18" height="246" fill="#ff8a98" opacity=".7"/><rect x="194" y="66" width="18" height="246" fill="#ff8a98" opacity=".7"/><circle cx="80" cy="318" r="12" fill="#2b2b33"/><circle cx="220" cy="318" r="12" fill="#2b2b33"/><rect x="120" y="150" width="60" height="60" rx="14" fill="url(#cYellow)"/>'+HL(70,120,12,40,.6,0)),
'SUN':('0 0 300 300', '<rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(0 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(45 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(90 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(135 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(180 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(225 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(270 150 150)"/><rect x="141" y="10" width="18" height="50" rx="9" fill="url(#cYellow)" transform="rotate(315 150 150)"/><circle cx="150" cy="150" r="78" fill="url(#cYellow)"/>'+HL(120,120,22,12,.7,-30)),
})

SV.update({
'JEANS':('0 0 300 380', '<ellipse cx="150" cy="366" rx="110" ry="12" fill="url(#cShade)"/><path d="M40 40 H260 L276 356 H170 L150 150 L130 356 H24Z" fill="url(#cDenim)"/><rect x="36" y="30" width="228" height="44" rx="10" fill="#4a78c4"/><path d="M150 74 V150" stroke="#e8b04a" stroke-width="5" stroke-dasharray="10 7"/><path d="M70 74 Q86 120 128 116" stroke="#e8b04a" stroke-width="5" fill="none" stroke-dasharray="10 7"/><path d="M230 74 Q214 120 172 116" stroke="#e8b04a" stroke-width="5" fill="none" stroke-dasharray="10 7"/><circle cx="150" cy="52" r="14" fill="url(#cGold)"/><circle cx="150" cy="52" r="5" fill="#a86a1e"/>'+HL(70,180,10,60,.45,0)),
})

def svg(name,w,extra=''):
    vb,body=SV[name]; _,_,vw,vh=map(float,vb.split()); h=round(w*vh/vw)
    return f'<svg class="clay"{extra} width="{w}" height="{h}" viewBox="{vb}" overflow="visible">{body}</svg>'
