#!/usr/bin/env python3
"""Populate Pitch Deck with Content"""
import json
import os
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]


def get_creds():
    return Credentials.from_authorized_user_file("token.json", SCOPES)


def populate_deck(pres_id, content_file):
    creds = get_creds()
    slides = build("slides", "v1", credentials=creds)

    with open(content_file, "r", encoding="utf-8") as f:
        content = json.load(f)

    pres = slides.presentations().get(presentationId=pres_id).execute()
    slide_list = pres.get("slides", [])

    print(f"Populating {len(slide_list)} slides...")

    for i, slide in enumerate(slide_list):
        slide_id = slide["objectId"]
        elements = slide.get("pageElements", [])

        requests = []
        for elem in elements:
            if "shape" in elem and elem["shape"].get("shapeType") == "TEXT_BOX":
                elem_id = elem["objectId"]
                text = get_text(elem_id, content, i)

                if text:
                    requests.append(
                        {
                            "deleteText": {
                                "objectId": elem_id,
                                "textRange": {"type": "ALL"},
                            }
                        }
                    )
                    requests.append(
                        {
                            "insertText": {
                                "objectId": elem_id,
                                "text": text,
                                "insertionIndex": 0,
                            }
                        }
                    )

        if requests:
            try:
                slides.presentations().batchUpdate(
                    presentationId=pres_id, body={"requests": requests}
                ).execute()
                print(f"  Updated slide {i+1}")
            except Exception as e:
                print(f"  Error on slide {i+1}: {e}")

    print(f"\nDeck updated: https://docs.google.com/presentation/d/{pres_id}/edit")


def get_text(elem_id, c, idx):
    if "title_company" in elem_id:
        return c.get("company_name", "")
    if "title_tagline" in elem_id:
        return c.get("tagline", "")
    if "prob_header" in elem_id:
        return c.get("problem_title", "The Problem")
    if "prob_bullets" in elem_id:
        return "\n".join([f" {p}" for p in c.get("problems", [])[:5]])
    if "sol_header" in elem_id:
        return c.get("solution_title", "Our Solution")
    if "sol_desc" in elem_id:
        return c.get("solution_description", "")
    if "sol_points" in elem_id:
        return "\n".join([f" {p}" for p in c.get("solution_points", [])[:5]])
    if "prod_header" in elem_id:
        return "How It Works"
    if "prod_name" in elem_id:
        return c.get("product_name", "")
    if "prod_features" in elem_id:
        return "\n".join([f" {f}" for f in c.get("features", [])[:6]])
    if "mkt_header" in elem_id:
        return "Market Opportunity"
    if "tam_val" in elem_id or "mkt_tam_val" in elem_id:
        return c.get("tam", "$60B")
    if "tam_lbl" in elem_id or "mkt_tam_lbl" in elem_id:
        return "TAM"
    if "tam_desc" in elem_id or "mkt_tam_desc" in elem_id:
        return "Total Addressable Market"
    if "sam_val" in elem_id or "mkt_sam_val" in elem_id:
        return c.get("sam", "$24B")
    if "sam_lbl" in elem_id or "mkt_sam_lbl" in elem_id:
        return "SAM"
    if "sam_desc" in elem_id or "mkt_sam_desc" in elem_id:
        return "Serviceable Addressable Market"
    if "som_val" in elem_id or "mkt_som_val" in elem_id:
        return c.get("som", "$500M")
    if "som_lbl" in elem_id or "mkt_som_lbl" in elem_id:
        return "SOM"
    if "som_desc" in elem_id or "mkt_som_desc" in elem_id:
        return "Serviceable Obtainable Market"
    if "mkt_desc" in elem_id:
        return c.get("market_description", "")
    if "comp_header" in elem_id:
        return "Competition"
    if "comp_list" in elem_id:
        comps = c.get("competitors", [])
        return "Competitive Landscape:\n" + "\n".join(
            [
                f" {co.get('name')}: {co.get('weakness')}"
                for co in comps[:4]
                if isinstance(co, dict)
            ]
        )
    if "diff_list" in elem_id:
        return "Our Advantages:\n" + "\n".join(
            [f" {d}" for d in c.get("differentiators", [])[:4]]
        )
    if "biz_header" in elem_id:
        return "Business Model"
    if "biz_model" in elem_id:
        return f"Model: {c.get('revenue_model', '')}"
    if "biz_pricing" in elem_id:
        return f"Pricing: {c.get('pricing', '')}"
    if "biz_streams_label" in elem_id:
        return "Revenue Streams:"
    if "biz_streams" in elem_id:
        return "\n".join([f" {s}" for s in c.get("revenue_streams", [])[:5]])
    if "trac_header" in elem_id:
        return "Traction"
    if "trac_val_0" in elem_id:
        return (
            c.get("traction_metrics", [])[0].get("value", "")
            if c.get("traction_metrics")
            else ""
        )
    if "trac_lbl_0" in elem_id:
        return (
            c.get("traction_metrics", [])[0].get("label", "")
            if c.get("traction_metrics")
            else ""
        )
    if "trac_val_1" in elem_id:
        return (
            c.get("traction_metrics", [])[1].get("value", "")
            if len(c.get("traction_metrics", [])) > 1
            else ""
        )
    if "trac_lbl_1" in elem_id:
        return (
            c.get("traction_metrics", [])[1].get("label", "")
            if len(c.get("traction_metrics", [])) > 1
            else ""
        )
    if "trac_val_2" in elem_id:
        return (
            c.get("traction_metrics", [])[2].get("value", "")
            if len(c.get("traction_metrics", [])) > 2
            else ""
        )
    if "trac_lbl_2" in elem_id:
        return (
            c.get("traction_metrics", [])[2].get("label", "")
            if len(c.get("traction_metrics", [])) > 2
            else ""
        )
    if "trac_miles" in elem_id:
        return "Key Milestones:\n" + "\n".join(
            [f" {m}" for m in c.get("milestones", [])[:4]]
        )
    if "team_header" in elem_id:
        return "Our Team"
    if "team_info_0" in elem_id:
        team = c.get("team", [])
        if team:
            return f"{team[0].get('name')}\n{team[0].get('role')}\n{team[0].get('background')}"
    if "fin_header" in elem_id:
        return "Financial Projections"
    if "fin_rev_y1_val" in elem_id:
        return c.get("revenue_y1", "$1M")
    if "fin_rev_y1_lbl" in elem_id:
        return "Year 1 Revenue"
    if "fin_rev_y5_val" in elem_id:
        return c.get("revenue_y5", "$10M")
    if "fin_rev_y5_lbl" in elem_id:
        return "Year 5 Revenue"
    if "fin_ebitda_val" in elem_id:
        return c.get("ebitda_y5", "$3M")
    if "fin_ebitda_lbl" in elem_id:
        return "Year 5 EBITDA"
    if "road_header" in elem_id:
        return "Roadmap"
    if "road_phase" in elem_id or "road_mile" in elem_id:
        roadmap = c.get("roadmap", [])
        for i in range(5):
            if f"_{i}" in elem_id and i < len(roadmap):
                if "phase" in elem_id:
                    return roadmap[i].get("phase", "")
                if "mile" in elem_id:
                    return roadmap[i].get("milestone", "")
    if "ask_header" in elem_id:
        return "Investment Ask"
    if "ask_amount" in elem_id:
        return c.get("ask_amount", "$1M")
    if "ask_label" in elem_id:
        return "Seed Round"
    if "ask_funds" in elem_id:
        funds = c.get("use_of_funds", [])
        return "Use of Funds:\n" + "\n".join(
            [
                f" {f.get('category')}: {f.get('percentage')}"
                for f in funds[:4]
                if isinstance(f, dict)
            ]
        )
    if "ask_contact" in elem_id:
        return f"Contact: {c.get('contact_email', '')}"
    if "ref_header" in elem_id:
        return "Sources & References"
    if "ref_subtitle" in elem_id:
        return "Market data and assumptions based on the following sources:"
    if "ref_list" in elem_id:
        refs = c.get("references", [])
        text = ""
        for i, ref in enumerate(refs[:8], 1):
            if isinstance(ref, dict):
                text += f"{i}. {ref.get('category')}: {ref.get('source')}\n"
                if ref.get("url"):
                    text += f"   {ref['url']}\n"
                text += "\n"
        return text
    if "ref_note" in elem_id:
        return "Full details in Financial Model: Sources & References sheet"
    return None


if __name__ == "__main__":
    populate_deck(sys.argv[1], sys.argv[2])
