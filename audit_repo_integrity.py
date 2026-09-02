import os
import re
import glob

def check_broken_links_and_files():
    print("=== Checking File Links & References ===")
    root_dir = os.path.abspath(".")
    
    # Files to check
    files_to_check = ["README.md", "manuscript.md", "index.html", "CITATION.cff"]
    
    for fpath in files_to_check:
        if not os.path.exists(fpath):
            print(f"Missing file: {fpath}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        print(f"\n--- Checking {fpath} ---")
        # Check href / src in html or markdown links
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]|src=[\'"]([^\'"]+)[\'"]|\[[^\]]+\]\(([^)]+)\)', content)
        all_links = []
        for l in links:
            for item in l:
                if item:
                    all_links.append(item)
                    
        for link in set(all_links):
            # Ignore web links, anchors, mailto
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.startswith("mailto:") or link.startswith("javascript:"):
                continue
            # Remove url params or anchor
            clean_link = link.split("#")[0].split("?")[0]
            if not clean_link:
                continue
            if not os.path.exists(clean_link):
                print(f"  [POTENTIAL BROKEN LINK] in {fpath}: '{link}' -> File not found on disk: {clean_link}")
            else:
                pass # print(f"  [OK] {link}")

def check_spelling_and_typos():
    print("\n=== Checking Common Typos in Text Files ===")
    typo_patterns = [
        r'\bcollumella\b', r'\bcollumelar\b', r'\bautodecoder\b', r'\btransverese\b',
        r'\bdiaplying\b', r'\bvisulsiation\b', r'\bvisulsation\b', r'\bmodle\b',
        r'\boccured\b', r'\bseperated\b', r'\bteh\b', r'\badirion\b', r'\bimrpove\b',
        r'\bavliablec\b', r'\bdeomains\b', r'\bidentifid\b', r'\boritented\b',
        r'\bworkign\b', r'\bflroal\b', r'\beat of\b', r'\bshold\b', r'\bdedox\b'
    ]
    
    check_files = glob.glob("*.md") + glob.glob("*.html") + glob.glob("data/*.js") + glob.glob("*.py")
    
    for fpath in check_files:
        if "zenodo_package" in fpath or ".git" in fpath:
            continue
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            for pat in typo_patterns:
                m = re.search(pat, line, re.IGNORECASE)
                if m:
                    print(f"  [TYPO/KEYWORD MATCH] in {fpath}:{i+1} -> '{m.group(0)}' in line: {line.strip()[:100]}")

if __name__ == "__main__":
    check_broken_links_and_files()
    check_spelling_and_typos()
