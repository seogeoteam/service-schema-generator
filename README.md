# service-schema-generator

> **Bluejaypro Antigravity Skill** — Generates a 100% valid (0 errors, 0 warnings) JSON-LD `Service` page schema for any local business.

[![Schema.org Valid](https://img.shields.io/badge/schema.org-valid-brightgreen)](https://validator.schema.org)
[![Google Rich Results](https://img.shields.io/badge/Google%20Rich%20Results-0%20errors-success)](https://search.google.com/test/rich-results)

---

## What It Does

Produces a production-ready `<script type="application/ld+json">` block for any **service page** (e.g., `/adu-design-build/`, `/roof-replacement/`, `/ac-repair/`), following the **validated single-root `Service` pattern**.

### Key Architecture Rules (Baked In)

| Rule | Correct Pattern |
|---|---|
| `aggregateRating` | Nested inside `provider` (LocalBusiness) → enables **Google Review Snippets** |
| `about` / `mentions` | Inside `mainEntityOfPage.WebPage` → **zero Schema.org validator warnings** |
| `addressCountry` | 2-letter ISO (`"US"`) — Wikidata URLs rejected automatically |
| `sameAs` | **Triple Authority Links**: Wikipedia + Wikidata QID + Google `kgmid` |
| `seller` in `offers` | Full NAP fields + `@id` reference → eliminates duplicate entity warnings |

---

## File Structure

```
service-schema-generator/
├── SKILL.md                          # Agent instructions (rules, inputs, workflow)
├── README.md                         # This file
├── scripts/
│   └── service_schema_generator.py   # Python generator (CLI + importable)
└── resources/
    ├── burnette_adu_service_schema.json  # Hand-crafted validated reference
    └── burnette_adu_output.json          # Script-generated output (verified)
```

---

## Usage

### As an Antigravity Agent Skill
The agent reads `SKILL.md` and follows the 5-step workflow:
1. Collect business data (NAP, GMB links, service details)
2. Resolve Triple Authority entities (Wikipedia + Wikidata + KGMID)
3. Generate schema from the validated template
4. Validate locally (address, aggregateRating placement, ISO country code)
5. Deliver `<script>` block ready for WordPress (BJP Schema Injector plugin)

### As a Python CLI

```powershell
# Demo mode (Burnette Construction ADU example)
python scripts/service_schema_generator.py

# From your own JSON data file
python scripts/service_schema_generator.py --input my_client.json --output schema.json
```

### Input JSON Format

```json
{
  "business_name": "Burnette Construction",
  "business_type": "GeneralContractor",
  "service_name": "ADU Design & Build",
  "service_type": "ADU Construction",
  "service_description": "Full-service ADU design and build in Antelope, CA.",
  "service_url": "https://burnetteco.com/adu-design-build/",
  "website_url": "https://burnetteco.com",
  "phone": "(916) 821-9353",
  "gmb_cid_url": "https://www.google.com/maps?cid=899938478654821731",
  "kgmid": "/g/11tp2gy1zy",
  "gmb_short_url": "https://maps.app.goo.gl/bCk2933GJ5BovQVZ7",
  "facebook_url": "https://www.facebook.com/burnetteconstructioninc/",
  "linkedin_url": "https://www.linkedin.com/in/burnetteconstruction",
  "street_address": "8100 Otium Way",
  "city": "Antelope",
  "state": "California",
  "postal_code": "95843",
  "country_iso": "US",
  "price_range": "$$$",
  "payment_accepted": "Cash, Credit Card, Visa/Master Card, PayPal",
  "rating_value": 4.9,
  "review_count": 87,
  "founding_date": "2021-12-03",
  "founder_name": "Christian Perry",
  "target_cities": ["Antelope, California", "Sacramento, California"],
  "service_output": "Permitted, Move-In-Ready ADU",
  "service_output_description": "A fully permitted ADU ready for occupancy."
}
```

---

## Valid `@type` Values for LocalBusiness

| Type | Use For |
|---|---|
| `GeneralContractor` | General construction, ADU, remodeling |
| `RoofingContractor` | Roofing services |
| `HVACBusiness` | HVAC, AC, heating |
| `Electrician` | Electrical services |
| `Plumber` | Plumbing services |
| `HomeAndConstructionBusiness` | Mixed construction |
| `LocalBusiness` | Fallback for any category |

---

## Entity Pools (Built-In)

The script auto-detects the service category and applies the appropriate entity pool:

- **ADU / Construction** — `Accessory Dwelling Unit`, `General contractor`, `Building permit`, `Zoning`, `California Building Code`
- **Roofing** — `Roof`, `Asphalt shingle`, `Building envelope`, `Water damage`
- **HVAC** — `Heating ventilation and air conditioning`, `Air conditioning`, `Energy efficiency`
- **Electrical** — `Electrician`, `Circuit breaker`, `National Electrical Code`

All entities include **Triple Authority Links** (Wikipedia → Wikidata QID → Google KGMID).

---

## Validation

Test your output at:
- **Schema.org validator:** https://validator.schema.org
- **Google Rich Results Test:** https://search.google.com/test/rich-results

Expected result: **0 errors / 0 warnings** (optional fields may show as informational).

---

## WordPress Deployment

Use the **BJP Schema Injector** plugin (from the Topical Entity Explorer Studio):
- Paste schema into the **Per-Page Metabox** for the specific service page URL
- Set hook to `<head>` (Google recommended)
- Save — no page refresh needed

---

## Built By

**Bluejaypro / Antigravity Agent Architecture**  
Validated against: `validator.schema.org`, Google Rich Results Test  
Reference client: Burnette Construction — `burnetteco.com`
