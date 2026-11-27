"""Prepare local JSON arguments for wms.oxr. This script makes no network requests."""

import argparse
import base64
import io
import json
import sys
from pathlib import Path


MAX_FILE_BYTES = 10 * 1024 * 1024
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def compact_image(source, limit):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise ValueError("图片超过参数上限。需要 Pillow 才能转码，也可换用更小的清晰图片。") from None

    with Image.open(source) as original:
        if getattr(original, "n_frames", 1) > 1:
            raise ValueError("多帧图片超过参数上限。请提供更小的原格式文件，以保留所有帧。")
        image = ImageOps.exif_transpose(original).convert("RGBA")
        rgb = Image.new("RGB", image.size, "white")
        rgb.paste(image, mask=image.getchannel("A"))
        for quality in (90, 80, 70):
            with io.BytesIO() as buffer:
                rgb.save(buffer, format="JPEG", quality=quality, subsampling=0, optimize=True)
                if buffer.tell() <= limit:
                    return buffer.getvalue()
    raise ValueError("同尺寸彩色 JPEG 仍超过参数上限。请提供更小且清晰的文件。")


def prepare(source, output, max_base64_chars):
    suffix = source.suffix.lower()
    if suffix not in IMAGE_SUFFIXES | {".pdf"}:
        raise ValueError("仅支持 PDF、PNG、JPEG、BMP、TIFF 和 WebP。")
    original_bytes = source.stat().st_size
    if not original_bytes:
        raise ValueError("附件为空。")
    limit = MAX_FILE_BYTES
    if max_base64_chars is not None:
        if max_base64_chars < 4:
            raise ValueError("--max-base64-chars 必须至少为 4。")
        limit = min(limit, (max_base64_chars // 4) * 3)

    converted = original_bytes > limit
    if converted and suffix == ".pdf":
        raise ValueError("PDF 超过参数上限。请提供更小的 PDF。")
    data = compact_image(source, limit) if converted else source.read_bytes()
    file_name = source.with_suffix(".jpg").name if converted else source.name
    encoded = base64.b64encode(data).decode("ascii")
    with output.open("x", encoding="utf-8") as stream:
        json.dump({"file": encoded, "fileName": file_name}, stream, ensure_ascii=False)
    return {
        "original_bytes": original_bytes,
        "prepared_bytes": len(data),
        "base64_chars": len(encoded),
        "converted_to_jpeg": converted,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attachment", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--max-base64-chars", type=int, help="客户端允许的 Base64 字符上限")
    args = parser.parse_args()
    try:
        metrics = prepare(args.attachment, args.output_json, args.max_base64_chars)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main())
