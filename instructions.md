# Hostinger Master Companion - Instructions & Runbook

## Executive Summary
Project bootstrap initiated. Platform identified as **Hostinger Website Builder** with native e-commerce. Initial documentation structure created.

## Current Setup
- **Domain**: benefills.com
- **Platform**: Hostinger Website Builder (AI Builder)
- **E-commerce**: Native Hostinger Store
- **Hosting**: Hostinger
- **Known Integrations**: 
  - Razorpay (Payments)
  - Shiprocket (Shipping)
  - Google Analytics (Planned)

## Store Capabilities & Limitations (Hostinger Builder)
- **Pros**: Easy drag-and-drop, integrated essential features, fast setup.
- **Cons**: Less flexible than WordPress/WooCommerce, no custom backend code (PHP), limited plugin ecosystem (integrations are mostly built-in or via code injection).
- **Customization**: Done via "Integrations" settings (Custom Code/Head) or UI settings.

### Hostinger Builder Operations Guide
#### 1. The Editor
- **Drag-and-Drop**: Elements (text, images, buttons) can be moved freely within the grid.
- **Global Styles**: Manage colors, typography, and button styles via the "Website Styles" panel (left-side toolbar).
- **Mobile Optimization**: Use the Mobile Editor view to rearrange elements specifically for phone screens without affecting the desktop layout.
- **Undo/Redo**: Use the toolbar at the top to revert mistakes. There is also a "Version History" to restore previous states.

#### 2. Store Management (E-commerce)
- **Product Catalog**: Accessible via "Online Store" > "Products". You can add physical products, manage descriptions, pricing, and variants (like monthly packs).
- **Inventory/Categories**: Create categories to group products (e.g., "Seeds", "Nut Butters").
- **Orders**: View and manage customer orders in the "Orders" tab. Do not update order statuses unless explicitly asked.

#### 3. Integrations
- **Payment Gateways**: Razorpay is already integrated. Settings are in Store settings > Payments.
- **Shipping**: Shiprocket is integrated. Manage zones and rates in Store settings > Shipping.
- **Marketing/Analytics**: Custom scripts (Google Analytics, Meta Pixel) can be added via "Settings" > "Integrations" using the "Custom Code" section.

## Operating Procedures
### ⚠️ CRITICAL NOTE: DO NOT PUBLISH CHANGES
**MOST IMPORTANT**: You must NOT publish any changes to the website by yourself. If you have made modifications in the editor, do not click the "Update Website" button. Instead, notify the user and they will manually review and publish the changes.

- **Read-Only**: Always explore changes in the editor without publishing first.
- **Publishing**: Only the user should click the "Update Website" button.

## Known Risks / TODOs
- [ ] Setup Google Analytics (Priority)
- [ ] Verify existing Razorpay/Shiprocket integration status.
- [ ] Optimize SEO settings in Builder.

## Reference Index
- [Hostinger Docs Index](docs/hostinger_docs_index.md)
- [Search Playbook](docs/search_playbook.md)
- [Site Snapshot](findings/site_snapshot.md)
- [Platform Identification](findings/platform_identification.md)
- [Operational Guide](docs/OPERATIONAL_GUIDE.md)

## Session Logs
### 2026-02-02 - Site Exploration & Documentation update
- Explored `benefills.com` structure and checkout flow.
- Researched Hostinger Website Builder operations (Editor, Store, Integrations).
- Created `docs/OPERATIONAL_GUIDE.md` with detailed instructions.
- Added **CRITICAL NOTE**: Do not publish changes by self; ask the user to do it manually.
- Populated `findings/site_snapshot.md` with current site details.
