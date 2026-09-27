#!/usr/bin/env bash
# 국어 변형 출제실의 PDF 글꼴을 만든다 (Gowun Batang/Dodum, SIL OFL).
# 결과: fonts/*.ttf(전체)와 fonts/*.ks.ttf(자주 쓰는 한글 2350자 + 기호, 힌팅 제거) — 앱을 발행할 때 files로 함께 올린다.
# 준비: pip install fonttools
set -euo pipefail
out=${1:-fonts}; mkdir -p "$out"
for f in gowunbatang/GowunBatang-Regular gowunbatang/GowunBatang-Bold gowundodum/GowunDodum-Regular; do
  curl -sSL -o "$out/$(basename $f).ttf" "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/$f.ttf"
done
ks=$(python3 -c "
s=[]
for c in range(0xAC00,0xD7A4):
    try:
        if len(chr(c).encode('euc-kr'))==2: s.append('U+%04X'%c)
    except: pass
print(','.join(s))")
for n in GowunBatang-Regular GowunBatang-Bold GowunDodum-Regular; do
  pyftsubset "$out/$n.ttf" --unicodes="U+0020-007E,U+00A0-00FF,U+2000-206F,U+2100-218F,U+2190-21FF,U+2200-22FF,U+2460-24FF,U+25A0-26FF,U+3000-303F,U+3131-318E,U+3200-32FF,U+FF01-FF5E,$ks" \
    --no-hinting --drop-tables+=DSIG,GSUB,GPOS --layout-features='' --output-file="$out/$n.ks.ttf"
done
ls -la "$out"
