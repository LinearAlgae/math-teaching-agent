#!/usr/bin/env python3
import os
import glob
import base64
import time
import argparse
from io import BytesIO
from PIL import Image
from openai import OpenAI
import pymupdf

DEFAULT_OUTPUT_DIR = "resource/markdown_output"
DEFAULT_MODEL = "google/gemma-4-e2b"
DEFAULT_API_URL = "http://localhost:1234/v1"

client = OpenAI(base_url=DEFAULT_API_URL, api_key="lm-studio")

def describe_image(image_bytes, page_context="", img_index=0, debug=False):
    if debug:
        print(f"    [Image {img_index}] Processing...", flush=True)
    
    for attempt in range(3):
        try:
            image = Image.open(BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            if max(image.size) > 512:
                ratio = 512 / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            if debug:
                print(f"    [Image {img_index}] Encoded: {len(img_b64)} bytes", flush=True)
            
            context_info = f"\n\n頁面上下文:\n{page_context[:1000]}...\n\n" if len(page_context.strip()) > 10 else ""
            prompt = f"請詳細描述這張數學教材圖片的內容，包括所有元素、文字、數學符號、圖表結構等。{context_info}中文回答。"
            
            if debug:
                print(f"    [Image {img_index}] Calling API (attempt {attempt+1}/3)...", flush=True)
            
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{'role': 'user', 'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}}
                ]}],
                timeout=600
            )
            
            if debug:
                print(f"    [Image {img_index}] Got response!", flush=True)
            
            content = response.choices[0].message.content or ""
            reasoning = response.choices[0].message.reasoning_content or ""
            result = content if content else reasoning
            
            if debug:
                print(f"    [Image {img_index}] Description length: {len(result)}", flush=True)
            return result
        except Exception as e:
            if debug:
                print(f"    [Image {img_index}] Error: {e}", flush=True)
            if attempt < 2:
                time.sleep(3)
            else:
                return f"[Error: {e}]"
    return "[Max retries exceeded]"

def convert_pdf(pdf_path, output_path, debug=False):
    if debug:
        print(f"Opening: {pdf_path}", flush=True)
    
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    
    if debug:
        print(f"  {total_pages} pages", flush=True)
    
    text_parts = []
    
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        text_parts.append(text)
        
        images = []
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            w, h = base_image["width"], base_image["height"]
            img_bytes = base_image["image"]
            if w >= 100 and h >= 100 and len(img_bytes) >= 5000:
                images.append({'bytes': img_bytes, 'w': w, 'h': h})
        
        if images:
            if debug:
                print(f"  Page {page_num+1}: {len(images)} images", flush=True)
            text_parts.append(f"\n\n[Images: {len(images)}]\n")
            for img_idx, img in enumerate(images):
                desc = describe_image(img['bytes'], page_context=text, img_index=img_idx+1, debug=debug)
                text_parts.append(f"[Image {img_idx+1} {img['w']}x{img['h']}]:\n{desc}\n")
                time.sleep(2)
        
        full_text = '\n'.join(text_parts)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        if debug:
            print(f"  Saved progress: {len(full_text)} chars", flush=True)
    
    doc.close()
    
    full_text = '\n'.join(text_parts)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    if debug:
        print(f"  Done! {os.path.getsize(output_path)} bytes", flush=True)
    return len(full_text)

def main():
    parser = argparse.ArgumentParser(description='Convert PDF files to markdown with image descriptions')
    parser.add_argument('--input', '-i', default='Resource', help='Input directory containing PDFs (default: Resource)')
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT_DIR, help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable detailed debug logging')
    parser.add_argument('--force', '-f', action='store_true', help='Force reconvert existing files')
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL, help=f'Model to use (default: {DEFAULT_MODEL})')
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(args.input, "**/*.pdf"), recursive=True)
    
    if not pdf_files:
        print(f"No PDF files found in {args.input}")
        return
    
    pdf_files = [f for f in pdf_files if not f.endswith('.pdf.pdf')]
    
    def get_relative_path(pdf_path):
        rel = os.path.relpath(pdf_path, args.input)
        return rel.replace('.pdf', '.md')
    
    print(f"Found {len(pdf_files)} PDF files")
    print(f"Output directory: {args.output}")
    print()
    
    converted = 0
    skipped = 0
    errors = 0
    
    for i, pdf_path in enumerate(pdf_files):
        rel_path = get_relative_path(pdf_path)
        md_path = os.path.join(args.output, rel_path)
        
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        
        if os.path.exists(md_path) and not args.force:
            skipped += 1
            if not args.debug:
                print(f"[{i+1}/{len(pdf_files)}] SKIP (already converted): {os.path.basename(pdf_path)}")
            else:
                print(f"[{i+1}/{len(pdf_files)}] SKIP: {pdf_path} -> {md_path}")
            continue
        
        if not args.debug:
            print(f"[{i+1}/{len(pdf_files)}] Converting: {os.path.basename(pdf_path)}")
        
        try:
            start = time.time()
            length = convert_pdf(pdf_path, md_path, debug=args.debug)
            elapsed = time.time() - start
            
            converted += 1
            
            if args.debug:
                print(f"[{i+1}/{len(pdf_files)}] Done: {pdf_path} ({length} chars, {elapsed:.1f}s)")
            else:
                size_kb = os.path.getsize(md_path) / 1024
                print(f"        -> {length} chars, {elapsed:.1f}s, {size_kb:.1f}KB")
        except Exception as e:
            errors += 1
            print(f"[{i+1}/{len(pdf_files)}] ERROR: {pdf_path} - {e}")
    
    print()
    print(f"Conversion complete!")
    print(f"  Converted: {converted}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()