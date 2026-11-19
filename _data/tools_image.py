# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 2: Image & File Tools (6)."""

IMAGE_TOOLS = [
    {
        "slug": "image-compressor",
        "name": "Image Compressor",
        "cat": "image",
        "popular": True,
        "icon": "Ic",
        "title": "Image Compressor – Compress Images Online Free | CalcHub",
        "desc": "Compress JPG, PNG and WebP images in your browser. Free online image compressor with quality control and before/after size comparison.",
        "h1": "Image Compressor",
        "lede": "Reduce the file size of JPG, PNG or WebP images without uploading them anywhere. Adjust the quality slider and compare the original and compressed sizes in real time.",
        "howto": [
            "Click the upload area to choose an image, or drag and drop one.",
            "Move the quality slider to find the right balance between size and quality.",
            "Check the original vs compressed file size and the savings percentage.",
            "Download the compressed image when you are happy with the result."
        ],
        "examples": [
            "Compress a 2.4 MB product photo to a fast-loading web image.",
            "Shrink large PNG screenshots before attaching them to an email.",
            "Prepare JPG photos for a portfolio where load speed matters."
        ],
        "features": [
            "Compresses JPG, PNG and WebP images",
            "Quality slider for size/quality balance",
            "Shows original vs compressed size and savings",
            "Result is clearly labelled if compression increases file size",
            "Fully local — the file never leaves your browser"
        ],
        "privacy": "Your images are processed entirely in your browser. Files are never uploaded to a server, so nothing is stored or transmitted.",
        "faq": [
            {"q": "Which formats are supported?", "a": "JPG, PNG and WebP images work in all modern browsers. HEIC and other niche formats depend on browser support and may not be available."},
            {"q": "What if the 'compressed' file is bigger?", "a": "This can happen with already-compressed images or at very high quality settings. We show the real before/after sizes and never claim a compression that did not happen."},
            {"q": "Is there a file size limit?", "a": "Practical limits depend on your device and browser memory. Very large images may be slow to process, but ordinary photos and screenshots work fine."}
        ],
        "related": ["image-resizer", "png-to-webp", "jpg-to-png", "image-cropper"]
    },
    {
        "slug": "image-resizer",
        "name": "Image Resizer",
        "cat": "image",
        "popular": False,
        "icon": "Ir",
        "title": "Image Resizer – Resize Images Online Free | CalcHub",
        "desc": "Resize JPG, PNG or WebP images to exact dimensions in your browser. Free online image resizer with aspect ratio lock and presets.",
        "h1": "Image Resizer",
        "lede": "Resize an image to exact pixel dimensions for social media, websites or email — all locally in your browser. Lock the aspect ratio or use a preset to keep things simple.",
        "howto": [
            "Upload or drag-and-drop an image.",
            "Enter the target width and height, or pick a preset.",
            "Toggle 'Lock aspect ratio' to keep proportions when you change one value.",
            "Preview the result and download the resized image."
        ],
        "examples": [
            "Resize a photo to 1200×630 px for a social share card.",
            "Scale a logo to 200×200 px for a favicon base or avatar.",
            "Fit a large scan into a standard 8.5×11 ratio for printing."
        ],
        "features": [
            "Exact width and height control",
            "Aspect ratio lock",
            "Common presets (Instagram, Twitter, YouTube, avatar)",
            "Local processing with download",
            "Live preview"
        ],
        "privacy": "Resizing happens locally in your browser. Your image is never uploaded, so no copy exists on any server.",
        "faq": [
            {"q": "Will resizing reduce quality?", "a": "Shrinking images generally looks fine. Enlarging beyond the original resolution can blur the image; we do not upscale beyond what the source supports well."},
            {"q": "Does it keep the original aspect ratio automatically?", "a": "Only if you enable 'Lock aspect ratio'. When disabled, you can set width and height independently, which may stretch the image."},
            {"q": "Which formats can I export?", "a": "You can download the resized image in JPG or PNG. The original format is preserved by default when possible."}
        ],
        "related": ["image-compressor", "image-cropper", "jpg-to-png", "png-to-webp"]
    },
    {
        "slug": "jpg-to-png",
        "name": "JPG to PNG Converter",
        "cat": "image",
        "popular": False,
        "icon": "Jp",
        "title": "JPG to PNG Converter – Convert Images Online Free | CalcHub",
        "desc": "Convert JPG images to PNG in your browser. Free online JPG to PNG converter with lossless output and local processing.",
        "h1": "JPG to PNG Converter",
        "lede": "Convert a JPG image to PNG format. PNG gives you lossless quality and is a common requirement for logos, screenshots and transparency workflows — though JPG itself does not contain transparency.",
        "howto": [
            "Upload or drag-and-drop a JPG image.",
            "The preview shows your image as it will appear.",
            "Click Download PNG to save the converted file."
        ],
        "examples": [
            "Save a JPG screenshot as PNG so text and edges stay crisp.",
            "Convert a JPG to PNG before adding it to a document that requires PNG.",
            "Keep a lossless copy of an image for further editing."
        ],
        "features": [
            "One-click JPG to PNG conversion",
            "Lossless PNG output",
            "Live preview",
            "Local browser processing"
        ],
        "privacy": "Conversion happens entirely in your browser. Your image is never uploaded to a server.",
        "faq": [
            {"q": "Why does my JPG have a white background after conversion?", "a": "JPG files have no transparency channel — every pixel is opaque. When we convert to PNG, any area that was white stays white. We do not fake transparency that did not exist."},
            {"q": "Will the PNG be bigger than the JPG?", "a": "Usually yes. PNG is lossless and often larger than JPG at the same resolution. That is expected when you choose PNG."},
            {"q": "Is quality lost during conversion?", "a": "No. PNG encodes the pixels losslessly, so the image content from the original JPG is preserved exactly."}
        ],
        "related": ["png-to-webp", "image-compressor", "image-resizer", "favicon-generator"]
    },
    {
        "slug": "png-to-webp",
        "name": "PNG to WebP Converter",
        "cat": "image",
        "popular": False,
        "icon": "Pw",
        "title": "PNG to WebP Converter – Convert Images Free | CalcHub",
        "desc": "Convert PNG images to WebP in your browser. Free online PNG to WebP converter with quality control for faster websites.",
        "h1": "PNG to WebP Converter",
        "lede": "Convert PNG images to WebP for smaller, faster-loading web images. Adjust the quality level and check the size savings before you download.",
        "howto": [
            "Upload or drag-and-drop a PNG image.",
            "Choose a quality level (lower = smaller, usually).",
            "Check the size comparison with the original.",
            "Download the WebP file."
        ],
        "examples": [
            "Convert PNG logos and illustrations to WebP to speed up a website.",
            "Shrink PNG screenshots for a lighter page weight.",
            "Replace heavy PNG assets in an email template or blog."
        ],
        "features": [
            "PNG to WebP conversion with quality control",
            "Shows original vs WebP file size",
            "Checks browser support for WebP encoding",
            "Local processing only"
        ],
        "privacy": "Images are processed locally in your browser and never uploaded to a server.",
        "faq": [
            {"q": "Does every browser support WebP?", "a": "WebP is supported by all modern browsers. We also detect encoding support in the browser you are using and warn you if it is not available."},
            {"q": "Will my transparent PNG stay transparent?", "a": "Yes. WebP supports transparency, so transparent areas are preserved correctly."},
            {"q": "Is WebP always smaller than PNG?", "a": "Usually, especially for photos and complex illustrations. For simple graphics with few colours, the difference can be small. We show the real comparison."}
        ],
        "related": ["jpg-to-png", "image-compressor", "image-resizer", "favicon-generator"]
    },
    {
        "slug": "image-cropper",
        "name": "Image Cropper",
        "cat": "image",
        "popular": False,
        "icon": "Cr",
        "title": "Image Cropper – Crop Images Online Free | CalcHub",
        "desc": "Crop JPG, PNG or WebP images to any size in your browser. Free online image cropper with aspect presets and touch support.",
        "h1": "Image Cropper",
        "lede": "Crop an image to remove unwanted areas or match a specific aspect ratio. Preset ratios help you prepare images for social media, cards, avatars and print.",
        "howto": [
            "Upload or drag-and-drop an image.",
            "Drag the crop area to choose what to keep.",
            "Select an aspect ratio preset or leave it free.",
            "Download the cropped image."
        ],
        "examples": [
            "Crop a landscape photo to 1:1 for a profile picture.",
            "Cut a photo to 16:9 for a YouTube thumbnail.",
            "Remove extra background from a product screenshot."
        ],
        "features": [
            "Drag-and-resize crop area",
            "Common aspect ratio presets (1:1, 4:3, 16:9, 9:16)",
            "Free-form cropping",
            "Touch-friendly on mobile",
            "Local processing with download"
        ],
        "privacy": "Cropping happens locally in your browser. Your image is never uploaded, stored or transmitted.",
        "faq": [
            {"q": "Can I change the crop area after selecting a preset?", "a": "Yes. You can drag the crop area around and adjust its edges within the preset ratio."},
            {"q": "What happens to pixels outside the crop area?", "a": "They are removed. Only the area inside the crop box is kept in the exported image."},
            {"q": "Does cropping reduce quality?", "a": "No. Cropping removes pixels but does not recompress the kept area, so quality is preserved."}
        ],
        "related": ["image-resizer", "image-compressor", "jpg-to-png", "png-to-webp"]
    },
    {
        "slug": "favicon-generator",
        "name": "Favicon Generator",
        "cat": "image",
        "popular": False,
        "icon": "Fg",
        "title": "Favicon Generator – Create Favicon Images Free | CalcHub",
        "desc": "Generate favicon PNGs in common sizes from any image. Free online favicon generator with 16, 32, 48, 64 and 128 px outputs.",
        "h1": "Favicon Generator",
        "lede": "Turn any square image into browser favicons in the standard sizes. Export PNG icons at 16, 32, 48, 64 and 128 pixels, ready to drop into your website.",
        "howto": [
            "Upload a square image (PNG or JPG).",
            "Preview the resized favicon sizes.",
            "Download the full set as individual PNG files."
        ],
        "examples": [
            "Generate a 16×16 and 32×32 favicon for your domain.",
            "Create a 192×192 icon for Android home screens.",
            "Prepare a 512×512 app icon base from a logo."
        ],
        "features": [
            "Exports 16, 32, 48, 64 and 128 px PNG favicons",
            "Preview of each size",
            "Square crop automatic",
            "Local browser processing"
        ],
        "privacy": "Your logo is processed locally in your browser and is never uploaded to a server.",
        "faq": [
            {"q": "Do you generate .ico files?", "a": "We generate PNG favicons in standard sizes, which work in all modern browsers. We do not fake .ico files by renaming PNGs, because that produces unusable icons."},
            {"q": "Which favicon size is most important?", "a": "32×32 (browser tab) and 16×16 (fallback) are the most important for desktop browsers. 192 and 512 px are used by mobile home screens."},
            {"q": "Does the source need to be square?", "a": "We crop the source to a square automatically, focusing on the centre, so a non-square logo will still work — check the preview."}
        ],
        "related": ["image-resizer", "image-compressor", "png-to-webp", "jpg-to-png"]
    },
]