from PIL import Image, ImageDraw, ImageFont
import os

MEME_CARDS = [
    {"name": "Pepe the Frog", "image_url": "pepe.png", "color": "#4CAF50"},
    {"name": "Wojak", "image_url": "wojak.png", "color": "#F5F5DC"},
    {"name": "Troll Face", "image_url": "troll.png", "color": "#FFFFFF"},
    {"name": "Is This a Pigeon?", "image_url": "pigeon.png", "color": "#2196F3"},
    {"name": "Success Kid", "image_url": "success.png", "color": "#FFC107"},
    {"name": "Hide the Pain Harold", "image_url": "harold.png", "color": "#FF9800"},
    {"name": "Distracted Boyfriend", "image_url": "boyfriend.png", "color": "#E91E63"},
    {"name": "Mocking SpongeBob", "image_url": "spongebob.png", "color": "#FFEB3B"},
    {"name": "Woman Yelling at Cat", "image_url": "yellingcat.png", "color": "#9E9E9E"},
    {"name": "Grumpy Cat", "image_url": "grumpycat.png", "color": "#795548"},
    {"name": "Doge", "image_url": "doge.png", "color": "#FFD54F"},
    {"name": "Stonks Man", "image_url": "stonks.png", "color": "#00BCD4"},
    {"name": "Disaster Girl", "image_url": "disastergirl.png", "color": "#F44336"},
    {"name": "Nyan Cat", "image_url": "nyancat.png", "color": "#E040FB"},
    {"name": "Cyber Doge", "image_url": "cyberdoge.png", "color": "#00E5FF"},
    {"name": "Gigachad", "image_url": "gigachad.png", "color": "#607D8B"},
    {"name": "Illuminati Triangle", "image_url": "illuminati.png", "color": "#8BC34A"}
]

output_dir = "../frontend/public/cards"
os.makedirs(output_dir, exist_ok=True)

for card in MEME_CARDS:
    img = Image.new('RGB', (300, 420), color=card["color"])
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("Arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        
    text = card["name"]
    # Provide simple text bounding box to center it manually if needed
    # Using a simple text draw for MVP
    d.text((10, 200), text, fill=(0,0,0), font=font)
    
    img.save(os.path.join(output_dir, card["image_url"]))

print(f"Generated {len(MEME_CARDS)} images in {output_dir}")
