# Checkout Flow & Shop Page Verification Checklist

## Status: COMPLETED (2026-02-12)
**Summary**: Full flow from shop to payment screen verified via browser exploration.

## 1. Shop Page Deep Dive (`/shop`)
- [ ] **Filters & Sorting**:
  - [ ] Are there categories (e.g., "Nut Butters", "Bars")?
  - [ ] Does sorting (Price, Date) work without page reload?
  - [ ] Is there a "Quick Add" button?
- [ ] **Product Cards**:
  - [ ] Check for visible ratings (Stars).
  - [ ] Check for "Sale" badges.
  - [ ] Verify image hover effects (secondary image?).

## 2. Product Detail Page (PDP)
- [ ] **URL Structure**: e.g., `/product/seeds-boost-bar`
- [ ] **Components**:
  - [ ] Title, Price, Discount %.
  - [ ] Variant Selector (e.g., "Pack of 3", "500g vs 1kg").
  - [ ] Quantity Counter.
  - [ ] "Add to Bag" vs "Buy Now" behavior.
  - [ ] Accordions/Tabs: Ingredients, Nutritional Info, How to Use.
- [ ] **Cross-Sells**: "You might also like" section?

## 3. Cart Interaction
- [ ] **Type**: Slide-out Drawer vs Full Page.
- [ ] **Elements**:
  - [ ] Item thumbnail, Title, Variant, Price.
  - [ ] Quantity adjuster.
  - [ ] Remove button.
  - [ ] Subtotal calculation.
  - [ ] "Free Shipping" progress bar (if applicable).
  - [ ] Order Notes field?

## 4. Checkout Flow (Hostinger Native)
- [ ] **Step 1: Information**
  - [ ] Email field (Check for "Login" prompt).
  - [ ] Shipping Address fields (Auto-complete?).
  - [ ] Phone number validation (Indu code +91?).
- [ ] **Step 2: Shipping**
  - [ ] Methods listed (e.g., "Standard Shipping", "Express").
  - [ ] Cost calculation verification.
- [ ] **Step 3: Payment**
  - [ ] Gateways visible:
    - [ ] Razorpay (Credit/Debit/UPI/Netbanking).
    - [ ] Cash on Delivery (COD)?
    - [ ] Other?
  - [ ] Order Summary review.

## 5. Post-Order (Hypothetical)
- [ ] Thank You Page structure.
- [ ] Email confirmation receipt.
