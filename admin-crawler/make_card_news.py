from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_card(author, article_title, subtitle, body, output_path):
    # Create a blank image with white background
    base = Image.new('RGBA', (800, 1000), (255, 255, 255, 255))
    # Initialize drawing context
    draw = ImageDraw.Draw(base)

    # Load a font
    font_author = ImageFont.truetype("/Users/annapo/Downloads/Pumping-iOS-develop/Projects/Shared/DesignSystem/Resources/Font/Pretendard/Pretendard-Regular.otf", 24)
    font_article_title = ImageFont.truetype("/Users/annapo/Downloads/Pumping-iOS-develop/Projects/Shared/DesignSystem/Resources/Font/Pretendard/Pretendard-Bold.otf", 32)
    font_subtitle = ImageFont.truetype("/Users/annapo/Downloads/Pumping-iOS-develop/Projects/Shared/DesignSystem/Resources/Font/Pretendard/Pretendard-Bold.otf", 40)
    font_body = ImageFont.truetype("/Users/annapo/Downloads/Pumping-iOS-develop/Projects/Shared/DesignSystem/Resources/Font/Pretendard/Pretendard-Regular.otf", 28)

    # Define text position and wrapping
    margin = 50
    offset = 50

    # Author name
    for line in textwrap.wrap(author, width=40):
        draw.text((margin, offset), line, font=font_author, fill=(0, 0, 0, 255))
        offset += draw.textbbox((0, 0), line, font=font_author)[3] + 10

    # Article title
    offset += 20
    for line in textwrap.wrap(article_title, width=30):
        draw.text((margin, offset), line, font=font_article_title, fill=(0, 0, 0, 255))
        offset += draw.textbbox((0, 0), line, font=font_article_title)[3] + 10

    # Subtitle
    offset += 20
    for line in textwrap.wrap(subtitle, width=30):
        draw.text((margin, offset), line, font=font_subtitle, fill=(0, 0, 0, 255))
        offset += draw.textbbox((0, 0), line, font=font_subtitle)[3] + 40  # 간격 조정

    # Adjust body font size dynamically to fit within the card if text is too long
    max_height = 1000 - offset - 50  # available space for body text
    while True:
        # Wrap the body text to the card width
        body_lines = textwrap.wrap(body, width=40)
        body_height = sum([draw.textbbox((0, 0), line, font=font_body)[3] + 10 for line in body_lines])

        if body_height <= max_height or font_body.size <= 10:  # 최소 폰트 크기 제한 추가
            break
        # Reduce font size if the text exceeds the available space
        font_body = ImageFont.truetype("/Users/annapo/Downloads/Pumping-iOS-develop/Projects/Shared/DesignSystem/Resources/Font/Pretendard/Pretendard-Regular.otf", font_body.size - 2)

    # Draw the body text
    for line in body_lines:
        draw.text((margin, offset), line, font=font_body, fill=(0, 0, 0, 255))
        offset += draw.textbbox((0, 0), line, font=font_body)[3] + 10

    # Save the image
    base.save(output_path)

# Sample data
data = {
    "author": "DevPill",
    "article_title": "25년차 시니어 엔지니어가 말하는 '내가 18살로 돌아간다면 꼭 하고 싶은 10가지'",
    "subtitle": "멘토링과 네트워킹",
    "body_content": "경력 초기에 대중 앞 노출을 중증 어려워했던 것과 같은 이유로, 네트워킹과 다른 사람들의 멘토링에 의존하는 것도 도전이었습니다. 많은 행사에 참여하고 제 분야의 수많은 사람들을 만났지만, 특히 이러한 관계를 유지하는 면에서 훨씬 더 잘할 수 있었다고 생각합니다."
}

# Create card
create_card(data["author"], data["article_title"], data["subtitle"], data["body_content"], "card_output.png")