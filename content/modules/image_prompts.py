class ImagePrompts:
    PREMIUM_DYNAMIC_POSTER = (
        "Create a high-resolution square (1:1) Instagram food poster of {product_description}. "
        "Capture the dish in a dynamic, explosion-like composition bursting toward the viewer. "
        "Present it with realistic, mouthwatering textures and vibrant colors. "
        "Use the Benefills brand palette: Teal (#2A9D8F), Warm Coral (#E76F51), and Cream (#F4F1DE) accents. "
        "Place it against a deep, rich backdrop (Teal or Navy) with dramatic professional studio lighting, rich depth of field, and high contrast. "
        "Emphasize the premium, luxurious, and visually impactful feel. "
        "Exclude any hands, people, text, logos, or distracting tableware."
    )

    TOP_DOWN_FLAT_LAY = (
        "Create top-down flat lay product photo for Instagram. Use the described product as the main object, centered. "
        "Product Description: {product_description}. "
        "Analyze the product type and automatically choose matching props/ingredients for an aesthetic flat lay around it "
        "(minimal, premium, on-brand) — e.g. scattered seeds, dried berries, honey drizzle. "
        "Preserve exact geometry, size, colors, label design, and all text on the product (no changes). "
        "Background: Clean Cream (#F4F1DE) or Soft Sage Green (#8AB17D) seamless paper. "
        "Lighting: Soft directional sunlight, crisp realistic shadow (Golden Hour). "
        "Ultra-realistic macro product photography, 100mm lens look, f/8, sharp focus, clean composition, no extra text, 8k."
    )

    COOKBOOK_STYLE = (
        "Input: {product_description}\n"
        "<instructions>\n"
        "Analysis: Extract key ingredients, cooking techniques, and cultural food elements\n"
        "Goal: A cookbook where ingredients and dishes emerge in delicious detail\n"
        "Rules:\n"
        "Base: A vintage cookbook with stained pages and fabric cover\n"
        "Scene: 3D Miniature kitchen or market scene with chef & ingredients\n"
        "Details: Detailed food textures, steam effects, cooking implements\n"
        "Lighting: Warm kitchen lighting with golden hour quality\n"
        "Output: Single 4:5 image with appetizing details\n"
        "</instructions>"
    )

    VARIATION_GRID = (
        "Generate a 6x6 grid of professional product photography for: {product_description}. "
        "Reference the mood: Warm, Inviting, Authentic. "
        "Each cell should showcase a completely different product variation in a unique studio setting with a distinct color palette "
        "(focusing on Teal, Coral, Cream, Sage). "
        "Maintain the same high-end commercial photography style throughout. "
        "Vary the lighting, backgrounds, props, and styling dramatically across all 36 images."
    )

    HIGH_KEY_EDITORIAL = (
        "High-key studio editorial product shot of {product_description}. "
        "Use pure white or soft cream (#F4F1DE) background with soft studio lighting. "
        "The product should fill about 80-85% of the frame, with a clean and sharp focus. "
        "Ensure no shadows, extra props, or distracting elements. Ideal for product catalog use."
    )

    AMAZON_CATALOG = (
        "Main Product Image for Amazon: {product_description}. "
        "Pure white background (RGB 255, 255, 255). "
        "Front view, crystal clear product-centric shot. "
        "No props, no distractions, no text. "
        "Soft studio lighting, sharp focus throughout. "
        "Product fills 85% of frame. Commercial e-commerce standard."
    )

    LIFESTYLE_CONTEXT = (
        "Lifestyle product photography of {product_description}. "
        "Setting: Natural, authentic environment (e.g., modern kitchen counter, sunny picnic table, or cozy living room). "
        "Lighting: Natural sunlight, golden hour, or bright morning light. "
        "Styling: Casual, organic, with subtle complementary props (fresh ingredients, scattered nuts/seeds). "
        "Color Palette: Warm neutrals, Cream, Teal accents. "
        "Focus: Product is clear hero, but context adds warmth and brand mood. "
        "Aesthetic: Fresh, healthy, wholesome, premium, empowering."
    )

    DEFAULT = PREMIUM_DYNAMIC_POSTER

    @classmethod
    def get_prompt(cls, style: str, product_description: str) -> str:
        """
        Returns a formatted prompt based on the style and product description.
        """
        style_map = {
            "poster": cls.PREMIUM_DYNAMIC_POSTER,
            "flatlay": cls.TOP_DOWN_FLAT_LAY,
            "cookbook": cls.COOKBOOK_STYLE,
            "grid": cls.VARIATION_GRID,
            "editorial": cls.HIGH_KEY_EDITORIAL,
            "amazon": cls.AMAZON_CATALOG,
            "lifestyle": cls.LIFESTYLE_CONTEXT
        }
        
        template = style_map.get(style.lower(), cls.DEFAULT)
        return template.format(product_description=product_description)
