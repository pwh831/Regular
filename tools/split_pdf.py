"""폴더 안의 PDF를 60쪽씩 나눠 새 폴더에 저장한다. 원본 파일은 건드리지 않는다.

준비: pip install pypdf
사용: python split_pdf.py "C:\\Users\\이름\\Desktop\\2-2 중간"
결과: 같은 위치에 "2-2 중간 (60쪽씩)" 폴더가 생기고,
      교사용_교과서_001-060쪽.pdf, 교사용_교과서_061-120쪽.pdf ... 처럼 저장된다.
"""
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

PAGES = 60


def main():
    if len(sys.argv) < 2:
        print('사용법: python split_pdf.py "PDF가 있는 폴더 경로"')
        sys.exit(1)
    src = Path(sys.argv[1].strip('"')).expanduser()
    if not src.is_dir():
        print(f"폴더를 찾지 못했어요: {src}")
        sys.exit(1)
    pdfs = sorted(p for p in src.iterdir() if p.suffix.lower() == ".pdf")
    if not pdfs:
        print(f"PDF가 없어요: {src}")
        sys.exit(1)

    out = src.parent / f"{src.name} ({PAGES}쪽씩)"
    out.mkdir(exist_ok=True)

    for pdf in pdfs:
        try:
            reader = PdfReader(pdf)
            if reader.is_encrypted:
                reader.decrypt("")
            total = len(reader.pages)
        except Exception as e:
            print(f"건너뜀 {pdf.name}: 열 수 없어요 ({e})")
            continue
        width = max(3, len(str(total)))
        for start in range(0, total, PAGES):
            end = min(start + PAGES, total)
            writer = PdfWriter()
            for i in range(start, end):
                writer.add_page(reader.pages[i])
            name = f"{pdf.stem}_{start + 1:0{width}d}-{end:0{width}d}쪽.pdf"
            with open(out / name, "wb") as f:
                writer.write(f)
        print(f"{pdf.name}: {total}쪽 → {-(-total // PAGES)}개 파일")

    print(f"\n끝났어요. 나눈 파일은 여기 있어요: {out}")


if __name__ == "__main__":
    main()
