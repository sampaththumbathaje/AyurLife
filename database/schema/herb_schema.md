# Herb Schema – AyurLife

## Collection Name
`herbs`

---

## Description
The `herbs` collection stores structured Ayurvedic knowledge about individual medicinal herbs.  
It functions as a **central knowledge repository** for the AyurLife system and supports:

- Herbs exploration and browsing UI
- Dosha-based filtering (Pacify / Aggravate / Tridosha)
- Ayurvedic research using Rasapanchaka
- Explainable chatbot responses
- Remedy composition through herb references

The schema is designed based on **classical Ayurvedic principles** while remaining **frontend- and backend-friendly**.

---

## Fields Overview

---

## 1. `_id`
- **Type:** ObjectId  
- **Description:** Auto-generated unique identifier created by MongoDB.

---

## 2. `herb_id`
- **Type:** String  
- **Description:** Application-level unique identifier for the herb.  
- **Example:** `H001`  
- **Usage:** Used for linking herbs with remedies and chatbot explanations.

---

## 3. `name`
- **Type:** String  
- **Description:** Common Ayurvedic name of the herb.  
- **Example:** `Tulsi`

---

## 4. `botanical_name`
- **Type:** String  
- **Description:** Scientific (botanical) name of the herb.  
- **Example:** `Ocimum sanctum`

---

## 5. `link`
- **Type:** String (URL)  
- **Description:** External authoritative reference or research source for the herb.  
- **Example:**  
  `https://www.amidhaayurveda.com/p/tulsi.html`

---

## 6. `preview`
- **Type:** String  
- **Description:** Short descriptive summary used in Herbs UI cards and previews.  
- **Example:**  
  `"Tulsi is known as the Queen of Herbs in Ayurveda and supports immunity."`

---

## Dosha Interaction

### 7. `dosha_effect`
- **Type:** Object  
- **Description:** Describes how the herb affects the three doshas.  
- **Purpose:** Used directly for UI filters, Prakriti-based suggestions, and chatbot reasoning.

#### Subfields
| Field | Type | Description |
|------|------|------------|
| `pacify` | Array[String] | Doshas pacified by the herb |
| `aggravate` | Array[String] | Doshas aggravated by the herb |
| `tridosha` | Boolean | Indicates if the herb balances all three doshas |

**Allowed Dosha Values:** `Vata`, `Pitta`, `Kapha`

---

## Ayurvedic Properties (Rasapanchaka)

### 8. `rasapanchaka`
- **Type:** Object  
- **Description:** Classical Ayurvedic pharmacological properties of the herb.

#### Subfields
| Field | Type | Description |
|------|------|------------|
| `rasa` | Array[String] | Taste (e.g., Katu, Tikta) |
| `guna` | Array[String] | Qualities (e.g., Laghu, Ruksha) |
| `virya` | String | Potency (Ushna / Sheeta) |
| `vipaka` | String | Post-digestive effect |

---

## Special Ayurvedic Action

### 9. `prabhav`
- **Type:** Array[String]  
- **Description:** Unique therapeutic actions of the herb beyond Rasapanchaka.  
- **Examples:**  
  `Rasayana`, `Krimighna`, `Kasahara`, `Shoolaghna`

---

## Metadata

### 10. `created_at`
- **Type:** ISODate  
- **Description:** Timestamp when the herb record was created.

### 11. `updated_at`
- **Type:** ISODate  
- **Description:** Timestamp of the most recent update.

---

## Relationship with Remedies

- Herbs are referenced in the `remedies.ingredients` field using `herb_id`.
- This design avoids data duplication and enables modular linking.
- Supports chatbot explanations such as:  
  *“This remedy contains Tulsi, which pacifies Kapha and Vata dosha.”*

---

## Example Document

```json
{
  "herb_id": "H001",
  "name": "Tulsi",
  "botanical_name": "Ocimum sanctum",
  "link": "https://www.amidhaayurveda.com/p/tulsi.html",
  "preview": "Tulsi is known as the Queen of Herbs in Ayurveda and supports immunity and respiratory health.",

  "dosha_effect": {
    "pacify": ["Vata", "Kapha"],
    "aggravate": ["Pitta"],
    "tridosha": false
  },

  "rasapanchaka": {
    "rasa": ["Katu", "Tikta"],
    "guna": ["Laghu", "Ruksha"],
    "virya": "Ushna",
    "vipaka": "Katu"
  },

  "prabhav": [
    "Rasayana",
    "Krimighna",
    "Kasahara",
    "Shoolaghna"
  ],

  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T10:00:00Z"
}
