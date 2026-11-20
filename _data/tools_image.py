# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 2: Image & File Tools (6).

Every claim below is checked against the widget markup in _scripts/build.py
and the runners in assets/js/tools.js. In particular: the compressor always
exports JPEG with two sliders (scale 10-100 @5, quality 10-100 @5), the
resizer and cropper always export PNG, the crop box is fixed at the centre,
and the favicon tool exports PNG only.
"""

IMAGE_TOOLS = [
    {
        "slug": "image-compressor",
        "name": "Image Compressor",
        "cat": "image",
        "popular": True,
        "icon": "Ic",
        "title": "Image Compressor — Shrink a Photo Before You Download | CalcHub",
        "desc": "Reduce an image's file size with a quality slider and optional scaling. Compare original and output sizes before downloading a JPG, all in your browser.",
        "h1": "Image Compressor",
        "lede": "Oversized photos are a common reason a page loads slowly or an attachment gets rejected. This tool re-encodes an image at settings you choose, then shows the exact size difference so you can judge whether the trade-off is worth it.",
        "howto": [
            "Drop an image onto the panel or click to choose one. The picker accepts JPG, PNG and WebP files.",
            "Set the Resize slider. It starts at 80%, which scales the pixel dimensions down as well as re-encoding.",
            "Set JPEG quality. Lower values discard more detail and usually produce a smaller file; the default is 80%.",
            "Compare Original, Output and Dimensions in the info line, check the preview, then Download compressed JPG."
        ],
        "examples": [
            "A 3 MB photo from a phone at 80% scale and 80% quality often lands well under 1 MB, with a visible but usually acceptable loss of fine texture.",
            "A simple logo with flat colours may barely shrink, because there is little detail for JPEG to discard.",
            "A PNG screenshot with sharp text can come out larger than the original; the tool flags this instead of claiming a saving."
        ],
        "understanding": [
            "Two separate settings change the file size. The Resize slider reduces the pixel dimensions — 80% means 80% of the original width and height — which permanently removes detail. The quality slider controls how much detail JPEG keeps within those dimensions: lower values simplify colour and texture information, which is where most of the saving comes from.",
            "The info line reports the original size, the output size and the new dimensions. The result line states the percentage saved, or tells you plainly when the output is larger. The preview shows the re-encoded image rather than the source, so what you see is what the download contains.",
            "Format matters too. JPEG is lossy and suits photographs; PNG is lossless and suits text, screenshots and transparency; WebP usually packs photographic detail more efficiently than either. This tool always writes JPEG, so a transparent PNG loses its transparency and an already-compressed WebP may not improve."
        ],
        "limitations": [
            "The output is always a JPEG, whatever the input format. Transparent areas in a PNG are not preserved, and EXIF metadata such as camera settings is not carried over.",
            "Results vary by image. Detailed photos compress well; flat graphics, text-heavy screenshots and files that are already heavily compressed may shrink little or even grow, in which case the tool says so.",
            "Both sliders are destructive. Scaling down and re-encoding cannot be undone in the output, so keep your original file.",
            "There is no choice of output format here. Use the JPG to PNG or PNG to WebP converters if you need a different file type, or set Resize to 100% if you only want to change quality.",
            "One image is handled at a time, and very large files are limited by your browser's memory because the whole image is drawn into a canvas on your device."
        ],
        "privacy": "The image is decoded and re-encoded on your device. It is never uploaded to a server.",
        "faq": [
            {"q": "Which formats can I open, and what do I get back?", "a": "The picker accepts JPG, PNG and WebP images. Whatever you start with, the download is a JPEG, because the canvas is exported at the quality you set. That makes it a good fit for photos and a poor fit for images that need transparency."},
            {"q": "What if the compressed file is bigger than the original?", "a": "The tool detects that case and marks the result as larger rather than reporting a false saving. It tends to happen with already-compressed files, flat graphics or screenshots with sharp text. Raise the quality setting, set Resize to 100%, or keep the original."},
            {"q": "Does lowering quality also change the dimensions?", "a": "No. Dimensions are controlled only by the Resize slider; the quality slider changes how the remaining pixels are encoded. Both are applied together whenever you move either slider."},
            {"q": "Is there a file size limit?", "a": "There is no server-side limit because nothing is uploaded. Practical limits come from your browser's memory when decoding and drawing a very large image."}
        ],
        "related": ["image-resizer", "png-to-webp", "jpg-to-png", "image-cropper"]
    },
    {
        "slug": "image-resizer",
        "name": "Image Resizer",
        "cat": "image",
        "popular": False,
        "icon": "Ir",
        "title": "Image Resizer — Set Exact Pixel Dimensions | CalcHub",
        "desc": "Resize an image to specific pixel dimensions with an optional aspect-ratio lock. Preview the result and download a PNG, processed in your browser.",
        "h1": "Image Resizer",
        "lede": "Some places ask for an image at an exact size — a 1200 by 630 preview card, or 600 pixels wide for a listing. Enter the numbers here and the image is redrawn at those dimensions.",
        "howto": [
            "Choose or drop an image. The width and height fields fill with its current pixel size.",
            "Leave Lock aspect ratio on to have the other dimension calculated automatically when you change one.",
            "Turn the lock off if you need both dimensions set independently — the image will stretch to fit.",
            "Click Apply resize, check the info line and preview, then Download PNG."
        ],
        "examples": [
            "A 4000 x 3000 photo with the lock on: set Width to 1200 and Height becomes 900 automatically.",
            "A 1000 x 1000 avatar needed at 256 x 256: type 256 in either field with the lock on.",
            "A banner that must be exactly 800 x 200: turn the lock off and enter both values."
        ],
        "understanding": [
            "The number fields are pixels, not centimetres or percentages. With the aspect-ratio lock on, changing one dimension recomputes the other from the image's original width-to-height ratio, so the picture keeps its proportions. With the lock off the two values are independent, and the image is stretched or squeezed to fit.",
            "The info line shows the original dimensions, the new dimensions and the size of the resulting PNG. The output is always PNG, which is why a photograph that started as a small JPEG can end up as a larger file even at smaller dimensions."
        ],
        "limitations": [
            "Enlarging an image cannot add detail. Scaling a small picture up will look soft or pixelated.",
            "The output is always PNG. If you need JPEG or WebP, use one of the format converters after resizing.",
            "Width and height accept values from 1 to 8000 pixels, and very large canvases depend on your browser's memory.",
            "Transparency is preserved in the PNG output, but EXIF metadata is not carried over.",
            "The lock uses the original file's ratio. If you set both fields with the lock off and then switch it back on, the next edit recalculates from the original proportions."
        ],
        "privacy": "The image is drawn into a canvas on your device and is never uploaded.",
        "faq": [
            {"q": "Does the tool keep the aspect ratio?", "a": "By default, yes — the lock is on when the page loads, so editing one field updates the other. Untick it to set both dimensions freely, which will distort the image if the new ratio differs from the original."},
            {"q": "Why is my resized PNG bigger than the original JPG?", "a": "PNG stores pixels losslessly and is inefficient for continuous-tone photographs, whereas JPEG compresses them aggressively. A smaller image can therefore have a larger file size after conversion."},
            {"q": "Can I resize several images at once?", "a": "No. One image is processed at a time, with a separate download for each."}
        ],
        "related": ["image-compressor", "image-cropper", "jpg-to-png", "png-to-webp"]
    },
    {
        "slug": "jpg-to-png",
        "name": "JPG to PNG Converter",
        "cat": "image",
        "popular": False,
        "icon": "Jp",
        "title": "JPG to PNG Converter — Change the Format, Not the Detail | CalcHub",
        "desc": "Turn a JPEG into a PNG in your browser. See why changing the file format does not restore detail lost to JPEG compression.",
        "h1": "JPG to PNG Converter",
        "lede": "A JPEG is already compressed. Putting those same pixels into a PNG changes the container, not the image — useful when a workflow insists on PNG, but it will not bring back detail the JPEG discarded.",
        "howto": [
            "Choose a JPEG file or drop it onto the panel. The file picker is limited to JPEG images.",
            "Conversion runs automatically at the image's original pixel dimensions.",
            "Check the info line for the dimensions and the output size.",
            "Click Download PNG to save the result."
        ],
        "examples": [
            "A 1600 x 1200 JPEG becomes a 1600 x 1200 PNG — same pixels, different format, usually a larger file.",
            "A product photo needed as PNG for a design tool that rejects JPEG uploads.",
            "A screenshot saved by mistake as JPEG: converting keeps the existing blur and artefacts exactly as they are."
        ],
        "understanding": [
            "The tool decodes the JPEG, draws it onto a canvas and exports that canvas as PNG. Width and height are unchanged. What changes is how the pixel data is stored: JPEG uses lossy compression tuned for photographs, while PNG stores pixels losslessly, which is why photographs usually get bigger.",
            "PNG's real advantages are lossless storage and an alpha channel for transparency. Converting from JPEG gives you the first but not the second automatically, because the source had no transparency to preserve."
        ],
        "limitations": [
            "Converting to PNG cannot restore detail, sharpness or colour information already lost to JPEG compression. It does not improve image quality.",
            "Photographs usually become larger files, sometimes several times larger, because PNG is not efficient for continuous-tone images.",
            "The file picker accepts JPEG images only, and the output is always PNG. There is no quality setting on this page.",
            "EXIF metadata such as camera settings is not preserved through the canvas redraw.",
            "If your goal is a smaller file rather than a different format, use the Image Compressor instead."
        ],
        "privacy": "Conversion runs on your device; the image is never uploaded.",
        "faq": [
            {"q": "Will converting to PNG improve my photo?", "a": "No. The pixels are exactly the ones the JPEG contained, including any compression artefacts. PNG simply stops further loss from happening when you save the file again."},
            {"q": "Why did the file get bigger?", "a": "JPEG discards information that PNG keeps, so a photograph stored losslessly needs more bytes. Screenshots and flat graphics are the cases where PNG can be smaller."},
            {"q": "Does it add a transparent background?", "a": "No. JPEG has no transparency, and this tool does not remove or invent a background. It only changes the file format."}
        ],
        "related": ["png-to-webp", "image-compressor", "image-resizer", "favicon-generator"]
    },
    {
        "slug": "png-to-webp",
        "name": "PNG to WebP Converter",
        "cat": "image",
        "popular": False,
        "icon": "Pw",
        "title": "PNG to WebP Converter — Encode Web Images in Your Browser | CalcHub",
        "desc": "Convert PNG, JPEG or WebP images to WebP locally. Learn when WebP helps, where compatibility matters and why the size saving varies.",
        "h1": "PNG to WebP Converter",
        "lede": "WebP was designed to store web images in fewer bytes than PNG or JPEG. This converter re-encodes an image into WebP and shows the resulting size before you download it.",
        "howto": [
            "Choose or drop an image. The picker accepts PNG, JPEG and WebP files.",
            "Conversion runs automatically at the image's original dimensions.",
            "Check the info line for the dimensions and output size.",
            "Click Download WebP."
        ],
        "examples": [
            "A large PNG hero graphic with flat colours is often substantially smaller as WebP.",
            "A photograph already stored as a high-quality JPEG may see only a modest change.",
            "A PNG screenshot with fine text: check the result carefully, because a lossy WebP encode can soften sharp edges."
        ],
        "understanding": [
            "The tool decodes the source, draws it onto a canvas and asks the browser to encode that canvas as WebP at a fixed quality setting of 0.92. Dimensions stay the same; any size difference comes entirely from the new encoding.",
            "WebP supports both lossy and lossless compression and generally packs photographic detail into fewer bytes than JPEG or PNG. How much you save depends on the image: flat graphics and large photos tend to benefit most, while already-compressed files and images with fine text may not."
        ],
        "limitations": [
            "There is no fixed saving percentage. Some files shrink a lot, some barely change, and a lossy re-encode can introduce artefacts around sharp text or line art.",
            "The quality level is fixed at 0.92 on this page and cannot be adjusted here.",
            "WebP is widely supported in current browsers, but older software, some image editors and certain upload forms may not accept it. Keep the original until you have confirmed your target accepts the file.",
            "If a browser cannot encode WebP, the canvas export may fall back to PNG while keeping a .webp filename. Check the file type if it will not open.",
            "EXIF metadata is not preserved, and the tool handles one image at a time.",
            "Despite the name, the picker also accepts JPEG and WebP files. The output is always WebP."
        ],
        "privacy": "The image is encoded on your device and is never uploaded.",
        "faq": [
            {"q": "How much smaller will my file be?", "a": "It depends on the image, so we do not promise a percentage. Flat-colour graphics and large photos usually benefit most; a file that is already efficiently compressed, or a screenshot with fine text, may change very little or lose a little sharpness."},
            {"q": "Where might WebP not work?", "a": "Current browsers handle WebP well. Problems are more likely with older desktop software, some content management upload forms and legacy image editors. If in doubt, keep a PNG or JPEG copy as well."},
            {"q": "Can I adjust the quality?", "a": "Not on this page — the encode uses a fixed 0.92 quality. If you need a quality slider, use the Image Compressor, which exports JPEG."}
        ],
        "related": ["jpg-to-png", "image-compressor", "image-resizer", "favicon-generator"]
    },
    {
        "slug": "image-cropper",
        "name": "Image Cropper",
        "cat": "image",
        "popular": False,
        "icon": "Cr",
        "title": "Image Cropper — Centre Crop to Common Aspect Ratios | CalcHub",
        "desc": "Crop an image to square, 4:3, 3:2, 16:9 or 9:16 with a centred selection. Preview the frame and download the cropped PNG.",
        "h1": "Image Cropper",
        "lede": "A profile picture needs a square; a presentation slide needs 16:9. Choose a ratio here and the tool takes the largest centred rectangle that fits, so what you lose comes evenly off the edges.",
        "howto": [
            "Choose or drop an image.",
            "Pick an aspect ratio from the dropdown, or leave Free (original) to keep the whole image.",
            "Check the preview, which shows exactly what will be exported.",
            "Click Download cropped PNG."
        ],
        "examples": [
            "A 4000 x 3000 landscape photo in 1:1 Square becomes a 3000 x 3000 centre crop, trimming 500 pixels from each side.",
            "A portrait photo in 9:16 keeps the full height and trims the sides to match a story format.",
            "A 16:9 banner crop from a 3:2 photo removes a strip from the top and bottom."
        ],
        "understanding": [
            "For a fixed ratio, the tool computes the largest rectangle of that shape that fits inside the image and centres it. If the calculated height would exceed the image height, it uses the full height and narrows the width instead. The selection is always centred — there is no drag handle to move it.",
            "The preview shows the cropped PNG before download. Cropping removes the pixels outside the frame; it does not resize or rescale the content that remains."
        ],
        "limitations": [
            "The crop area is fixed at the centre. You cannot drag it, so an off-centre subject may be clipped. Reposition the image in another editor first if the framing matters.",
            "Cropping discards the outside area permanently in the downloaded file. Keep your original.",
            "Output is always PNG, and EXIF metadata is not preserved.",
            "Free (original) keeps the whole image at its original dimensions, which is effectively a conversion to PNG rather than a crop.",
            "Only one image and one preset ratio are handled at a time; there is no custom ratio field."
        ],
        "privacy": "The image is drawn into a canvas on your device and never uploaded.",
        "faq": [
            {"q": "Can I choose which part of the image to keep?", "a": "Not in this tool. The selection is centred automatically for the ratio you pick. To control the framing, crop or reposition the image elsewhere first, then use Free (original) here."},
            {"q": "Does cropping resize the image?", "a": "No. It removes pixels outside the chosen frame and leaves the remaining pixels at their original scale. Use the Image Resizer if you also need different dimensions."},
            {"q": "What formats can I open and download?", "a": "The picker accepts common image files. The download is always a PNG, regardless of what you started with."}
        ],
        "related": ["image-resizer", "image-compressor", "jpg-to-png", "png-to-webp"]
    },
    {
        "slug": "favicon-generator",
        "name": "Favicon Generator",
        "cat": "image",
        "popular": False,
        "icon": "Fg",
        "title": "Favicon Generator — Build a PNG Site Icon | CalcHub",
        "desc": "Make a favicon from a single letter or an uploaded image, choose a size and colours, then download a PNG. See where favicons appear and what sizes mean.",
        "h1": "Favicon Generator",
        "lede": "A favicon is the small mark beside a page title in a browser tab, and the icon saved with a bookmark. This tool builds one from a letter or an image at a standard square size.",
        "howto": [
            "Type a character in Letter or emoji, or drop an image onto the panel to use that instead.",
            "Pick Background color and Foreground color for the letter version.",
            "Choose a Size: 32, 48, 64 or 128 pixels square.",
            "Click Render favicon, check the preview, then Download PNG."
        ],
        "examples": [
            "A single 'C' in white on a blue 32 x 32 tile for a site's browser tab.",
            "A 128 x 128 version for a home-screen shortcut, where a larger icon stays sharp.",
            "Dropping a logo: it is scaled to fit with a margin and centred on the chosen background colour."
        ],
        "understanding": [
            "Favicons appear in browser tabs, bookmark lists, history and sometimes on mobile home-screen shortcuts. Browsers request a small square icon and may scale it, which is why a simple, high-contrast mark reads better than detailed artwork.",
            "The size selector sets the exact pixel dimensions of the square PNG. In letter mode the first character is drawn large and centred on the background using the foreground colour. In image mode the uploaded picture is scaled to about 80% of the tile and centred, with the background colour filling the rest."
        ],
        "limitations": [
            "This tool exports PNG only. It does not create a multi-size .ico file; if your site needs one, generate it separately from the PNG.",
            "Letter mode uses only the first character and draws it uppercase. The field allows two characters, but the second is ignored, and a multi-character emoji may not render as a complete symbol.",
            "In image mode the foreground colour has no effect — it applies to the letter rendering only.",
            "An uploaded image is fitted into the square rather than cropped to a custom shape, so wide or tall artwork will have visible background around it.",
            "Each download produces one PNG at one size. Sites wanting several sizes can generate and save each one separately."
        ],
        "privacy": "The icon is drawn on a canvas in your browser; no image or text is uploaded.",
        "faq": [
            {"q": "Do you generate .ico files?", "a": "No. The output is a single PNG at the size you choose, which modern browsers accept as a favicon. If you need a traditional .ico containing several sizes, convert the PNG with a dedicated icon tool."},
            {"q": "Which size should I choose?", "a": "32 x 32 is a common size for a browser tab. 64 or 128 is useful where the icon is shown larger, such as a shortcut or high-density display. Browsers can scale a larger icon down, so generating the biggest you need and letting them scale is a reasonable approach."},
            {"q": "Does the source image need to be square?", "a": "No. Non-square artwork is scaled down proportionally and centred, with the background colour filling the remaining space. A square source gives the most predictable result."}
        ],
        "related": ["image-resizer", "image-compressor", "png-to-webp", "jpg-to-png"]
    },
]
