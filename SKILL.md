---
name: service-schema-generator
description: >-
  Generates a 100% valid (0 errors, 0 warnings) JSON-LD Service page schema
  for any local business. Uses the validated single-root Service pattern with
  WebPage mainEntityOfPage (containing about + mentions), and aggregateRating
  nested under LocalBusiness provider. Follows Google Rich Result criteria for
  Review Snippets. Use when the user asks to create or generate a service page
  schema, or provides a service page URL + business info.
---

# Service Schema Generator

This skill produces a **production-ready, Schema.org-valid JSON-LD `<script>` block** for a local business **service page** (e.g., `/adu-design-build/`, `/ac-repair/`, `/roof-replacement/`).

The schema is iteratively validated to produce **0 Errors / 0 Warnings** on `validator.schema.org`.

---

## Architecture: Validated Single-Root Pattern

The schema uses **one root `@type: Service`** object. All knowledge-graph entity enrichment (`about`, `mentions`) is nested inside `mainEntityOfPage` (a `WebPage`), not directly on `Service`. The `aggregateRating` lives inside `provider` (the `LocalBusiness`).

```
<script type="application/ld+json">
{
  "@context": "http://schema.org",
  "@type": "Service",
  "provider": {                       ← LocalBusiness block
    "aggregateRating": { … }          ← REQUIRED: nested here, NOT on Service
    "address": { "@type": "PostalAddress" }
    "sameAs": [ … ]
    "hasMap": "GMB CID Maps URL"
  },
  "mainEntityOfPage": {               ← WebPage block
    "@type": "WebPage",
    "about": [ … ],                   ← Primary entities (who/what this is about)
    "mentions": [ … ]                 ← Supporting topical entities
  },
  "areaServed": [ … ],               ← Array of City strings
  "offers": { … },                   ← Offer with priceSpecification
  "serviceOutput": { … },            ← The tangible result
  "brand": { … }                     ← Organization brand anchor
}
```

> [!IMPORTANT]
> **Why this structure?**
> `Service` does NOT support `about` or `mentions` as direct properties — placing them there causes Schema.org validator warnings. Wrapping them inside `WebPage.mainEntityOfPage` is the only valid pattern.
> `aggregateRating` is NOT eligible for Review Snippets when placed on `Service` — it MUST be on `LocalBusiness` or `Product`.

---

## Required Inputs

Collect these before generating. Ask the user if any are missing.

| Field | Example |
|---|---|
| Business Name | Burnette Construction |
| Street Address | 8100 Otium Way |
| City / State / Zip | Antelope, CA 95843 |
| Phone (E.164) | +19168219353 |
| Website URL | https://burnetteco.com |
| **Service Page URL** | https://burnetteco.com/adu-design-build/ |
| **Service Name** | ADU Design & Build |
| **Service Type / Category** | ADU Construction |
| **Service Description (1–2 sentences)** | Scraped or user-provided |
| GMB `hasMap` URL (CID) | https://www.google.com/maps?cid=... |
| GMB `kgmid` | /g/11tp2gy1zy |
| GMB Business Profile ID | 11638949139430961433 |
| GMB Short URL | https://maps.app.goo.gl/bCk2933GJ5BovQVZ7 |
| GMB Place ID URL | https://www.google.com/maps/place/?q=place_id:... |
| Knowledge Panel URL | https://www.google.com/search?kgmid=... |
| Facebook URL | https://www.facebook.com/... |
| LinkedIn URL | https://www.linkedin.com/in/... |
| Instagram / Twitter | (if available) |
| Yelp URL | (if available) |
| **Aggregate Rating** | ratingValue: 4.9, reviewCount: 87 |
| Founding Year | 2021 |
| Founder / Owner Name | Christian Perry |
| **Accepted Payment Methods** | Cash, Credit Card, Visa/Master Card, PayPal |
| Price Range | $$$ |
| **Target Service Cities** | Antelope CA, Sacramento CA, Roseville CA |
| Country ISO Code | US |
| Wikidata Country URL | https://www.wikidata.org/wiki/Q30 |
| Business Category (`@type`) | GeneralContractor |

### Valid `@type` values for `LocalBusiness`:
| Valid | Notes |
|---|---|
| `GeneralContractor` | ✅ |
| `RoofingContractor` | ✅ |
| `HVACBusiness` | ✅ |
| `Electrician` | ✅ |
| `Plumber` | ✅ |
| `HomeAndConstructionBusiness` | ✅ |
| `LocalBusiness` | ✅ Fallback |
| `HVACContractor` | ❌ Use `HVACBusiness` |
| `ElectricalContractor` | ❌ Use `Electrician` |

---

## Critical Schema Rules (Learned from Validation)

| Rule | Correct | Wrong |
|---|---|---|
| `addressCountry` | `"US"` (ISO 2-letter) | `"https://www.wikidata.org/wiki/Q30"` ❌ |
| `aggregateRating` location | Inside `provider` (LocalBusiness) | Directly on `Service` ❌ |
| `about` / `mentions` location | Inside `mainEntityOfPage.WebPage` | Directly on `Service` ❌ |
| Entity `sameAs` format | Array of strings | Single string ❌ |
| `priceRange` | Inside `provider` | On root `Service` ❌ |
| `@context` | `"http://schema.org"` | `"https://schema.org"` (either works, but be consistent) |

---

## Entity Enrichment Pattern

Each entity in `about[]` and `mentions[]` should follow the **Triple Authority Link** pattern:

```json
{
  "@type": "Thing",
  "name": "Accessory Dwelling Unit",
  "sameAs": [
    "https://en.wikipedia.org/wiki/Accessory_dwelling_unit",
    "https://www.wikidata.org/wiki/Q18562603",
    "https://www.google.com/search?kgmid=/m/07yk30"
  ],
  "description": "A secondary housing unit on a single-family residential lot."
}
```

**Authority sources (in priority order):**
1. `en.wikipedia.org/wiki/...` — English Wikipedia canonical URL
2. `www.wikidata.org/wiki/Q...` — Wikidata QID
3. `www.google.com/search?kgmid=/m/...` or `/g/...` — Google Knowledge Graph ID

---

## areaServed Format

Use an array of strings (city + state) for simplicity. For richer markup, use `City` objects:

```json
"areaServed": [
  { "@type": "City", "name": "Antelope", "sameAs": "https://en.wikipedia.org/wiki/Antelope,_California" },
  { "@type": "City", "name": "Sacramento", "sameAs": "https://en.wikipedia.org/wiki/Sacramento,_California" }
]
```

Minimum: include the primary business city plus all target service radius cities.

---

## offers Format

```json
"offers": {
  "@type": "Offer",
  "name": "[Service Name]",
  "url": "[Service Page URL]",
  "availability": "https://schema.org/InStock",
  "priceSpecification": {
    "@type": "PriceSpecification",
    "priceCurrency": "USD",
    "price": "0",
    "description": "Free estimate available. Contact for custom quote."
  },
  "seller": {
    "@type": "[LocalBusiness @type]",
    "name": "[Business Name]"
  }
}
```

---

## Full Output Template

After collecting data, generate this structure and populate every `[PLACEHOLDER]`:

```json
<script type="application/ld+json">
{
    "@context": "http://schema.org",
    "@type": "Service",
    "name": "[Service Name] in [Primary City], [State]",
    "serviceType": "[Service Type/Category]",
    "description": "[1-2 sentence service description]",
    "url": "[Service Page URL]",
    "provider": {
        "@type": "[LocalBusiness @type]",
        "name": "[Business Name]",
        "telephone": "[+E.164 Phone]",
        "hasMap": "[GMB CID URL]",
        "sameAs": [
            "[Facebook URL]",
            "[LinkedIn URL]",
            "[Yelp URL]",
            "[GMB Short URL]",
            "[Knowledge Panel URL]",
            "[GMB Place ID URL]",
            "https://www.google.com/search?kgmid=[kgmid]"
        ],
        "priceRange": "[$ / $$ / $$$ / $$$$]",
        "paymentAccepted": "[Cash, Credit Card, etc.]",
        "currenciesAccepted": "USD",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "[4.9]",
            "reviewCount": "[87]",
            "bestRating": "5",
            "worstRating": "1"
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "[Street Address]",
            "addressLocality": "[City]",
            "addressRegion": "[State full name]",
            "postalCode": "[ZIP]",
            "addressCountry": "[US]",
            "name": "[Business Name]",
            "@id": "[Website URL]/#PostalAddress"
        },
        "image": "[Logo or Photo URL]",
        "url": "[Website URL]",
        "foundingDate": "[YYYY-MM-DD]",
        "founder": {
            "@type": "Person",
            "name": "[Founder/Owner Name]"
        },
        "@id": "[Website URL]/#[BusinessShortId]"
    },
    "areaServed": [
        { "@type": "City", "name": "[City 1]", "sameAs": "https://en.wikipedia.org/wiki/[City_1]" },
        { "@type": "City", "name": "[City 2]", "sameAs": "https://en.wikipedia.org/wiki/[City_2]" }
    ],
    "offers": {
        "@type": "Offer",
        "name": "[Service Name]",
        "url": "[Service Page URL]",
        "availability": "https://schema.org/InStock",
        "priceSpecification": {
            "@type": "PriceSpecification",
            "priceCurrency": "USD",
            "price": "0",
            "description": "Free estimate available. Contact for custom quote."
        },
        "seller": {
            "@type": "[LocalBusiness @type]",
            "name": "[Business Name]"
        }
    },
    "serviceOutput": {
        "@type": "Thing",
        "name": "[Tangible Result of Service]",
        "description": "[What the customer ends up with]"
    },
    "brand": {
        "@type": "Organization",
        "name": "[Business Name]",
        "url": "[Website URL]",
        "@id": "[Website URL]/#organization"
    },
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "[Service Page URL]",
        "name": "[Service Name] | [Business Name]",
        "url": "[Service Page URL]",
        "about": [
            {
                "@type": "Thing",
                "name": "[Primary Entity Name]",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/[...]",
                    "https://www.wikidata.org/wiki/Q[...]",
                    "https://www.google.com/search?kgmid=/m/[...]"
                ],
                "description": "[Short encyclopedic description]"
            }
        ],
        "mentions": [
            {
                "@type": "Thing",
                "name": "[Supporting Entity Name]",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/[...]",
                    "https://www.wikidata.org/wiki/Q[...]"
                ],
                "description": "[Short encyclopedic description]"
            }
        ]
    }
}
</script>
```

---

## Execution Workflow

### Step 1 — Collect Data
- Ask user for all required inputs from the table above, OR
- If a service page URL is provided, scrape it with `read_url_content` to extract the service description and any FAQs.
- Use `search_web` to find the GMB CID URL if not provided (search business name + city on Google Maps).

### Step 2 — Resolve Entities
Identify 5–10 `about` entities (core topic entities) and 5–10 `mentions` entities (supporting/topical) based on the service category.

For each entity, resolve the Triple Authority Links:
- Search Wikipedia: `https://en.wikipedia.org/wiki/[EntityName]`
- Wikidata: search `https://www.wikidata.org/w/index.php?search=[EntityName]` for the QID
- Google KG: include only if kgmid is known

Common entity pools by category:

**ADU / Construction:**
- About: Accessory Dwelling Unit, General contractor, Building permit, Residential construction
- Mentions: California Building Code, ADU Ordinance, Foundation (engineering), Zoning laws, Construction management

**Roofing:**
- About: Roof, Roofing contractor, Asphalt shingle, Roof flashing
- Mentions: Building envelope, Storm damage, Roof ventilation, Insurance claim, Water damage

**HVAC:**
- About: HVAC, Air conditioning, Furnace, Heat pump
- Mentions: Energy efficiency, Indoor air quality, SEER rating, Refrigerant, Ductwork

**Electrical:**
- About: Electrician, Electrical wiring, Circuit breaker, Ground fault circuit interrupter
- Mentions: National Electrical Code, Load calculation, Panel upgrade, Arc-fault circuit interrupter

### Step 3 — Generate Schema
Fill the full output template with all collected data. Apply all Critical Schema Rules.

### Step 4 — Validate
After generating, check for the following:
- [ ] `addressCountry` is 2-letter ISO code (e.g., `"US"`)
- [ ] `aggregateRating` is inside `provider`, NOT on root `Service`
- [ ] `about` and `mentions` are inside `mainEntityOfPage.WebPage`
- [ ] `sameAs` is an array (even if only one URL)
- [ ] No Wikidata URLs used as `addressCountry` value
- [ ] `priceRange` inside `provider`
- [ ] At least 2 cities in `areaServed`

### Step 5 — Deliver
Present the schema as a code block inside `<script type="application/ld+json">` tags, ready to paste into WordPress (via BJP Schema Injector plugin or any theme/plugin).

---

## Output Location Reference

- **WordPress Plugin:** BJP Schema Injector — paste into Per-Page Metabox for the service page URL.
- **Manual:** Add via `wp_head` action or Elementor HTML widget.
- **Validation URL:** https://validator.schema.org or https://search.google.com/test/rich-results

---

## Reference: Burnette Construction — ADU Service Page (Validated Example)

**URL:** https://burnetteco.com/adu-design-build/  
**Business:** Burnette Construction, 8100 Otium Way, Antelope, CA 95843  
**Phone:** +19168219353  
**kgmid:** /g/11tp2gy1zy  
**GMB CID URL:** https://www.google.com/maps?cid=899938478654821731  

See `resources/burnette_adu_service_schema.json` for the fully validated output.
