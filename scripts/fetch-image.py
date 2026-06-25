#!/usr/bin/env python3
"""
fetch-image.py — 从 Unsplash / Pexels / Pixabay 搜索并下载图片，自动更新文章 frontmatter。

用法：
  # 全自动（取第一张，用于脚本/Agent）
  python3 scripts/fetch-image.py <markdown文件路径> [关键词] --auto

  # 只下载图片，返回 URL（用于内嵌图片）
  python3 scripts/fetch-image.py --inline <关键词> <输出文件名（不含扩展名）>

环境变量：
  UNSPLASH_ACCESS_KEY   — Unsplash API Key（优先使用）
  UNSPLASH_ACCESS_KEY_2 — Unsplash 备用 Key
  PEXELS_API_KEY        — Pexels API Key（Unsplash 无结果时 fallback）
  PIXABAY_API_KEY       — Pixabay API Key（Pexels 也无结果时最终 fallback）
"""

import os
import re
import sys
import json
import shutil
import urllib.request
import urllib.parse
import urllib.error

# ── 配置 ──────────────────────────────────────────────────────────────────────

UNSPLASH_API_BASE = "https://api.unsplash.com"
PEXELS_API_BASE   = "https://api.pexels.com/v1"
PIXABAY_API_BASE  = "https://pixabay.com/api"
IMAGE_DIR         = "public/images"
IMAGE_URL_PREFIX  = "/images"
IMAGE_WIDTH       = 1920
IMAGE_HEIGHT      = 1080
SITE_KEY = os.environ.get("SITE_KEY", "diy_maker_station").replace("-", "_")

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80]


def parse_frontmatter(content: str) -> tuple[dict, str, str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not match:
        return {}, "", content
    raw = match.group(1)
    body = match.group(2)
    fm = {}
    for line in raw.split("\n"):
        if ": " in line:
            key, _, val = line.partition(": ")
            fm[key.strip()] = val.strip().strip('"')
        elif line.endswith(":"):
            fm[line.rstrip(":")] = ""
    return fm, raw, body


def update_frontmatter(content: str, key: str, value: str) -> str:
    match = re.match(r"^(---\n)(.*?)(\n---\n?)(.*)", content, re.DOTALL)
    if not match:
        return content
    prefix, raw, suffix, body = match.groups()
    lines = raw.split("\n")
    updated = False
    new_lines = []
    for line in lines:
        if re.match(rf"^{re.escape(key)}\s*:", line):
            new_lines.append(f'{key}: "{value}"')
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        insert_idx = next(
            (i for i, l in enumerate(new_lines) if l.startswith("draft:")),
            len(new_lines)
        )
        new_lines.insert(insert_idx, f'{key}: "{value}"')
    return prefix + "\n".join(new_lines) + suffix + body


def download_image(url: str, dest_path: str, headers: dict | None = None) -> None:
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "central-intelligence/1.0"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(resp, f)


def get_project_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


# ── Unsplash ──────────────────────────────────────────────────────────────────

def unsplash_search(query: str, per_page: int = 5) -> list[dict]:
    keys = []
    k1 = os.environ.get("UNSPLASH_ACCESS_KEY", "").strip()
    k2 = os.environ.get("UNSPLASH_ACCESS_KEY_2", "").strip()
    if k1: keys.append(k1)
    if k2 and k2 != k1: keys.append(k2)
    if not keys:
        return []

    params = urllib.parse.urlencode({
        "query": query, "per_page": per_page,
        "orientation": "landscape", "order_by": "relevant",
    })
    url = f"{UNSPLASH_API_BASE}/search/photos?{params}"

    for key in keys:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Client-ID {key}", "Accept-Version": "v1",
        })
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("results", [])
                if results:
                    return [{"_source": "unsplash", **r} for r in results]
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                print(f"⚠️  Unsplash key 受限 ({e.code})，尝试下一个", file=sys.stderr)
                continue
        except Exception:
            pass
    return []


def save_unsplash(photo: dict, filename_slug: str) -> tuple[str, str, str]:
    """返回 (image_url, alt_text, attribution_html)"""
    project_root = get_project_root()
    img_dir = os.path.join(project_root, IMAGE_DIR)
    os.makedirs(img_dir, exist_ok=True)
    dest_path = os.path.join(img_dir, f"{filename_slug}.jpg")

    raw_url = photo["urls"]["raw"]
    dl_url = f"{raw_url}&w={IMAGE_WIDTH}&h={IMAGE_HEIGHT}&fit=crop&auto=format&q=85"
    download_image(dl_url, dest_path)

    image_url = f"{IMAGE_URL_PREFIX}/{filename_slug}.jpg"
    alt_text = (photo.get("alt_description") or photo.get("description") or filename_slug)[:120]
    author_name = photo["user"]["name"]
    author_url  = photo["user"]["links"]["html"]
    attribution = f'Photo by <a href="{author_url}?utm_source={SITE_KEY}&utm_medium=referral">{author_name}</a> on Unsplash'
    return image_url, alt_text, attribution


# ── Pexels ────────────────────────────────────────────────────────────────────

def pexels_search(query: str, per_page: int = 5) -> list[dict]:
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return []

    params = urllib.parse.urlencode({
        "query": query, "per_page": per_page,
        "orientation": "landscape",
    })
    url = f"{PEXELS_API_BASE}/search?{params}"
    req = urllib.request.Request(url, headers={"Authorization": key})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("photos", [])
            return [{"_source": "pexels", **r} for r in results]
    except Exception as e:
        print(f"⚠️  Pexels 搜索失败：{e}", file=sys.stderr)
        return []


def save_pexels(photo: dict, filename_slug: str) -> tuple[str, str, str]:
    """返回 (image_url, alt_text, attribution_html)"""
    project_root = get_project_root()
    img_dir = os.path.join(project_root, IMAGE_DIR)
    os.makedirs(img_dir, exist_ok=True)
    dest_path = os.path.join(img_dir, f"{filename_slug}.jpg")

    dl_url = photo["src"].get("large2x") or photo["src"].get("large") or photo["src"]["original"]
    download_image(dl_url, dest_path, headers={
        "Authorization": os.environ.get("PEXELS_API_KEY", ""),
        "User-Agent": "central-intelligence/1.0",
    })

    image_url = f"{IMAGE_URL_PREFIX}/{filename_slug}.jpg"
    alt_text = (photo.get("alt") or filename_slug)[:120]
    photographer = photo.get("photographer", "Unknown")
    photo_url    = photo.get("url", "https://www.pexels.com")
    attribution  = f'Photo by <a href="{photo_url}">{photographer}</a> on Pexels'
    return image_url, alt_text, attribution


# ── Pixabay ───────────────────────────────────────────────────────────────────

def pixabay_search(query: str, per_page: int = 5) -> list[dict]:
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return []
    params = urllib.parse.urlencode({
        "key": key, "q": query, "per_page": per_page,
        "image_type": "photo", "orientation": "horizontal",
        "safesearch": "true",
    })
    try:
        with urllib.request.urlopen(f"{PIXABAY_API_BASE}/?{params}", timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return [{"_source": "pixabay", **h} for h in data.get("hits", [])]
    except Exception as e:
        print(f"⚠️  Pixabay 搜索失败：{e}", file=sys.stderr)
        return []


def save_pixabay(photo: dict, filename_slug: str) -> tuple[str, str, str]:
    project_root = get_project_root()
    img_dir = os.path.join(project_root, IMAGE_DIR)
    os.makedirs(img_dir, exist_ok=True)
    dest_path = os.path.join(img_dir, f"{filename_slug}.jpg")

    dl_url = photo.get("largeImageURL") or photo.get("webformatURL")
    download_image(dl_url, dest_path)

    image_url   = f"{IMAGE_URL_PREFIX}/{filename_slug}.jpg"
    alt_text    = (photo.get("tags", "") or filename_slug)[:120]
    user        = photo.get("user", "Unknown")
    page_url    = photo.get("pageURL", "https://pixabay.com")
    attribution = f'Photo by <a href="{page_url}">{user}</a> on Pixabay'
    return image_url, alt_text, attribution


# ── 统一搜索入口（Unsplash → Pexels → Pixabay fallback） ─────────────────────

def search_photo(query: str, per_page: int = 5) -> list[dict]:
    results = unsplash_search(query, per_page)
    if results:
        return results
    print(f"⚠️  Unsplash 无结果，切换 Pexels…", file=sys.stderr)
    results = pexels_search(query, per_page)
    if results:
        return results
    print(f"⚠️  Pexels 无结果，切换 Pixabay…", file=sys.stderr)
    return pixabay_search(query, per_page)


def save_photo(photo: dict, filename_slug: str) -> tuple[str, str, str]:
    source = photo.get("_source", "unsplash")
    if source == "pexels":
        return save_pexels(photo, filename_slug)
    if source == "pixabay":
        return save_pixabay(photo, filename_slug)
    return save_unsplash(photo, filename_slug)


# ── 主流程 ────────────────────────────────────────────────────────────────────

def mode_inline(args: list[str]) -> None:
    if len(args) < 2:
        print("用法：python3 fetch-image.py --inline <关键词> <文件名slug>", file=sys.stderr)
        sys.exit(1)
    query = args[0]
    filename_slug = slugify(args[1])
    results = search_photo(query, per_page=3)
    if not results:
        print(f"❌ 没有找到图片：{query}", file=sys.stderr)
        sys.exit(1)
    image_url, alt_text, attribution = save_photo(results[0], filename_slug)
    print(f"![{alt_text}]({image_url})")
    print(attribution)


def mode_cover(md_path: str, query: str, auto: bool) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    fm, _, _ = parse_frontmatter(content)
    title = fm.get("title", "")
    if not title:
        print("❌ 文章缺少 title 字段", file=sys.stderr)
        sys.exit(1)

    if not query:
        stopwords = {"i","my","a","an","the","for","to","how","why","what",
                     "when","where","under","with","and","or"}
        words = [w for w in re.sub(r"[^\w\s]","",title.lower()).split()
                 if w not in stopwords]
        query = " ".join(words[:5])

    print(f"📷 搜索关键词：{query}", file=sys.stderr)
    results = search_photo(query)
    if not results:
        print("❌ 没有找到相关图片", file=sys.stderr)
        sys.exit(1)

    if auto:
        selected = results[0]
    else:
        print("\n搜索结果：")
        for i, photo in enumerate(results):
            source = photo.get("_source","unsplash")
            if source == "pexels":
                desc = photo.get("alt","（无描述）")
                author = photo.get("photographer","Unknown")
            else:
                desc = photo.get("description") or photo.get("alt_description") or "（无描述）"
                author = photo["user"]["name"]
            print(f"  [{i+1}] [{source}] {desc[:55]}  — {author}")
        print("  [0] 跳过")
        while True:
            try:
                choice = int(input(f"\n请选择图片编号 [0-{len(results)}]：").strip())
                if 0 <= choice <= len(results): break
            except (ValueError, EOFError): pass
        if choice == 0:
            print("⏭  已跳过")
            sys.exit(0)
        selected = results[choice - 1]

    filename_slug = slugify(title)
    image_url, alt_text, attribution = save_photo(selected, filename_slug)

    content = update_frontmatter(content, "image", image_url)
    content = update_frontmatter(content, "imageAlt", alt_text)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    source = selected.get("_source", "unsplash")
    print(f"✅ 封面图已保存 [{source}]", file=sys.stderr)
    print(f"   image: {image_url}", file=sys.stderr)
    print(f"\n📌 署名：{attribution}", file=sys.stderr)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--inline":
        mode_inline(args[1:])
        return

    md_path = args[0]
    if not os.path.isfile(md_path):
        print(f"❌ 找不到文件：{md_path}", file=sys.stderr)
        sys.exit(1)

    auto = "--auto" in args
    remaining = [a for a in args[1:] if a != "--auto"]
    query = " ".join(remaining) if remaining else ""
    mode_cover(md_path, query, auto)


if __name__ == "__main__":
    main()
