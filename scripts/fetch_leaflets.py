import os, pathlib, requests

OUT_DIR = pathlib.Path("data/leaflets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# CDC (public domain unless noted): English PDFs
CDC_PDFS = {
    # Antibiotic use patient education
    # "prevention-brochure.pdf": "https://www.cdc.gov/hivnexus/media/pdfs/2024/04/cdc-lsht-prevention-brochure-clinicians-quick-guide-what-is-injectable-hiv-prep.pdf",  # example brochure
    # You can add more CDC printable PDFs by pasting their direct links below:
    "cdc-hiv-teesting-models-lessons-summary.pdf": "https://www.cdc.gov/hivpartners/media/pdfs/2024/11/cdc-hiv-teesting-models-lessons-summary.pdf",
    "cdc-lsht-testing-brochure-understanding-test-results-patient.pdf": "https://www.cdc.gov/hivnexus/media/pdfs/2024/04/cdc-lsht-testing-brochure-understanding-test-results-patient.pdf",
    "cdc-hiv-consumer-info-sheet-safer-sex-2023-508.pdf": "https://www.cdc.gov/hiv/resourcelibrary/infosheets/cdc-hiv-consumer-info-sheet-safer-sex-2023-508.pdf",
    "prep-pocket-guide_together-branded.pdf": "https://www.cdc.gov/hiv/resourcelibrary/pocketguides/prep-pocket-guide_together-branded.pdf",
    "cdc-hiv-consumer-info-sheet-idu-101-2023-508.pdf": "https://www.cdc.gov/hiv/resourcelibrary/infosheets/cdc-hiv-consumer-info-sheet-idu-101-2023-508.pdf"
    }   

# NCI (copyright-free text; many pages are HTML, but some PDFs exist too)
NCI_PDFS = {
    # Add PDFs as you find them; many PDQ summaries are HTML (you can later add HTML ingestion).
    # Example (if a PDF is available):
    "nci_cancer_staging_basics.pdf": "https://www.cancer.gov/publications/pdq/some-pdf.pdf"
}

# NHS (OGL v3.0): use with attribution (“Information from the NHS website is licensed under the OGL v3.0.”)
NHS_PDFS = {
    # Many NHS patient pages are HTML; for PDFs, prefer their downloadable leaflets.
    # Example placeholders (replace with real PDF URLs you pick):
    "nhs_high_blood_pressure_leaflet.pdf": "https://assets.nhs.uk/some/path/hypertension-leaflet.pdf"
}

# Taiwan HPA / 健康九九 (Government Open Data License; attribute the source)
HPA_PDFS = {
    # Health literacy toolkit (Traditional Chinese)
    "hpa_health_literacy_toolkit_zh.pdf": "https://health99.hpa.gov.tw/media/public/pdf/22136.pdf",
    # You can add more: browse 健康九九 “宣導品/手冊/單張” items that provide "檔案下載"
    # Example placeholder:
    # "hpa_diabetes_patient_handbook_zh.pdf": "https://health99.hpa.gov.tw/media/public/pdf/xxxx.pdf"
}

URLS = {}
URLS.update(CDC_PDFS)
URLS.update(NCI_PDFS)
URLS.update(NHS_PDFS)
URLS.update(HPA_PDFS)

def fetch(name, url):
    out = OUT_DIR / name
    if out.exists():
        print(f"[skip] {name}")
        return
    print(f"[get ] {name} <- {url}")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    out.write_bytes(r.content)
    print(f"[done] {name} ({out.stat().st_size/1024:.1f} KB)")

if __name__ == "__main__":
    for name, url in URLS.items():
        try:
            fetch(name, url)
        except Exception as e:
            print(f"[fail] {name}: {e}")
