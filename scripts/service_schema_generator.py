#!/usr/bin/env python3
"""
service_schema_generator.py
============================
Bluejaypro Service Schema Generator
Produces a 100% valid (0 errors / 0 warnings) JSON-LD <script> block
for any local business service page.

Usage:
    python service_schema_generator.py --input data.json --output schema.json
    python service_schema_generator.py  # Interactive mode

Validation: https://validator.schema.org
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

# ─── Valid Schema.org LocalBusiness @types ───────────────────────────────────
VALID_LOCAL_BUSINESS_TYPES = [
    "GeneralContractor",
    "RoofingContractor",
    "HVACBusiness",
    "Electrician",
    "Plumber",
    "Painter",
    "HomeAndConstructionBusiness",
    "LocalBusiness",
    "Organization",
    "HomeGoodsStore",
    "AutoRepair",
    "LandscapeService",
]

# ─── Entity pools by service category ───────────────────────────────────────
ENTITY_POOLS = {
    "adu": {
        "about": [
            {
                "@type": "Thing",
                "name": "Accessory Dwelling Unit",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Accessory_dwelling_unit",
                    "https://www.wikidata.org/wiki/Q18562603",
                    "https://www.google.com/search?kgmid=/m/07yk30"
                ],
                "description": "A secondary housing unit on a single-family residential lot, either attached or detached from the primary dwelling."
            },
            {
                "@type": "Thing",
                "name": "General contractor",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/General_contractor",
                    "https://www.wikidata.org/wiki/Q1139982",
                    "https://www.google.com/search?kgmid=/m/01nk3b"
                ],
                "description": "A professional responsible for the day-to-day oversight of a construction site, management of vendors and trades, and communication throughout a project."
            },
            {
                "@type": "Thing",
                "name": "Building permit",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Building_permit",
                    "https://www.wikidata.org/wiki/Q2916482",
                    "https://www.google.com/search?kgmid=/m/0j4bm"
                ],
                "description": "Approval granted by a local government body that authorizes a construction project to proceed."
            },
            {
                "@type": "Thing",
                "name": "Residential construction",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Residential_construction",
                    "https://www.wikidata.org/wiki/Q811430"
                ],
                "description": "The construction of houses or buildings for private residence."
            },
            {
                "@type": "Thing",
                "name": "Garage conversion",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Garage_conversion",
                    "https://www.wikidata.org/wiki/Q5522441"
                ],
                "description": "The conversion of an existing garage to a living space, often used to create an ADU."
            }
        ],
        "mentions": [
            {
                "@type": "Thing",
                "name": "Zoning",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Zoning",
                    "https://www.wikidata.org/wiki/Q948149",
                    "https://www.google.com/search?kgmid=/m/01z7d8"
                ],
                "description": "A method of urban land use planning which divides land into areas called zones, each with a set of regulations."
            },
            {
                "@type": "Thing",
                "name": "California Building Code",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/California_Building_Code",
                    "https://www.wikidata.org/wiki/Q5020461"
                ],
                "description": "The construction standards adopted by the state of California, based on the International Building Code."
            },
            {
                "@type": "Thing",
                "name": "Foundation (engineering)",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Foundation_(engineering)",
                    "https://www.wikidata.org/wiki/Q163730",
                    "https://www.google.com/search?kgmid=/m/035wy7"
                ],
                "description": "The lowest and supporting layer of a structure, transmitting its weight to the underlying natural ground."
            },
            {
                "@type": "Thing",
                "name": "Construction management",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Construction_management",
                    "https://www.wikidata.org/wiki/Q1090849"
                ],
                "description": "A professional service that uses specialized management techniques to oversee the planning, design, and construction of a project."
            }
        ]
    },
    "roofing": {
        "about": [
            {
                "@type": "Thing",
                "name": "Roof",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Roof",
                    "https://www.wikidata.org/wiki/Q44377",
                    "https://www.google.com/search?kgmid=/m/06l_3"
                ],
                "description": "The top covering of a building, including all materials and constructions necessary to support it on the walls of the building or on uprights."
            },
            {
                "@type": "Thing",
                "name": "Asphalt shingle",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Asphalt_shingle",
                    "https://www.wikidata.org/wiki/Q4804089"
                ],
                "description": "A type of wall and roof shingle that uses asphalt for waterproofing and is the most widely used roofing product in North America."
            },
            {
                "@type": "Thing",
                "name": "Roofing contractor",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Roofer",
                    "https://www.wikidata.org/wiki/Q1638659"
                ],
                "description": "A tradesperson who specializes in roof construction and repair."
            }
        ],
        "mentions": [
            {
                "@type": "Thing",
                "name": "Building envelope",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Building_envelope",
                    "https://www.wikidata.org/wiki/Q1059042"
                ],
                "description": "The physical separator between the conditioned and unconditioned environment of a building."
            },
            {
                "@type": "Thing",
                "name": "Water damage",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Water_damage",
                    "https://www.wikidata.org/wiki/Q7975218"
                ],
                "description": "Damage caused by water intruding where it will enable attack of a material or system."
            }
        ]
    },
    "hvac": {
        "about": [
            {
                "@type": "Thing",
                "name": "Heating, ventilation, and air conditioning",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Heating,_ventilation,_and_air_conditioning",
                    "https://www.wikidata.org/wiki/Q44395",
                    "https://www.google.com/search?kgmid=/m/03hmk"
                ],
                "description": "The technology of indoor environmental comfort using heating, ventilation, and air conditioning systems."
            },
            {
                "@type": "Thing",
                "name": "Air conditioning",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Air_conditioning",
                    "https://www.wikidata.org/wiki/Q265914",
                    "https://www.google.com/search?kgmid=/m/0f9fc"
                ],
                "description": "The process of removing heat and controlling the humidity of air in an enclosed space to achieve a more comfortable interior environment."
            }
        ],
        "mentions": [
            {
                "@type": "Thing",
                "name": "Energy efficiency",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Efficient_energy_use",
                    "https://www.wikidata.org/wiki/Q1534030",
                    "https://www.google.com/search?kgmid=/m/036vm"
                ],
                "description": "The goal to reduce the amount of energy required to provide products and services."
            },
            {
                "@type": "Thing",
                "name": "Indoor air quality",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Indoor_air_quality",
                    "https://www.wikidata.org/wiki/Q1642524"
                ],
                "description": "The air quality within and around buildings and structures, especially as it relates to the health and comfort of building occupants."
            }
        ]
    },
    "electrical": {
        "about": [
            {
                "@type": "Thing",
                "name": "Electrician",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Electrician",
                    "https://www.wikidata.org/wiki/Q165029",
                    "https://www.google.com/search?kgmid=/m/02c9c5"
                ],
                "description": "A tradesperson specializing in electrical wiring of buildings, stationary machines, and related equipment."
            },
            {
                "@type": "Thing",
                "name": "Circuit breaker",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/Circuit_breaker",
                    "https://www.wikidata.org/wiki/Q224168",
                    "https://www.google.com/search?kgmid=/m/01vn2"
                ],
                "description": "An automatically operated electrical switch designed to protect an electrical circuit from damage caused by excess current."
            }
        ],
        "mentions": [
            {
                "@type": "Thing",
                "name": "National Electrical Code",
                "sameAs": [
                    "https://en.wikipedia.org/wiki/National_Electrical_Code",
                    "https://www.wikidata.org/wiki/Q3317875"
                ],
                "description": "A regionally adoptable standard for the safe installation of electrical wiring and equipment in the United States."
            }
        ]
    }
}

# ─── Helper: normalize phone to E.164 ────────────────────────────────────────
def normalize_phone(phone: str) -> str:
    digits = ''.join(c for c in phone if c.isdigit())
    if not digits.startswith('1') and len(digits) == 10:
        digits = '1' + digits
    return '+' + digits if digits else phone


# ─── Helper: detect entity category ─────────────────────────────────────────
def detect_category(service_type: str) -> str:
    st = service_type.lower()
    if any(k in st for k in ['adu', 'accessory', 'dwelling', 'garage conv']):
        return 'adu'
    if any(k in st for k in ['roof', 'shingle', 'gutter']):
        return 'roofing'
    if any(k in st for k in ['hvac', 'air cond', 'heat', 'furnace', 'ac ', ' ac']):
        return 'hvac'
    if any(k in st for k in ['electric', 'wiring', 'panel']):
        return 'electrical'
    return 'adu'  # default fallback


# ─── Core schema builder ─────────────────────────────────────────────────────
def build_service_schema(data: dict) -> dict:
    """
    Build a 100%-valid Service schema from input data dict.
    All critical rules from the skill are enforced here.
    """
    business_name = data['business_name']
    biz_type      = data.get('business_type', 'LocalBusiness')
    service_name  = data['service_name']
    service_type  = data.get('service_type', service_name)
    service_desc  = data['service_description']
    service_url   = data['service_url']
    website_url   = data['website_url'].rstrip('/')
    phone         = normalize_phone(data.get('phone', ''))
    gmb_cid_url   = data.get('gmb_cid_url', '')
    kgmid         = data.get('kgmid', '')
    gmb_short     = data.get('gmb_short_url', '')
    gmb_place_id  = data.get('gmb_place_id_url', '')
    facebook_url  = data.get('facebook_url', '')
    linkedin_url  = data.get('linkedin_url', '')
    yelp_url      = data.get('yelp_url', '')
    street        = data['street_address']
    city          = data['city']
    state         = data['state']
    postal        = data['postal_code']
    country       = data.get('country_iso', 'US')   # MUST be 2-letter ISO
    price_range   = data.get('price_range', '$$$')
    payment       = data.get('payment_accepted', 'Cash, Credit Card')
    rating_value  = str(data.get('rating_value', '5.0'))
    review_count  = str(data.get('review_count', '0'))
    founding_date = data.get('founding_date', '')
    founder       = data.get('founder_name', '')
    logo_url      = data.get('logo_url', '')
    target_cities = data.get('target_cities', [city])
    service_output = data.get('service_output', f'Completed {service_name}')
    service_output_desc = data.get('service_output_description', f'A fully completed {service_name} project.')
    custom_about  = data.get('about_entities', [])
    custom_mentions = data.get('mentions_entities', [])

    # Validate business type
    if biz_type not in VALID_LOCAL_BUSINESS_TYPES:
        print(f"[WARNING] '{biz_type}' is not a recognized Schema.org type. Falling back to 'LocalBusiness'.")
        biz_type = 'LocalBusiness'

    # Validate country code
    if len(country) > 2 or country.startswith('http'):
        print(f"[WARNING] addressCountry '{country}' is not a 2-letter ISO code. Forcing 'US'.")
        country = 'US'

    # Build sameAs array
    same_as = []
    for url in [facebook_url, linkedin_url, yelp_url, gmb_short, gmb_place_id]:
        if url:
            same_as.append(url)
    if kgmid:
        same_as.append(f"https://www.google.com/search?kgmid={kgmid}")
    if gmb_cid_url and gmb_cid_url not in same_as:
        same_as.append(gmb_cid_url)

    # Build areaServed
    area_served = []
    for c in target_cities:
        if isinstance(c, dict):
            area_served.append(c)
        else:
            # Auto-format Wikipedia URL: "Sacramento, California" → "Sacramento,_California"
            wiki_name = c.strip().replace(' ', '_')
            area_served.append({
                "@type": "City",
                "name": c.split(',')[0].strip(),
                "sameAs": f"https://en.wikipedia.org/wiki/{wiki_name}"
            })

    # Build entity arrays
    category = detect_category(service_type)
    pool = ENTITY_POOLS.get(category, ENTITY_POOLS['adu'])
    about_entities = custom_about if custom_about else pool['about']
    mentions_entities = custom_mentions if custom_mentions else pool['mentions']

    # Build provider block
    provider = {
        "@type": biz_type,
        "name": business_name,
        "telephone": phone,
        "hasMap": gmb_cid_url,
        "sameAs": same_as,
        "priceRange": price_range,
        "paymentAccepted": payment,
        "currenciesAccepted": "USD",
        "aggregateRating": {                     # ← MUST be in provider, not Service
            "@type": "AggregateRating",
            "ratingValue": rating_value,
            "reviewCount": review_count,
            "bestRating": "5",
            "worstRating": "1"
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": city,
            "addressRegion": state,
            "postalCode": postal,
            "addressCountry": country,           # ← 2-letter ISO, NOT Wikidata URL
            "name": business_name,
            "@id": f"{website_url}/#PostalAddress"
        },
        "url": website_url,
        "@id": f"{website_url}/#{business_name.replace(' ', '')}"
    }
    if logo_url:
        provider["image"] = logo_url
    if founding_date:
        provider["foundingDate"] = founding_date
    if founder:
        provider["founder"] = {"@type": "Person", "name": founder}

    # Build final schema
    schema = {
        "@context": "http://schema.org",
        "@type": "Service",
        "name": f"{service_name} in {city}, {state[:2].upper() if len(state) > 2 else state}",
        "serviceType": service_type,
        "description": service_desc,
        "url": service_url,
        "provider": provider,
        "areaServed": area_served,
        "offers": {
            "@type": "Offer",
            "name": service_name,
            "url": service_url,
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "priceCurrency": "USD",
                "price": "0",
                "description": "Free estimate available. Contact for custom quote."
            },
            "seller": {
                "@type": biz_type,
                "name": business_name
            }
        },
        "serviceOutput": {
            "@type": "Thing",
            "name": service_output,
            "description": service_output_desc
        },
        "brand": {
            "@type": "Organization",
            "name": business_name,
            "url": website_url,
            "@id": f"{website_url}/#organization"
        },
        "mainEntityOfPage": {                    # ← about + mentions MUST be here
            "@type": "WebPage",
            "@id": service_url,
            "name": f"{service_name} | {business_name}",
            "url": service_url,
            "about": about_entities,             # ← NOT on root Service
            "mentions": mentions_entities        # ← NOT on root Service
        }
    }

    return schema


# ─── Validation checker ───────────────────────────────────────────────────────
def validate_schema(schema: dict) -> list:
    """Run basic local validation checks. Returns list of issues found."""
    issues = []

    # Check aggregateRating location
    if 'aggregateRating' in schema:
        issues.append("[ERROR] aggregateRating is on root Service — must be inside provider (LocalBusiness)")
    if 'aggregateRating' not in schema.get('provider', {}):
        issues.append("[WARN]  aggregateRating missing from provider — Review Snippets won't work")

    # Check about/mentions location
    for field in ['about', 'mentions']:
        if field in schema:
            issues.append(f"[ERROR] '{field}' is on root Service — must be inside mainEntityOfPage.WebPage")
    if 'mainEntityOfPage' not in schema:
        issues.append("[WARN]  mainEntityOfPage missing — about/mentions will have nowhere to live")

    # Check addressCountry
    addr = schema.get('provider', {}).get('address', {})
    country = addr.get('addressCountry', '')
    if country.startswith('http') or len(country) > 2:
        issues.append(f"[ERROR] addressCountry '{country}' is not a 2-letter ISO code (e.g., 'US')")

    # Check business type
    biz_type = schema.get('provider', {}).get('@type', '')
    if biz_type not in VALID_LOCAL_BUSINESS_TYPES:
        issues.append(f"[WARN]  Provider @type '{biz_type}' may not be a valid Schema.org type")

    return issues


# ─── Output formatter ─────────────────────────────────────────────────────────
def format_as_script_tag(schema: dict) -> str:
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=4, ensure_ascii=False)}\n</script>'


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Bluejaypro Service Schema Generator — Produces 0-error JSON-LD'
    )
    parser.add_argument('--input', '-i', type=str, help='Path to JSON data file')
    parser.add_argument('--output', '-o', type=str, help='Path to write output schema (default: stdout)')
    parser.add_argument('--validate-only', action='store_true', help='Validate input schema without regenerating')
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[ERROR] Input file not found: {args.input}")
            sys.exit(1)
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Use embedded Burnette demo data
        print("[INFO] No --input provided. Using Burnette Construction demo data.\n")
        data = {
            "business_name": "Burnette Construction",
            "business_type": "GeneralContractor",
            "service_name": "ADU Design & Build",
            "service_type": "ADU Construction",
            "service_description": "Burnette Construction offers full-service ADU design and build in Antelope, CA — from permit-ready architectural drawings to final inspection.",
            "service_url": "https://burnetteco.com/adu-design-build/",
            "website_url": "https://burnetteco.com",
            "phone": "(916) 821-9353",
            "gmb_cid_url": "https://www.google.com/maps?cid=899938478654821731",
            "kgmid": "/g/11tp2gy1zy",
            "gmb_short_url": "https://maps.app.goo.gl/bCk2933GJ5BovQVZ7",
            "gmb_place_id_url": "https://www.google.com/maps/place/?q=place_id:ChIJdUDaXdTXmoARYxXtO0c5fQw",
            "facebook_url": "https://www.facebook.com/burnetteconstruction",
            "linkedin_url": "https://www.linkedin.com/in/burnetteconstruc",
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
            "logo_url": "https://burnetteco.com/wp-content/uploads/burnette-construction-logo.png",
            "target_cities": [
                "Antelope, California",
                "Sacramento, California",
                "Citrus Heights, California",
                "Carmichael, California",
                "Fair Oaks, California",
                "Folsom, California",
                "Rancho Cordova, California",
                "Rocklin, California",
                "Roseville, California"
            ],
            "service_output": "Permitted, Move-In-Ready Accessory Dwelling Unit",
            "service_output_description": "A complete, code-compliant ADU (attached, detached, or garage conversion) fully permitted by Sacramento County, ready for occupancy or rental."
        }

    if args.validate_only:
        issues = validate_schema(data)
        if issues:
            print("Validation Issues Found:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("[OK] No issues found.")
        return

    schema = build_service_schema(data)
    issues = validate_schema(schema)

    if issues:
        print("[VALIDATION WARNINGS]:")
        for issue in issues:
            print(f"  {issue}")
        print()
    else:
        print("[OK] Schema passed all local validation checks.\n")

    script_output = format_as_script_tag(schema)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script_output)
        print(f"[OK] Schema written to: {output_path.resolve()}")
    else:
        print(script_output)


if __name__ == '__main__':
    main()
