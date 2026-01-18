#!/usr/bin/env python3
"""Generate Windows ICO file from NLS icon.

Creates a multi-resolution ICO file suitable for Windows Explorer file association.
Requires: pip install Pillow

For SVG support (optional): pip install svglib reportlab
"""

from pathlib import Path
import sys
import io

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# Try to import SVG support (optional)
HAS_SVG = False
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM

    HAS_SVG = True
except ImportError:
    pass


def svg_to_image(svg_path: Path, size: int) -> Image.Image:
    """Convert SVG to PIL Image at specified size."""
    if not HAS_SVG:
        raise RuntimeError("svglib/reportlab not available")

    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"Could not parse SVG: {svg_path}")

    # Scale to target size
    scale = size / max(drawing.width, drawing.height)
    drawing.width = size
    drawing.height = size
    drawing.scale(scale, scale)

    # Render to PNG bytes
    png_bytes = renderPM.drawToString(drawing, fmt="PNG")
    return Image.open(io.BytesIO(png_bytes))


def create_nls_icon(size: int) -> Image.Image:
    """Create NLS icon programmatically - copper 'NL' text."""
    # Create RGBA image with transparency
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # NLS copper color (#B87333)
    copper = (184, 115, 51, 255)

    # Calculate font size (roughly 60% of icon size for good visibility)
    font_size = int(size * 0.6)

    # Try to use Arial Bold, fallback to default
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            # Use default font and scale as best we can
            font = ImageFont.load_default()

    text = "NL"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]

    # Draw the text
    draw.text((x, y), text, fill=copper, font=font)

    return img


def generate_ico(
    output_ico: Path,
    source_svg: Path | None = None,
    sizes: list[int] | None = None,
) -> None:
    """Generate ICO file with multiple resolutions.

    Uses SVG if available and svglib is installed, otherwise creates icon programmatically.

    Args:
        output_ico: Path for output ICO file
        source_svg: Path to source SVG file (optional)
        sizes: List of icon sizes (default: [16, 24, 32, 48, 64, 128, 256])
    """
    if sizes is None:
        sizes = [16, 24, 32, 48, 64, 128, 256]

    icons = []
    use_svg = source_svg and source_svg.exists() and HAS_SVG

    for size in sizes:
        if use_svg:
            try:
                img = svg_to_image(source_svg, size)
            except Exception as e:
                print(f"Warning: SVG conversion failed ({e}), using programmatic icon")
                img = create_nls_icon(size)
        else:
            img = create_nls_icon(size)

        # Ensure RGBA mode for transparency
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        icons.append(img)

    # Save as ICO with all sizes
    # For ICO format, we save the largest image and specify all target sizes
    # Pillow will create the multi-resolution ICO from the largest image
    output_ico.parent.mkdir(parents=True, exist_ok=True)

    # Get the largest image (last in list since we iterate ascending)
    largest = icons[-1]

    # Save with explicit sizes list
    largest.save(
        str(output_ico),
        format="ICO",
        sizes=[(s, s) for s in sizes],
    )

    print(f"Created {output_ico} with sizes: {sizes}")


def main() -> None:
    """Generate NLS icon files."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    source_svg = project_root / "vscode-nls" / "images" / "file-icon.svg"
    output_ico = script_dir / "nls-file.ico"

    print(f"SVG support available: {HAS_SVG}")

    generate_ico(output_ico, source_svg)

    # Also copy to nlsc package for distribution
    nlsc_ico = project_root / "nlsc" / "resources" / "nls-file.ico"
    nlsc_ico.parent.mkdir(parents=True, exist_ok=True)
    generate_ico(nlsc_ico, source_svg)
    print(f"Also created {nlsc_ico}")


if __name__ == "__main__":
    main()
