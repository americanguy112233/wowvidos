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

def svg(name,w,extra=''):
    vb,body=SV[name]; _,_,vw,vh=map(float,vb.split()); h=round(w*vh/vw)
    return f'<svg class="clay"{extra} width="{w}" height="{h}" viewBox="{vb}" overflow="visible">{body}</svg>'
