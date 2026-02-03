# Plan to Migrate Benefills to Lovable

This document outlines the step-by-step plan to migrate the **Benefills** website from Hostinger Builder to **Lovable.dev**, leveraging AI generation for a rapid and high-quality transition.

## Phase 1: Preparation & Export (Status: Mostly Done)

I have already scraped your live site to generate the necessary data files.

### 1. Visual Assets (Images & Logos)
*   **Action**: Create a folder on your desktop named `benefills_assets`.
*   **Task**: "Save" or "Download" the following from your current live site:
    *   **Logo**: The main Benefills logo (PNG/SVG).
    *   **Hero Images**: The main banner images from the homepage.
    *   **Product Images**: (Optional) I have included image links in the CSV, but downloading high-res versions is always safer.
*   **Screenshots**: Take full-page screenshots of your Homepage, Shop Page, and Product Page. Lovable can "see" these designs and replicate the layout.

### 2. Product Data (CSV) - **DONE ✅**
*   **Status**: I have already scraped your site and created **`benefills/migration_assets/products.csv`** with all 6 active products.
*   **Action**: You just need to upload this file to Lovable.
*   **Note on Hostinger Export**: The Hostinger Panel **fails** to provide a Product Export feature. However, it **DOES** allow you to export **Orders** to CSV if you need your sales history (Go to Store > Orders > Export to CSV).

### 3. Copy & Text - **DONE ✅**
*   **Status**: I have extracted the "Why Benefills Works" and "Testimonials" text into **`benefills/migration_assets/brand_copy.md`**.
*   **Action**: Open this file and copy-paste the text when Lovable asks for content or just upload the file as context.

---

## Phase 2: The "Lovable" Migration Prompt

Lovable allows you to upload files for context. 
**Step 1**: Upload your `products.csv` and the `Screenshots` of your current site to the chat in Lovable.
**Step 2**: Copy and paste the following prompt. It is engineered to be specific about your brand, features, and the coupon logic.

### 📋 The Master Prompt

```markdown
Build a modern, premium e-commerce web app for "Benefills" - a functional food brand focused on snacks for Thyroid Health.

**Design Aesthetic:**
- Use the visual style referenced in the uploaded screenshots.
- **Primary Colors**: Use a harmonious palette of Deep Green (#2b5a41) and Purple (as seen in screenshots) to convey health and vitality.
- **Typography**: Clean, modern sans-serif fonts (like Inter or Outfit) for a medical-grade but friendly feel.
- **Layout**: Mobile-first, responsive, with plenty of whitespace.

**Core Features & Pages:**

1.  **Homepage**:
    - **Hero Section**: High-impact banner with the headline "Snacks with Benefits for Thyroid Health" and a Call to Action (CTA) "Shop Now".
    - **Trust Signals**: A section displaying "Why Benefills Works" using cards/icons for "Metabolism", "Energy", "Stress Relief".
    - **Featured Products**: A horizontal scroll or grid of top sellers.
    - **Testimonials**: A carousel of customer reviews ("Real people, Real results").

2.  **Shop Page & Product Details**:
    - Display products from the database (use the structure in the uploaded CSV).
    - **Filters**: Allow filtering by Category and sorting by Price.
    - **Product Page**: detailed view showing Ingredients (Selenium, Zinc, Ashwagandha) and Benefits clearly. Add an "Add to Cart" button that opens a side-drawer cart.

3.  **Smart Checkout & Coupon Widget**:
    - **Cart**: A slide-out drawer showing selected items and total.
    - **Checkout Page**: A clean, single-page checkout form.
    - **Coupon Feature (CRITICAL)**:
        - Near the "Discount Code" input field, add a clickable link: "View Available Coupons".
        - Clicking this opens a Modal/Popup showing a list of active coupons (e.g., FIRSTLOVE20 for 20% off, SAVE10 for 10% off).
        - Clicking "Apply" on a coupon in the modal should auto-fill the code into the input field and apply the discount.

**Technical Stack & Data**:
- Use **Supabase** for the backend to store `products`, `orders`, and `coupons`.
- Create a `coupons` table with columns: `code` (text), `discount_percent` (number), `description` (text).
- Seed the database with the products provided in the CSV.
- Use **Tailwind CSS** for styling and **Lucide React** for icons.

**Context**:
I have uploaded my current site design and product list. Please replicate the "purple & green" brand identity exactly but improve the UI to be more modern and "Lovable".
```

---

## Phase 3: Post-Generation Refinement

Once Lovable generates the V1:
1.  **Check the Database**: Go to the Supabase integration in Lovable and ensure the **Products** table is populated. If not, ask it to "Seed the products table with this data: [paste data]".
2.  **Test the Coupon Widget**: Click "View Available Coupons" in the checkout. If it doesn't work, reply to Lovable: *"The coupon modal isn't popping up. Please ensure the state is handled correctly in React and the Z-index is high enough."*
3.  **Connect Domain**: Once satisfied, use Lovable's export or deployment features (usually via GitHub + Netlify/Vercel) to go live.

### 4. Integrations (Razorpay & Shiprocket)
*   **Note**: Lovable will build the *UI* for checkout, but the actual payment processing (Razorpay) and shipping logic (Shiprocket) requires API keys.
*   **Action**: After the site is built, you will need to ask Lovable: *"How do I connect my Razorpay API keys for the checkout?"* or manually add them to the exported code environment variables.
