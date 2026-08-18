from pathlib import Path
import textwrap

import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = PROJECT_ROOT / "docs" / "demo_assets"
SUBMISSION_DIR = (
    Path.home()
    / "OneDrive"
    / "Desktop"
    / "Coackroach DB"
    / "NHS_Capacity_Submission_Pack"
)

WIDTH = 1920
HEIGHT = 1080
FPS = 24


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT_TITLE = font(66, bold=True)
FONT_H2 = font(42, bold=True)
FONT_BODY = font(31)
FONT_SMALL = font(25)
FONT_MONO = font(27)


def wrap(text, width=68):
    lines = []
    for part in text.split("\n"):
        if not part.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(part, width=width))
    return lines


def draw_wrapped(draw, text, xy, fill, fnt, width=68, line_gap=10):
    x, y = xy
    for line in wrap(text, width):
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + line_gap
    return y


def rounded(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def paste_image_fit(base, path, box):
    if not path.exists():
        return
    img = Image.open(path).convert("RGB")
    x1, y1, x2, y2 = box
    target_w = x2 - x1
    target_h = y2 - y1
    img.thumbnail((target_w, target_h))
    px = x1 + (target_w - img.width) // 2
    py = y1 + (target_h - img.height) // 2
    base.paste(img, (px, py))


def base_slide(title, kicker="NHS Capacity Memory Agent"):
    img = Image.new("RGB", (WIDTH, HEIGHT), "#f7fafc")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, 96), fill="#123c69")
    draw.text((70, 29), kicker, fill="white", font=FONT_SMALL)
    draw.text((70, 138), title, fill="#10233f", font=FONT_TITLE)
    draw.line((70, 230, 1850, 230), fill="#d6e2ef", width=3)
    return img, draw


def slide_intro():
    img, draw = base_slide("NHS Capacity Memory Agent")
    body = (
        "A deployed decision-support assistant for bed pressure, A&E demand, "
        "short-term forecasting, and operational memory."
    )
    draw_wrapped(draw, body, (70, 280), "#1d3557", FONT_H2, width=55)

    labels = [
        ("CockroachDB", "Cloud SQL + vector memory"),
        ("AWS Bedrock", "LLM reasoning"),
        ("AWS Lambda", "public API runtime"),
        ("Vercel", "clean web interface"),
    ]
    x = 80
    y = 570
    for name, desc in labels:
        rounded(draw, (x, y, x + 410, y + 150), 26, "#ffffff", "#d6e2ef", 3)
        draw.text((x + 28, y + 30), name, fill="#0b6b4f", font=FONT_H2)
        draw.text((x + 28, y + 92), desc, fill="#4f647d", font=FONT_SMALL)
        x += 445
    return img


def slide_homepage():
    img, draw = base_slide("Live Web Interface")
    draw_wrapped(
        draw,
        "The deployed app lets users ask NHS capacity questions in plain English through a clean, focused interface.",
        (70, 270),
        "#1d3557",
        FONT_BODY,
        width=58,
    )
    rounded(draw, (70, 390, 1850, 980), 24, "#ffffff", "#d6e2ef", 3)
    paste_image_fit(img, ASSET_DIR / "01_homepage.png", (105, 425, 1815, 945))
    return img


def slide_question(title, question, answer, tag):
    img, draw = base_slide(title)
    rounded(draw, (80, 275, 1840, 405), 22, "#ffffff", "#bdd7ee", 3)
    draw.text((115, 305), "Question", fill="#4f647d", font=FONT_SMALL)
    draw_wrapped(draw, question, (115, 348), "#10233f", FONT_BODY, width=88)

    rounded(draw, (80, 460, 1840, 930), 22, "#ffffff", "#d6e2ef", 3)
    draw.text((115, 498), "Agent answer", fill="#4f647d", font=FONT_SMALL)
    draw_wrapped(draw, answer, (115, 550), "#10233f", FONT_BODY, width=92)

    rounded(draw, (1470, 150, 1840, 215), 22, "#e7f6ef", "#9bd8bd", 2)
    draw.text((1500, 166), tag, fill="#0b6b4f", font=FONT_SMALL)
    return img


def slide_architecture():
    img, draw = base_slide("System Architecture")
    steps = [
        ("User", "asks a capacity question"),
        ("FastAPI\nLambda", "receives the request"),
        ("CockroachDB", "returns NHS data\nand memory"),
        ("Bedrock", "generates the\ngrounded answer"),
        ("Memory", "stores the useful\ninteraction"),
    ]

    x = 70
    y = 335
    card_w = 315
    card_h = 210
    gap = 62
    for i, (name, desc) in enumerate(steps):
        rounded(draw, (x, y, x + card_w, y + card_h), 24, "#ffffff", "#b9cee5", 3)
        draw.multiline_text((x + 26, y + 30), name, fill="#123c69", font=FONT_H2, spacing=6)
        draw.multiline_text((x + 26, y + 126), desc, fill="#4f647d", font=FONT_SMALL, spacing=6)
        if i < len(steps) - 1:
            start_x = x + card_w + 12
            end_x = x + card_w + gap - 12
            mid_y = y + card_h // 2
            draw.line((start_x, mid_y, end_x, mid_y), fill="#0b6b4f", width=7)
            draw.polygon([(end_x, mid_y), (end_x - 18, mid_y - 13), (end_x - 18, mid_y + 13)], fill="#0b6b4f")
        x += card_w + gap

    draw_wrapped(
        draw,
        "The demo proves a full loop: retrieved context, AI reasoning, vector memory, forecast signal, and saved conversation history.",
        (120, 705),
        "#1d3557",
        FONT_BODY,
        width=86,
    )
    return img


def slide_closing():
    img, draw = base_slide("Deployed System Summary")
    draw_wrapped(
        draw,
        "NHS Capacity Memory Agent connects a Vercel interface, AWS Lambda API, AWS Bedrock reasoning, and CockroachDB memory/vector search.",
        (80, 300),
        "#10233f",
        FONT_H2,
        width=62,
    )
    draw_wrapped(
        draw,
        "This deployed demo turns NHS capacity data into grounded answers, short-term A and E forecasts, and remembered follow-up conversations.",
        (80, 560),
        "#1d3557",
        FONT_BODY,
        width=82,
    )
    draw.text((80, 860), "Built by", fill="#4f647d", font=FONT_SMALL)
    draw.text((80, 905), "Fatimo Adenike Adeniya | Adeyinka Adejumobi", fill="#10233f", font=FONT_BODY)
    return img


def save_video(slide_paths, video_path):
    frames = []
    seconds_per_slide = [13, 7, 25, 22, 22, 17, 8]
    for path, seconds in zip(slide_paths, seconds_per_slide):
        frame = imageio.imread(path)
        frames.extend([frame] * (seconds * FPS))
    imageio.mimsave(video_path, frames, fps=FPS, codec="libx264", quality=8)


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    slides_dir = ASSET_DIR / "demo_video_slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    slides = [
        slide_intro(),
        slide_homepage(),
        slide_question(
            "Regional Bed Pressure",
            "Which region has the highest bed occupancy?",
            "South West has the highest General and Acute bed occupancy in the current regional dataset. The answer is grounded in the regional beds table stored in CockroachDB.",
            "CockroachDB data retrieval",
        ),
        slide_question(
            "Three-Month A&E Forecast",
            "What is the likely A&E pressure trend over the next 3 months?",
            "The agent uses recent monthly A&E activity and a simple linear trend. It forecasts attendances, emergency admissions, and 12-hour waits, while stating that this is not an official NHS prediction.",
            "Forecasting tool",
        ),
        slide_question(
            "Operational Memory Recall",
            "What did I ask earlier about capacity pressure?",
            "The assistant recalls earlier questions because each useful interaction is saved to CockroachDB memory. Vector search helps find related previous questions, not just exact matches.",
            "Vector memory",
        ),
        slide_architecture(),
        slide_closing(),
    ]

    slide_paths = []
    for index, slide in enumerate(slides, start=1):
        path = slides_dir / f"demo_slide_{index:02d}.png"
        slide.save(path)
        slide_paths.append(path)

    video_path = ASSET_DIR / "nhs_capacity_memory_agent_demo_draft.mp4"
    save_video(slide_paths, video_path)

    copy_video_path = SUBMISSION_DIR / "nhs_capacity_memory_agent_demo_draft.mp4"
    copy_guide_path = SUBMISSION_DIR / "DEMO_VIDEO_SCRIPT.md"
    copy_video_path.write_bytes(video_path.read_bytes())

    guide = """# Demo Video Script

Target length: 90 seconds to 2 minutes.

## Demo Story

1. Show homepage.
2. Ask: Which region has the highest bed occupancy?
3. Ask: What is the likely A&E pressure trend over the next 3 months?
4. Ask: What did I ask earlier about capacity pressure?
5. Show that it remembers previous questions.
6. Briefly mention CockroachDB, Bedrock, vector memory, and AWS Lambda.

## Voiceover Script

Emergency care pressure is hard to understand quickly because bed occupancy, A&E demand, admissions, and long waits are usually spread across separate datasets. I built NHS Capacity Memory Agent to turn those signals into a question-answering assistant.

On the homepage, users can ask plain-English capacity questions. The app is deployed online, and the backend is also available through an AWS Lambda Function URL.

First, I ask: Which region has the highest bed occupancy? The agent retrieves regional bed pressure from CockroachDB and answers using the stored NHS data.

Next, I ask: What is the likely A&E pressure trend over the next 3 months? The agent uses recent A&E activity and a simple forecasting tool to produce a short-term trend signal. It also explains that this is not an official NHS prediction.

Finally, I ask: What did I ask earlier about capacity pressure? The assistant recalls previous questions because useful interactions are saved into CockroachDB memory. The project also includes vector memory, so similar questions can be retrieved semantically rather than only by exact text matching.

The architecture uses CockroachDB Cloud for NHS data, memory, and vector search; AWS Bedrock for answer generation; AWS Lambda for the API runtime; and Vercel for the frontend.

This is NHS Capacity Memory Agent: a deployed decision-support assistant for capacity pressure, A&E demand forecasting, and operational memory.

## Demo Links

- Frontend: https://nhs-healthcare-capacity-ai.vercel.app/
- Lambda API: https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/
- API health check: https://yul47sn53pnghl73lmiacl444u0jqoxt.lambda-url.us-east-1.on.aws/health
- GitHub: https://github.com/Nik-ui/nhs-healthcare-capacity-ai

## Files Created

- Silent draft video: `nhs_capacity_memory_agent_demo_draft.mp4`
- Slide images: `docs/demo_assets/demo_video_slides/`

Use the silent draft as a visual guide. For the final Devpost video, record the live app while following this script so judges see the system working.
"""
    copy_guide_path.write_text(guide, encoding="utf-8")

    print(f"Created video draft: {video_path}")
    print(f"Copied video draft to: {copy_video_path}")
    print(f"Created guide: {copy_guide_path}")
    print(f"Created slides in: {slides_dir}")


if __name__ == "__main__":
    main()
