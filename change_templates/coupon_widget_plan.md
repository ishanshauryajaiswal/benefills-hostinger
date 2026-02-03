# Implementation Plan - Available Coupons Widget

## Goal
Implement a "View Available Coupons" feature on the checkout page of `benefills.com` to improve user conversion and experience.

## Technical Details
- **Platform**: Hostinger Website Builder.
- **Method**: JavaScript Injection via "Custom Code" (Integrations) settings.
- **Trigger**: A "View Coupons" link/button injected near the discount input field.
- **UI**: A modern, responsive modal showing coupon cards.

## Components

### 1. The Injector (JavaScript)
- A script that runs on the checkout page.
- Uses `MutationObserver` to detect when the `.discount-field` element is added to the DOM.
- Injects a "View Coupons" button below the input.

### 2. The Modal (HTML/CSS)
- **Design**: 
  - Dark mode support or theme-consistent colors.
  - Backdrop blur (glassmorphism).
  - Clean cards for each coupon.
- **Content**:
  - `FIRSTLOVE20`: 20% Off
  - `SAVE10`: 10% Off
  - `SAVE20`: 20% Off
  - *Criteria*: "Valid on all products" (placeholder).

### 3. Application Logic
- When a coupon is clicked:
  1. Set `document.getElementById('discountCode').value = code`.
  2. Trigger `input` and `change` events.
  3. Click the `Apply` button.
  4. (Optional) Show a success message or close the modal.

## Steps
1.  **Draft the Code**: Write the single-file HTML/CSS/JS block.
2.  **Verify UI**: I'll provide a mock or screenshot if possible, but since I can't "preview" on the actual site easily without the user, I'll make it robust.
3.  **Handoff**: Provide the code block to the user to paste into Hostinger settings.

## Mockup / CSS Styles
```css
/* Placeholder for premium styles */
.coupon-widget-trigger {
  color: #c4a163; /* Example gold/brand color */
  cursor: pointer;
  font-size: 0.85rem;
  margin-top: 8px;
  display: block;
  text-decoration: underline;
}
.coupon-modal {
  /* ... styles ... */
}
```
