"""
Pitch Deck Creator - From Scratch
=================================
Creates professional pitch decks from scratch with proper formatting and embedded charts.

Features:
1. Clean slides built programmatically (no template dependency)
2. Proper text sizing and layouts
3. Charts embedded directly from the financial model spreadsheet
4. Consistent branding and design

Usage:
    python create_pitch_deck.py --company "CompanyName" --content-file content.json
    python create_pitch_deck.py --company "CompanyName" --financial-model "SPREADSHEET_URL" --content-file content.json
    python create_pitch_deck.py --company "CompanyName" --type investor --content-file content.json
"""

import os
import sys
import argparse
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# =============================================================================
# DECK CONFIGURATIONS
# =============================================================================
DECK_TYPES = {
    "minimal": ["title", "problem", "solution", "market", "ask", "references"],
    "seed": ["title", "problem", "solution", "market", "business_model", "traction", "ask", "references"],
    "startup": ["title", "problem", "solution", "product", "market", "business_model", "traction", "team", "financials", "ask", "references"],
    "investor": ["title", "problem", "solution", "product", "market", "competition", "business_model", "traction", "team", "financials", "roadmap", "ask", "references"],
    "series_a": ["title", "executive_summary", "problem", "solution", "product", "market", "competition", "business_model", "traction", "team", "financials", "projections", "roadmap", "ask", "references"],
    "full": ["title", "executive_summary", "problem", "solution", "product", "market", "tam_sam_som", "competition", "business_model", "unit_economics", "traction", "team", "financials", "projections", "roadmap", "ask", "references"]
}

# =============================================================================
# DESIGN CONSTANTS
# =============================================================================
EMU = 914400  # EMUs per inch
SLIDE_WIDTH = int(10 * EMU)
SLIDE_HEIGHT = int(5.625 * EMU)

# Colors (RGB 0-1 scale)
COLORS = {
    "primary": {"red": 0.13, "green": 0.59, "blue": 0.95},     # Bright blue
    "secondary": {"red": 0.0, "green": 0.78, "blue": 0.62},    # Teal
    "accent": {"red": 1.0, "green": 0.6, "blue": 0.0},         # Orange
    "dark": {"red": 0.12, "green": 0.12, "blue": 0.15},        # Near black
    "light": {"red": 0.97, "green": 0.97, "blue": 0.98},       # Off white
    "white": {"red": 1.0, "green": 1.0, "blue": 1.0},
    "gray": {"red": 0.6, "green": 0.6, "blue": 0.65},
    "success": {"red": 0.2, "green": 0.78, "blue": 0.35},      # Green
    "warning": {"red": 1.0, "green": 0.76, "blue": 0.03},      # Yellow
}

# Font sizes (points)
FONT = {
    "title": 48,
    "subtitle": 24,
    "heading": 36,
    "subheading": 24,
    "body": 16,
    "small": 12,
    "metric_large": 56,
    "metric_medium": 40,
}


def pt(points):
    """Convert points to EMU for font sizes."""
    return int(points * 12700)


def inch(inches):
    """Convert inches to EMU."""
    return int(inches * EMU)


def get_credentials():
    """Get OAuth2 credentials."""
    creds = None
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception:
            pass
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


# =============================================================================
# SLIDE BUILDERS - Each function creates one slide type
# =============================================================================

def create_title_slide(slides_service, presentation_id, content):
    """Create title slide with company name and tagline."""
    company = content.get("company_name", "Company Name")
    tagline = content.get("tagline", "Your Vision Statement Here")
    
    requests = [
        {"createSlide": {"slideLayoutReference": {"predefinedLayout": "BLANK"}}},
    ]
    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()
    slide_id = response["replies"][0]["createSlide"]["objectId"]
    
    # Add elements
    requests = [
        # Background
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": COLORS["primary"]}}}},
            "fields": "pageBackgroundFill.solidFill.color"
        }},
        # Company name
        create_textbox(slide_id, "title_company", company, inch(0.5), inch(1.8), inch(9), inch(1.2),
                      FONT["title"], COLORS["white"], bold=True, align="CENTER"),
        # Tagline
        create_textbox(slide_id, "title_tagline", tagline, inch(1), inch(3.2), inch(8), inch(0.6),
                      FONT["subtitle"], COLORS["light"], align="CENTER"),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_problem_slide(slides_service, presentation_id, content):
    """Create problem statement slide."""
    problem_title = content.get("problem_title", "The Problem")
    problems = content.get("problems", [
        "Problem point 1 - describe the pain point",
        "Problem point 2 - why it matters",
        "Problem point 3 - current solutions fail"
    ])
    
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    # Build bullet text
    bullet_text = "\n".join([f" {p}" for p in problems[:5]])
    
    requests = [
        # Header
        create_textbox(slide_id, "prob_header", problem_title, inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        # Problem bullets
        create_textbox(slide_id, "prob_bullets", bullet_text, inch(0.5), inch(1.3), inch(9), inch(3.5),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_solution_slide(slides_service, presentation_id, content):
    """Create solution slide."""
    solution_title = content.get("solution_title", "Our Solution")
    solution_desc = content.get("solution_description", "A brief description of your solution and how it solves the problem.")
    solution_points = content.get("solution_points", [
        "Key benefit 1",
        "Key benefit 2", 
        "Key benefit 3"
    ])
    
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    bullet_text = "\n".join([f" {p}" for p in solution_points[:5]])
    
    requests = [
        create_textbox(slide_id, "sol_header", solution_title, inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "sol_desc", solution_desc, inch(0.5), inch(1.2), inch(9), inch(1),
                      FONT["body"], COLORS["gray"]),
        create_textbox(slide_id, "sol_points", bullet_text, inch(0.5), inch(2.4), inch(9), inch(2.5),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_product_slide(slides_service, presentation_id, content):
    """Create product/how it works slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    product_name = content.get("product_name", content.get("company_name", "Product"))
    features = content.get("features", ["Feature 1", "Feature 2", "Feature 3"])
    
    feature_text = "\n".join([f" {f}" for f in features[:6]])
    
    requests = [
        create_textbox(slide_id, "prod_header", "How It Works", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "prod_name", product_name, inch(0.5), inch(1.2), inch(4), inch(0.6),
                      FONT["subheading"], COLORS["primary"], bold=True),
        create_textbox(slide_id, "prod_features", feature_text, inch(0.5), inch(1.9), inch(4.5), inch(3),
                      FONT["body"], COLORS["dark"], line_spacing=170),
        # Placeholder for product image/demo
        create_shape(slide_id, "prod_image_placeholder", inch(5.5), inch(1.2), inch(4), inch(3.5),
                    COLORS["light"], "Product Screenshot / Demo"),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_market_slide(slides_service, presentation_id, content):
    """Create market size slide with TAM/SAM/SOM."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    tam = content.get("tam", "$50B")
    sam = content.get("sam", "$10B")
    som = content.get("som", "$500M")
    market_desc = content.get("market_description", "Description of your target market opportunity")
    
    requests = [
        create_textbox(slide_id, "mkt_header", "Market Opportunity", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        # TAM
        create_metric_box(slide_id, "tam", tam, "TAM", "Total Addressable Market", inch(0.5), inch(1.3), COLORS["primary"]),
        # SAM
        create_metric_box(slide_id, "sam", sam, "SAM", "Serviceable Market", inch(3.5), inch(1.3), COLORS["secondary"]),
        # SOM
        create_metric_box(slide_id, "som", som, "SOM", "Target Market", inch(6.5), inch(1.3), COLORS["accent"]),
        # Description
        create_textbox(slide_id, "mkt_desc", market_desc, inch(0.5), inch(4), inch(9), inch(1),
                      FONT["small"], COLORS["gray"]),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_competition_slide(slides_service, presentation_id, content):
    """Create competitive landscape slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    competitors = content.get("competitors", [
        {"name": "Competitor A", "weakness": "Too expensive"},
        {"name": "Competitor B", "weakness": "Poor UX"},
        {"name": "Competitor C", "weakness": "Limited features"},
    ])
    differentiators = content.get("differentiators", ["Our unique advantage 1", "Our unique advantage 2"])
    
    # Build competitor text
    comp_text = "Competitive Landscape:\n"
    for c in competitors[:4]:
        if isinstance(c, dict):
            comp_text += f"\n {c.get('name', 'Competitor')}: {c.get('weakness', '')}"
        else:
            comp_text += f"\n {c}"
    
    diff_text = "Our Advantages:\n" + "\n".join([f" {d}" for d in differentiators[:4]])
    
    requests = [
        create_textbox(slide_id, "comp_header", "Competition", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "comp_list", comp_text, inch(0.5), inch(1.2), inch(4.5), inch(2.5),
                      FONT["body"], COLORS["dark"], line_spacing=160),
        create_textbox(slide_id, "diff_list", diff_text, inch(5.2), inch(1.2), inch(4.3), inch(2.5),
                      FONT["body"], COLORS["success"], line_spacing=160),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_business_model_slide(slides_service, presentation_id, content):
    """Create business model / revenue slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    revenue_model = content.get("revenue_model", "Subscription-based SaaS")
    pricing = content.get("pricing", "$99/month per user")
    revenue_streams = content.get("revenue_streams", ["Primary revenue stream", "Secondary stream", "Future expansion"])
    
    streams_text = "\n".join([f" {s}" for s in revenue_streams[:5]])
    
    requests = [
        create_textbox(slide_id, "biz_header", "Business Model", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "biz_model", f"Model: {revenue_model}", inch(0.5), inch(1.2), inch(4.5), inch(0.5),
                      FONT["subheading"], COLORS["primary"], bold=True),
        create_textbox(slide_id, "biz_pricing", f"Pricing: {pricing}", inch(0.5), inch(1.8), inch(4.5), inch(0.5),
                      FONT["body"], COLORS["dark"]),
        create_textbox(slide_id, "biz_streams_label", "Revenue Streams:", inch(0.5), inch(2.5), inch(4.5), inch(0.4),
                      FONT["body"], COLORS["gray"], bold=True),
        create_textbox(slide_id, "biz_streams", streams_text, inch(0.5), inch(3), inch(4.5), inch(2),
                      FONT["body"], COLORS["dark"], line_spacing=160),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_traction_slide(slides_service, presentation_id, content):
    """Create traction/metrics slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    metrics = content.get("traction_metrics", [
        {"value": "1,000+", "label": "Customers"},
        {"value": "$500K", "label": "ARR"},
        {"value": "50%", "label": "MoM Growth"},
    ])
    
    milestones = content.get("milestones", ["Milestone 1 achieved", "Milestone 2 achieved"])
    
    requests = [
        create_textbox(slide_id, "trac_header", "Traction", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    # Add metrics boxes
    x_positions = [0.5, 3.5, 6.5]
    for i, metric in enumerate(metrics[:3]):
        if isinstance(metric, dict):
            val = metric.get("value", "N/A")
            lbl = metric.get("label", "Metric")
        else:
            val, lbl = str(metric), f"Metric {i+1}"
        
        requests.append(create_textbox(slide_id, f"trac_val_{i}", val, inch(x_positions[i]), inch(1.3), inch(2.8), inch(1),
                                       FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
        requests.append(create_textbox(slide_id, f"trac_lbl_{i}", lbl, inch(x_positions[i]), inch(2.3), inch(2.8), inch(0.5),
                                       FONT["small"], COLORS["gray"], align="CENTER"))
    
    # Milestones
    if milestones:
        mile_text = "Key Milestones:\n" + "\n".join([f" {m}" for m in milestones[:4]])
        requests.append(create_textbox(slide_id, "trac_miles", mile_text, inch(0.5), inch(3.2), inch(9), inch(1.8),
                                       FONT["small"], COLORS["dark"], line_spacing=150))
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_team_slide(slides_service, presentation_id, content):
    """Create team slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    team = content.get("team", [
        {"name": "CEO Name", "role": "CEO & Founder", "background": "10+ years experience"},
        {"name": "CTO Name", "role": "CTO", "background": "Ex-Google engineer"},
        {"name": "COO Name", "role": "COO", "background": "Operations expert"},
    ])
    
    requests = [
        create_textbox(slide_id, "team_header", "Our Team", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    # Add team members
    x_positions = [0.5, 3.5, 6.5]
    for i, member in enumerate(team[:3]):
        if isinstance(member, dict):
            name = member.get("name", "Name")
            role = member.get("role", "Role")
            bg = member.get("background", "")
        else:
            name, role, bg = str(member), "", ""
        
        member_text = f"{name}\n{role}\n{bg}"
        # Avatar placeholder
        requests.append(create_shape(slide_id, f"team_avatar_{i}", inch(x_positions[i]), inch(1.2), inch(1.2), inch(1.2),
                                     COLORS["light"], ""))
        requests.append(create_textbox(slide_id, f"team_info_{i}", member_text, inch(x_positions[i]), inch(2.5), inch(2.8), inch(1.5),
                                       FONT["small"], COLORS["dark"], align="CENTER", line_spacing=140))
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_financials_slide(slides_service, presentation_id, content, chart_info=None):
    """Create financials slide with optional embedded chart."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    revenue_y1 = content.get("revenue_y1", "$1M")
    revenue_y5 = content.get("revenue_y5", "$10M")
    ebitda_y5 = content.get("ebitda_y5", "$3M")
    margin_y5 = content.get("margin_y5", "30%")
    
    requests = [
        create_textbox(slide_id, "fin_header", "Financial Projections", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    # Key metrics
    requests.append(create_textbox(slide_id, "fin_rev_y1_val", revenue_y1, inch(0.5), inch(1.3), inch(2.2), inch(0.8),
                                   FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
    requests.append(create_textbox(slide_id, "fin_rev_y1_lbl", "Year 1 Revenue", inch(0.5), inch(2.1), inch(2.2), inch(0.4),
                                   FONT["small"], COLORS["gray"], align="CENTER"))
    
    requests.append(create_textbox(slide_id, "fin_rev_y5_val", revenue_y5, inch(3.3), inch(1.3), inch(2.2), inch(0.8),
                                   FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
    requests.append(create_textbox(slide_id, "fin_rev_y5_lbl", "Year 5 Revenue", inch(3.3), inch(2.1), inch(2.2), inch(0.4),
                                   FONT["small"], COLORS["gray"], align="CENTER"))
    
    requests.append(create_textbox(slide_id, "fin_ebitda_val", ebitda_y5, inch(6.1), inch(1.3), inch(2.2), inch(0.8),
                                   FONT["metric_medium"], COLORS["secondary"], bold=True, align="CENTER"))
    requests.append(create_textbox(slide_id, "fin_ebitda_lbl", "Year 5 EBITDA", inch(6.1), inch(2.1), inch(2.2), inch(0.4),
                                   FONT["small"], COLORS["gray"], align="CENTER"))
    
    # Chart placeholder or embedded chart
    if chart_info and chart_info.get("revenue_chart_id"):
        # Embed chart from sheets
        requests.append({
            "createSheetsChart": {
                "objectId": f"{slide_id}_revenue_chart",
                "spreadsheetId": chart_info["spreadsheet_id"],
                "chartId": chart_info["revenue_chart_id"],
                "linkingMode": "LINKED",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": inch(8), "unit": "EMU"}, "height": {"magnitude": inch(2.3), "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": inch(1), "translateY": inch(2.7), "unit": "EMU"}
                }
            }
        })
    else:
        # Placeholder
        requests.append(create_shape(slide_id, "fin_chart_placeholder", inch(0.5), inch(2.7), inch(9), inch(2.3),
                                     COLORS["light"], "Revenue Growth Chart"))
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_projections_slide(slides_service, presentation_id, content, chart_info=None):
    """Create detailed projections slide with P&L summary."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    # Get financial data
    y1 = content.get("revenue_y1", "$1M")
    y5 = content.get("revenue_y5", "$10M")
    y10 = content.get("revenue_y10", "$50M")
    
    requests = [
        create_textbox(slide_id, "proj_header", "5-Year Projections", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    # Revenue progression
    years = ["Y1", "Y3", "Y5"]
    values = [y1, content.get("revenue_y3", "$5M"), y5]
    x_positions = [0.8, 4, 7.2]
    
    for i, (year, val) in enumerate(zip(years, values)):
        requests.append(create_textbox(slide_id, f"proj_year_{i}", year, inch(x_positions[i]), inch(1.3), inch(2), inch(0.4),
                                       FONT["subheading"], COLORS["gray"], align="CENTER"))
        requests.append(create_textbox(slide_id, f"proj_val_{i}", val, inch(x_positions[i]), inch(1.7), inch(2), inch(0.8),
                                       FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
    
    # Chart area
    if chart_info and chart_info.get("revenue_chart_id"):
        requests.append({
            "createSheetsChart": {
                "objectId": f"{slide_id}_proj_chart",
                "spreadsheetId": chart_info["spreadsheet_id"],
                "chartId": chart_info["revenue_chart_id"],
                "linkingMode": "LINKED",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": inch(9), "unit": "EMU"}, "height": {"magnitude": inch(2.5), "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": inch(0.5), "translateY": inch(2.8), "unit": "EMU"}
                }
            }
        })
    else:
        requests.append(create_shape(slide_id, "proj_chart_placeholder", inch(0.5), inch(2.8), inch(9), inch(2.2),
                                     COLORS["light"], "Revenue & EBITDA Projection Chart"))
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_roadmap_slide(slides_service, presentation_id, content):
    """Create roadmap/timeline slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    roadmap = content.get("roadmap", [
        {"phase": "Q1-Q2", "milestone": "Product launch, first 100 customers"},
        {"phase": "Q3-Q4", "milestone": "Scale to 1,000 customers, Series A"},
        {"phase": "Year 2", "milestone": "Expand to new markets"},
    ])
    
    requests = [
        create_textbox(slide_id, "road_header", "Roadmap", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    # Timeline items
    y_pos = 1.4
    for i, item in enumerate(roadmap[:5]):
        if isinstance(item, dict):
            phase = item.get("phase", f"Phase {i+1}")
            milestone = item.get("milestone", "Milestone")
        else:
            phase, milestone = f"Phase {i+1}", str(item)
        
        requests.append(create_textbox(slide_id, f"road_phase_{i}", phase, inch(0.5), inch(y_pos), inch(1.5), inch(0.4),
                                       FONT["body"], COLORS["primary"], bold=True))
        requests.append(create_textbox(slide_id, f"road_mile_{i}", milestone, inch(2.2), inch(y_pos), inch(7.3), inch(0.5),
                                       FONT["body"], COLORS["dark"]))
        y_pos += 0.7
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_ask_slide(slides_service, presentation_id, content):
    """Create investment ask / closing slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    ask_amount = content.get("ask_amount", "$2M")
    use_of_funds = content.get("use_of_funds", [
        {"category": "Product Development", "percentage": "40%"},
        {"category": "Sales & Marketing", "percentage": "35%"},
        {"category": "Operations", "percentage": "25%"},
    ])
    contact_email = content.get("contact_email", "contact@company.com")
    company = content.get("company_name", "Company")
    
    requests = [
        # Background
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": COLORS["dark"]}}}},
            "fields": "pageBackgroundFill.solidFill.color"
        }},
        create_textbox(slide_id, "ask_header", "Investment Ask", inch(0.5), inch(0.3), inch(9), inch(0.7),
                      FONT["heading"], COLORS["white"], bold=True),
        create_textbox(slide_id, "ask_amount", ask_amount, inch(0.5), inch(1.1), inch(9), inch(1),
                      FONT["metric_large"], COLORS["accent"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ask_label", "Seed Round", inch(0.5), inch(2.1), inch(9), inch(0.4),
                      FONT["subheading"], COLORS["light"], align="CENTER"),
    ]
    
    # Use of funds
    funds_text = "Use of Funds:\n"
    for item in use_of_funds[:4]:
        if isinstance(item, dict):
            cat = item.get("category", "Category")
            pct = item.get("percentage", "25%")
            funds_text += f"\n {cat}: {pct}"
        else:
            funds_text += f"\n {item}"
    
    requests.append(create_textbox(slide_id, "ask_funds", funds_text, inch(0.5), inch(2.8), inch(5), inch(2),
                                   FONT["small"], COLORS["light"], line_spacing=150))
    
    # Contact
    requests.append(create_textbox(slide_id, "ask_contact", f"Contact: {contact_email}", inch(0.5), inch(5), inch(9), inch(0.4),
                                   FONT["small"], COLORS["gray"], align="CENTER"))
    
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_executive_summary_slide(slides_service, presentation_id, content):
    """Create executive summary slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    summary_points = content.get("executive_summary", [
        "Brief company description",
        "Problem we solve",
        "Our unique solution",
        "Market opportunity",
        "Traction to date"
    ])
    
    bullet_text = "\n".join([f" {p}" for p in summary_points[:6]])
    
    requests = [
        create_textbox(slide_id, "exec_header", "Executive Summary", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "exec_bullets", bullet_text, inch(0.5), inch(1.3), inch(9), inch(3.8),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_tam_sam_som_slide(slides_service, presentation_id, content):
    """Create detailed TAM/SAM/SOM slide with descriptions."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    tam = content.get("tam", "$50B")
    sam = content.get("sam", "$10B")
    som = content.get("som", "$500M")
    tam_desc = content.get("tam_description", "Total global market for this category")
    sam_desc = content.get("sam_description", "Portion we can realistically serve")
    som_desc = content.get("som_description", "Our target in the next 5 years")
    
    requests = [
        create_textbox(slide_id, "tss_header", "Market Size", inch(0.5), inch(0.3), inch(9), inch(0.7),
                      FONT["heading"], COLORS["dark"], bold=True),
        
        # TAM
        create_textbox(slide_id, "tss_tam_val", tam, inch(0.5), inch(1.2), inch(2.8), inch(0.8),
                      FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_tam_lbl", "TAM", inch(0.5), inch(2), inch(2.8), inch(0.3),
                      FONT["body"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_tam_desc", tam_desc, inch(0.5), inch(2.4), inch(2.8), inch(0.8),
                      FONT["small"], COLORS["gray"], align="CENTER"),
        
        # SAM
        create_textbox(slide_id, "tss_sam_val", sam, inch(3.6), inch(1.2), inch(2.8), inch(0.8),
                      FONT["metric_medium"], COLORS["secondary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_sam_lbl", "SAM", inch(3.6), inch(2), inch(2.8), inch(0.3),
                      FONT["body"], COLORS["secondary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_sam_desc", sam_desc, inch(3.6), inch(2.4), inch(2.8), inch(0.8),
                      FONT["small"], COLORS["gray"], align="CENTER"),
        
        # SOM
        create_textbox(slide_id, "tss_som_val", som, inch(6.7), inch(1.2), inch(2.8), inch(0.8),
                      FONT["metric_medium"], COLORS["accent"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_som_lbl", "SOM", inch(6.7), inch(2), inch(2.8), inch(0.3),
                      FONT["body"], COLORS["accent"], bold=True, align="CENTER"),
        create_textbox(slide_id, "tss_som_desc", som_desc, inch(6.7), inch(2.4), inch(2.8), inch(0.8),
                      FONT["small"], COLORS["gray"], align="CENTER"),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


def create_unit_economics_slide(slides_service, presentation_id, content):
    """Create unit economics slide."""
    slide_id = create_blank_slide(slides_service, presentation_id)
    
    cac = content.get("cac", "$500")
    ltv = content.get("ltv", "$2,500")
    ltv_cac = content.get("ltv_cac_ratio", "5x")
    payback = content.get("payback_period", "6 months")
    
    requests = [
        create_textbox(slide_id, "ue_header", "Unit Economics", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        
        create_textbox(slide_id, "ue_cac_val", cac, inch(0.5), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["warning"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_cac_lbl", "CAC", inch(0.5), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        
        create_textbox(slide_id, "ue_ltv_val", ltv, inch(2.8), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["success"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_ltv_lbl", "LTV", inch(2.8), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        
        create_textbox(slide_id, "ue_ratio_val", ltv_cac, inch(5.1), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_ratio_lbl", "LTV:CAC", inch(5.1), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        
        create_textbox(slide_id, "ue_payback_val", payback, inch(7.4), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["secondary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_payback_lbl", "Payback", inch(7.4), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
    ]
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": flatten(requests)}).execute()
    return slide_id


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_blank_slide(slides_service, presentation_id):
    """Create a blank slide and return its ID."""
    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": [{"createSlide": {"slideLayoutReference": {"predefinedLayout": "BLANK"}}}]}
    ).execute()
    return response["replies"][0]["createSlide"]["objectId"]


def create_textbox(slide_id, element_id, text, x, y, width, height, font_size, color, bold=False, align="START", line_spacing=100):
    """Create a textbox element request."""
    # Map alignment values to Google Slides API values
    align_map = {"LEFT": "START", "CENTER": "CENTER", "RIGHT": "END", "START": "START", "END": "END"}
    alignment = align_map.get(align.upper(), "START")
    
    obj_id = f"{slide_id}_{element_id}"
    return [
        {
            "createShape": {
                "objectId": obj_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": width, "unit": "EMU"}, "height": {"magnitude": height, "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}
                }
            }
        },
        {
            "insertText": {
                "objectId": obj_id,
                "text": text,
                "insertionIndex": 0
            }
        },
        {
            "updateTextStyle": {
                "objectId": obj_id,
                "style": {
                    "fontSize": {"magnitude": font_size, "unit": "PT"},
                    "foregroundColor": {"opaqueColor": {"rgbColor": color}},
                    "bold": bold,
                    "fontFamily": "Open Sans"
                },
                "textRange": {"type": "ALL"},
                "fields": "fontSize,foregroundColor,bold,fontFamily"
            }
        },
        {
            "updateParagraphStyle": {
                "objectId": obj_id,
                "style": {
                    "alignment": alignment,
                    "lineSpacing": line_spacing
                },
                "textRange": {"type": "ALL"},
                "fields": "alignment,lineSpacing"
            }
        }
    ]


def create_shape(slide_id, element_id, x, y, width, height, fill_color, text=""):
    """Create a shape (rectangle) element request."""
    obj_id = f"{slide_id}_{element_id}"
    requests = [
        {
            "createShape": {
                "objectId": obj_id,
                "shapeType": "RECTANGLE",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": width, "unit": "EMU"}, "height": {"magnitude": height, "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}
                }
            }
        },
        {
            "updateShapeProperties": {
                "objectId": obj_id,
                "shapeProperties": {
                    "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": fill_color}}}
                },
                "fields": "shapeBackgroundFill.solidFill.color"
            }
        }
    ]
    if text:
        requests.extend([
            {"insertText": {"objectId": obj_id, "text": text, "insertionIndex": 0}},
            {"updateTextStyle": {
                "objectId": obj_id,
                "style": {"fontSize": {"magnitude": 12, "unit": "PT"}, "foregroundColor": {"opaqueColor": {"rgbColor": COLORS["gray"]}}},
                "textRange": {"type": "ALL"},
                "fields": "fontSize,foregroundColor"
            }},
            {"updateParagraphStyle": {"objectId": obj_id, "style": {"alignment": "CENTER"}, "textRange": {"type": "ALL"}, "fields": "alignment"}}
        ])
    return requests


def create_metric_box(slide_id, metric_id, value, label, description, x, y, color):
    """Create a metric display box (value + label + description)."""
    return [
        create_textbox(slide_id, f"{metric_id}_val", value, x, y, inch(2.8), inch(0.8),
                      FONT["metric_medium"], color, bold=True, align="CENTER"),
        create_textbox(slide_id, f"{metric_id}_lbl", label, x, y + inch(0.8), inch(2.8), inch(0.4),
                      FONT["body"], color, bold=True, align="CENTER"),
        create_textbox(slide_id, f"{metric_id}_desc", description, x, y + inch(1.3), inch(2.8), inch(0.8),
                      FONT["small"], COLORS["gray"], align="CENTER"),
    ]


def flatten(nested_list):
    """Flatten a nested list of requests."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# =============================================================================
# CONTENT BUILDERS - Return requests without executing (for batching)
# =============================================================================

def build_title_content(slide_id, content):
    """Build title slide content requests."""
    company = content.get("company_name", "Company Name")
    tagline = content.get("tagline", "Your Vision Statement Here")
    return [
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": COLORS["primary"]}}}},
            "fields": "pageBackgroundFill.solidFill.color"
        }},
        create_textbox(slide_id, "title_company", company, inch(0.5), inch(1.8), inch(9), inch(1.2),
                      FONT["title"], COLORS["white"], bold=True, align="CENTER"),
        create_textbox(slide_id, "title_tagline", tagline, inch(1), inch(3.2), inch(8), inch(0.6),
                      FONT["subtitle"], COLORS["light"], align="CENTER"),
    ]


def build_problem_content(slide_id, content):
    """Build problem slide content requests."""
    problem_title = content.get("problem_title", "The Problem")
    problems = content.get("problems", ["Problem point 1", "Problem point 2", "Problem point 3"])
    bullet_text = "\n".join([f"• {p}" for p in problems[:5]])
    return [
        create_textbox(slide_id, "prob_header", problem_title, inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "prob_bullets", bullet_text, inch(0.5), inch(1.3), inch(9), inch(3.5),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]


def build_solution_content(slide_id, content):
    """Build solution slide content requests."""
    solution_title = content.get("solution_title", "Our Solution")
    solution_desc = content.get("solution_description", "Brief description of your solution.")
    solution_points = content.get("solution_points", ["Benefit 1", "Benefit 2", "Benefit 3"])
    bullet_text = "\n".join([f"✓ {p}" for p in solution_points[:5]])
    return [
        create_textbox(slide_id, "sol_header", solution_title, inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "sol_desc", solution_desc, inch(0.5), inch(1.2), inch(9), inch(1),
                      FONT["body"], COLORS["gray"]),
        create_textbox(slide_id, "sol_points", bullet_text, inch(0.5), inch(2.4), inch(9), inch(2.5),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]


def build_product_content(slide_id, content):
    """Build product slide content requests."""
    product_name = content.get("product_name", content.get("company_name", "Product"))
    features = content.get("features", ["Feature 1", "Feature 2", "Feature 3"])
    feature_text = "\n".join([f"• {f}" for f in features[:6]])
    return [
        create_textbox(slide_id, "prod_header", "How It Works", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "prod_name", product_name, inch(0.5), inch(1.2), inch(4), inch(0.6),
                      FONT["subheading"], COLORS["primary"], bold=True),
        create_textbox(slide_id, "prod_features", feature_text, inch(0.5), inch(1.9), inch(4.5), inch(3),
                      FONT["body"], COLORS["dark"], line_spacing=170),
        create_shape(slide_id, "prod_image", inch(5.5), inch(1.2), inch(4), inch(3.5),
                    COLORS["light"], "Product Demo"),
    ]


def build_market_content(slide_id, content):
    """Build market slide content requests."""
    tam = content.get("tam", "$50B")
    sam = content.get("sam", "$10B")
    som = content.get("som", "$500M")
    market_desc = content.get("market_description", "Target market opportunity")
    return [
        create_textbox(slide_id, "mkt_header", "Market Opportunity", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_metric_box(slide_id, "tam", tam, "TAM", "Total Addressable", inch(0.5), inch(1.3), COLORS["primary"]),
        create_metric_box(slide_id, "sam", sam, "SAM", "Serviceable", inch(3.5), inch(1.3), COLORS["secondary"]),
        create_metric_box(slide_id, "som", som, "SOM", "Target", inch(6.5), inch(1.3), COLORS["accent"]),
        create_textbox(slide_id, "mkt_desc", market_desc, inch(0.5), inch(4), inch(9), inch(1),
                      FONT["small"], COLORS["gray"]),
    ]


def build_tam_sam_som_content(slide_id, content):
    """Build detailed TAM/SAM/SOM slide."""
    return build_market_content(slide_id, content)  # Same as market for now


def build_competition_content(slide_id, content):
    """Build competition slide content requests."""
    competitors = content.get("competitors", [{"name": "Competitor A", "weakness": "Too expensive"}])
    differentiators = content.get("differentiators", ["Our unique advantage"])
    
    comp_text = "Competitive Landscape:\n"
    for c in competitors[:4]:
        if isinstance(c, dict):
            comp_text += f"\n• {c.get('name', 'Competitor')}: {c.get('weakness', '')}"
        else:
            comp_text += f"\n• {c}"
    
    diff_text = "Our Advantages:\n" + "\n".join([f"✓ {d}" for d in differentiators[:4]])
    
    return [
        create_textbox(slide_id, "comp_header", "Competition", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "comp_list", comp_text, inch(0.5), inch(1.2), inch(4.5), inch(2.5),
                      FONT["body"], COLORS["dark"], line_spacing=160),
        create_textbox(slide_id, "diff_list", diff_text, inch(5.2), inch(1.2), inch(4.3), inch(2.5),
                      FONT["body"], COLORS["success"], line_spacing=160),
    ]


def build_business_model_content(slide_id, content):
    """Build business model slide content requests."""
    revenue_model = content.get("revenue_model", "Subscription SaaS")
    pricing = content.get("pricing", "$99/month")
    revenue_streams = content.get("revenue_streams", ["Primary revenue", "Secondary"])
    streams_text = "\n".join([f"• {s}" for s in revenue_streams[:5]])
    
    return [
        create_textbox(slide_id, "biz_header", "Business Model", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "biz_model", f"Model: {revenue_model}", inch(0.5), inch(1.2), inch(4.5), inch(0.5),
                      FONT["subheading"], COLORS["primary"], bold=True),
        create_textbox(slide_id, "biz_pricing", f"Pricing: {pricing}", inch(0.5), inch(1.8), inch(4.5), inch(0.5),
                      FONT["body"], COLORS["dark"]),
        create_textbox(slide_id, "biz_streams_label", "Revenue Streams:", inch(0.5), inch(2.5), inch(4.5), inch(0.4),
                      FONT["body"], COLORS["gray"], bold=True),
        create_textbox(slide_id, "biz_streams", streams_text, inch(0.5), inch(3), inch(4.5), inch(2),
                      FONT["body"], COLORS["dark"], line_spacing=160),
    ]


def build_unit_economics_content(slide_id, content):
    """Build unit economics slide content requests."""
    cac = content.get("cac", "$500")
    ltv = content.get("ltv", "$2,500")
    ltv_cac = content.get("ltv_cac_ratio", "5x")
    payback = content.get("payback_period", "6 months")
    
    return [
        create_textbox(slide_id, "ue_header", "Unit Economics", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "ue_cac_val", cac, inch(0.5), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["warning"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_cac_lbl", "CAC", inch(0.5), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        create_textbox(slide_id, "ue_ltv_val", ltv, inch(2.8), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["success"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_ltv_lbl", "LTV", inch(2.8), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        create_textbox(slide_id, "ue_ratio_val", ltv_cac, inch(5.1), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_ratio_lbl", "LTV:CAC", inch(5.1), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
        create_textbox(slide_id, "ue_payback_val", payback, inch(7.4), inch(1.4), inch(2), inch(0.7),
                      FONT["metric_medium"], COLORS["secondary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ue_payback_lbl", "Payback", inch(7.4), inch(2.1), inch(2), inch(0.4),
                      FONT["body"], COLORS["gray"], align="CENTER"),
    ]


def build_traction_content(slide_id, content):
    """Build traction slide content requests."""
    metrics = content.get("traction_metrics", [
        {"value": "1,000+", "label": "Customers"},
        {"value": "$500K", "label": "ARR"},
        {"value": "50%", "label": "Growth"},
    ])
    milestones = content.get("milestones", ["Milestone 1", "Milestone 2"])
    
    requests = [
        create_textbox(slide_id, "trac_header", "Traction", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    x_positions = [0.5, 3.5, 6.5]
    for i, metric in enumerate(metrics[:3]):
        if isinstance(metric, dict):
            val = metric.get("value", "N/A")
            lbl = metric.get("label", "Metric")
        else:
            val, lbl = str(metric), f"Metric {i+1}"
        requests.append(create_textbox(slide_id, f"trac_val_{i}", val, inch(x_positions[i]), inch(1.3), inch(2.8), inch(1),
                                       FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
        requests.append(create_textbox(slide_id, f"trac_lbl_{i}", lbl, inch(x_positions[i]), inch(2.3), inch(2.8), inch(0.5),
                                       FONT["small"], COLORS["gray"], align="CENTER"))
    
    if milestones:
        mile_text = "Key Milestones:\n" + "\n".join([f"✓ {m}" for m in milestones[:4]])
        requests.append(create_textbox(slide_id, "trac_miles", mile_text, inch(0.5), inch(3.2), inch(9), inch(1.8),
                                       FONT["small"], COLORS["dark"], line_spacing=150))
    return requests


def build_team_content(slide_id, content):
    """Build team slide content requests."""
    team = content.get("team", [
        {"name": "CEO Name", "role": "CEO", "background": "Background"},
        {"name": "CTO Name", "role": "CTO", "background": "Background"},
    ])
    
    requests = [
        create_textbox(slide_id, "team_header", "Our Team", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    x_positions = [0.5, 3.5, 6.5]
    for i, member in enumerate(team[:3]):
        if isinstance(member, dict):
            name = member.get("name", "Name")
            role = member.get("role", "Role")
            bg = member.get("background", "")
        else:
            name, role, bg = str(member), "", ""
        member_text = f"{name}\n{role}\n{bg}"
        requests.append(create_shape(slide_id, f"team_avatar_{i}", inch(x_positions[i]), inch(1.2), inch(1.2), inch(1.2),
                                     COLORS["light"], ""))
        requests.append(create_textbox(slide_id, f"team_info_{i}", member_text, inch(x_positions[i]), inch(2.5), inch(2.8), inch(1.5),
                                       FONT["small"], COLORS["dark"], align="CENTER", line_spacing=140))
    return requests


def build_financials_content(slide_id, content, chart_info=None):
    """Build financials slide content requests."""
    revenue_y1 = content.get("revenue_y1", "$1M")
    revenue_y5 = content.get("revenue_y5", "$10M")
    ebitda_y5 = content.get("ebitda_y5", "$3M")
    
    requests = [
        create_textbox(slide_id, "fin_header", "Financial Projections", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "fin_rev_y1_val", revenue_y1, inch(0.5), inch(1.3), inch(2.2), inch(0.8),
                      FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "fin_rev_y1_lbl", "Year 1 Revenue", inch(0.5), inch(2.1), inch(2.2), inch(0.4),
                      FONT["small"], COLORS["gray"], align="CENTER"),
        create_textbox(slide_id, "fin_rev_y5_val", revenue_y5, inch(3.3), inch(1.3), inch(2.2), inch(0.8),
                      FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "fin_rev_y5_lbl", "Year 5 Revenue", inch(3.3), inch(2.1), inch(2.2), inch(0.4),
                      FONT["small"], COLORS["gray"], align="CENTER"),
        create_textbox(slide_id, "fin_ebitda_val", ebitda_y5, inch(6.1), inch(1.3), inch(2.2), inch(0.8),
                      FONT["metric_medium"], COLORS["secondary"], bold=True, align="CENTER"),
        create_textbox(slide_id, "fin_ebitda_lbl", "Year 5 EBITDA", inch(6.1), inch(2.1), inch(2.2), inch(0.4),
                      FONT["small"], COLORS["gray"], align="CENTER"),
    ]
    
    if chart_info and chart_info.get("revenue_chart_id"):
        requests.append({
            "createSheetsChart": {
                "objectId": f"{slide_id}_revenue_chart",
                "spreadsheetId": chart_info["spreadsheet_id"],
                "chartId": chart_info["revenue_chart_id"],
                "linkingMode": "LINKED",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": inch(8), "unit": "EMU"}, "height": {"magnitude": inch(2.3), "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": inch(1), "translateY": inch(2.7), "unit": "EMU"}
                }
            }
        })
    else:
        requests.append(create_shape(slide_id, "fin_chart", inch(0.5), inch(2.7), inch(9), inch(2.3),
                                     COLORS["light"], "Revenue Chart"))
    return requests


def build_projections_content(slide_id, content, chart_info=None):
    """Build projections slide content requests."""
    y1 = content.get("revenue_y1", "$1M")
    y3 = content.get("revenue_y3", "$5M")
    y5 = content.get("revenue_y5", "$10M")
    
    requests = [
        create_textbox(slide_id, "proj_header", "5-Year Projections", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    years = ["Y1", "Y3", "Y5"]
    values = [y1, y3, y5]
    x_positions = [0.8, 4, 7.2]
    
    for i, (year, val) in enumerate(zip(years, values)):
        requests.append(create_textbox(slide_id, f"proj_year_{i}", year, inch(x_positions[i]), inch(1.3), inch(2), inch(0.4),
                                       FONT["subheading"], COLORS["gray"], align="CENTER"))
        requests.append(create_textbox(slide_id, f"proj_val_{i}", val, inch(x_positions[i]), inch(1.7), inch(2), inch(0.8),
                                       FONT["metric_medium"], COLORS["primary"], bold=True, align="CENTER"))
    
    if chart_info and chart_info.get("revenue_chart_id"):
        requests.append({
            "createSheetsChart": {
                "objectId": f"{slide_id}_proj_chart",
                "spreadsheetId": chart_info["spreadsheet_id"],
                "chartId": chart_info["revenue_chart_id"],
                "linkingMode": "LINKED",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": inch(9), "unit": "EMU"}, "height": {"magnitude": inch(2.5), "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": inch(0.5), "translateY": inch(2.8), "unit": "EMU"}
                }
            }
        })
    else:
        requests.append(create_shape(slide_id, "proj_chart", inch(0.5), inch(2.8), inch(9), inch(2.2),
                                     COLORS["light"], "Projection Chart"))
    return requests


def build_roadmap_content(slide_id, content):
    """Build roadmap slide content requests."""
    roadmap = content.get("roadmap", [
        {"phase": "Q1-Q2", "milestone": "Launch and first customers"},
        {"phase": "Q3-Q4", "milestone": "Scale operations"},
    ])
    
    requests = [
        create_textbox(slide_id, "road_header", "Roadmap", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
    ]
    
    y_pos = 1.4
    for i, item in enumerate(roadmap[:5]):
        if isinstance(item, dict):
            phase = item.get("phase", f"Phase {i+1}")
            milestone = item.get("milestone", "Milestone")
        else:
            phase, milestone = f"Phase {i+1}", str(item)
        requests.append(create_textbox(slide_id, f"road_phase_{i}", phase, inch(0.5), inch(y_pos), inch(1.5), inch(0.4),
                                       FONT["body"], COLORS["primary"], bold=True))
        requests.append(create_textbox(slide_id, f"road_mile_{i}", milestone, inch(2.2), inch(y_pos), inch(7.3), inch(0.5),
                                       FONT["body"], COLORS["dark"]))
        y_pos += 0.7
    return requests


def build_ask_content(slide_id, content):
    """Build investment ask slide content requests."""
    ask_amount = content.get("ask_amount", "$2M")
    use_of_funds = content.get("use_of_funds", [
        {"category": "Product", "percentage": "40%"},
        {"category": "Sales", "percentage": "35%"},
        {"category": "Operations", "percentage": "25%"},
    ])
    contact_email = content.get("contact_email", "contact@company.com")
    
    funds_text = "Use of Funds:\n"
    for item in use_of_funds[:4]:
        if isinstance(item, dict):
            cat = item.get("category", "Category")
            pct = item.get("percentage", "25%")
            funds_text += f"\n• {cat}: {pct}"
        else:
            funds_text += f"\n• {item}"
    
    return [
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": COLORS["dark"]}}}},
            "fields": "pageBackgroundFill.solidFill.color"
        }},
        create_textbox(slide_id, "ask_header", "Investment Ask", inch(0.5), inch(0.3), inch(9), inch(0.7),
                      FONT["heading"], COLORS["white"], bold=True),
        create_textbox(slide_id, "ask_amount", ask_amount, inch(0.5), inch(1.1), inch(9), inch(1),
                      FONT["metric_large"], COLORS["accent"], bold=True, align="CENTER"),
        create_textbox(slide_id, "ask_label", "Seed Round", inch(0.5), inch(2.1), inch(9), inch(0.4),
                      FONT["subheading"], COLORS["light"], align="CENTER"),
        create_textbox(slide_id, "ask_funds", funds_text, inch(0.5), inch(2.8), inch(5), inch(2),
                      FONT["small"], COLORS["light"], line_spacing=150),
        create_textbox(slide_id, "ask_contact", f"Contact: {contact_email}", inch(0.5), inch(5), inch(9), inch(0.4),
                      FONT["small"], COLORS["gray"], align="CENTER"),
    ]


def build_references_content(slide_id, content):
    """Build references/sources slide content requests."""
    references = content.get("references", [])
    
    # Default references if none provided
    if not references:
        references = [
            {"category": "Market Size", "source": "[Source name]", "url": "[URL]"},
            {"category": "Industry Growth", "source": "[Source name]", "url": "[URL]"},
            {"category": "Competitor Data", "source": "[Source name]", "url": "[URL]"},
        ]
    
    # Build reference list text
    ref_text = ""
    for i, ref in enumerate(references[:12], 1):  # Limit to 12 references
        if isinstance(ref, dict):
            category = ref.get("category", "Data")
            source = ref.get("source", "[Source]")
            url = ref.get("url", "")
            if url and url != "[URL]":
                ref_text += f"{i}. {category}: {source}\n   {url}\n\n"
            else:
                ref_text += f"{i}. {category}: {source}\n\n"
        else:
            ref_text += f"{i}. {ref}\n\n"
    
    return [
        create_textbox(slide_id, "ref_header", "Sources & References", inch(0.5), inch(0.3), inch(9), inch(0.7),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "ref_subtitle", "Market data and assumptions are based on the following sources:", 
                      inch(0.5), inch(0.9), inch(9), inch(0.4),
                      FONT["small"], COLORS["gray"]),
        create_textbox(slide_id, "ref_list", ref_text, inch(0.5), inch(1.4), inch(9), inch(3.8),
                      FONT["small"], COLORS["dark"], line_spacing=120),
        create_textbox(slide_id, "ref_note", "Full source details available in Financial Model: Sources & References sheet", 
                      inch(0.5), inch(5.1), inch(9), inch(0.3),
                      FONT["small"], COLORS["gray"], align="CENTER"),
    ]


def build_executive_summary_content(slide_id, content):
    """Build executive summary slide content requests."""
    summary_points = content.get("executive_summary", [
        "Company description",
        "Problem and solution",
        "Market opportunity",
        "Traction highlights"
    ])
    bullet_text = "\n".join([f"• {p}" for p in summary_points[:6]])
    return [
        create_textbox(slide_id, "exec_header", "Executive Summary", inch(0.5), inch(0.3), inch(9), inch(0.8),
                      FONT["heading"], COLORS["dark"], bold=True),
        create_textbox(slide_id, "exec_bullets", bullet_text, inch(0.5), inch(1.3), inch(9), inch(3.8),
                      FONT["body"], COLORS["dark"], line_spacing=180),
    ]


# =============================================================================
# FINANCIAL MODEL INTEGRATION
# =============================================================================

def load_financial_data(spreadsheet_url):
    """Load financial data from Google Sheets financial model."""
    creds = get_credentials()
    gc = gspread.authorize(creds)
    
    # Extract ID from URL
    if "spreadsheets/d/" in spreadsheet_url:
        spreadsheet_id = spreadsheet_url.split("spreadsheets/d/")[1].split("/")[0]
    else:
        spreadsheet_id = spreadsheet_url
    
    spreadsheet = gc.open_by_key(spreadsheet_id)
    data = {}
    
    # Try Pitch Deck Data sheet
    try:
        sheet = spreadsheet.worksheet("Pitch Deck Data")
        values = sheet.get_all_values()
        
        for row in values:
            if len(row) >= 3 and row[0] and row[2]:
                key = row[0].lower().replace(" ", "_").replace("{{", "").replace("}}", "")
                val = row[2] if row[2] else row[1]
                if key and val:
                    data[key] = val
    except:
        pass
    
    # Try P&L sheet for direct values
    try:
        pnl = spreadsheet.worksheet("P&L")
        pnl_data = pnl.get_all_values()
        
        if len(pnl_data) > 1:
            # Row 2 is Revenue (index 1), columns C-L are Years 1-10
            if len(pnl_data[1]) > 2:
                data["revenue_y1"] = format_currency(pnl_data[1][2])
            if len(pnl_data[1]) > 6:
                data["revenue_y5"] = format_currency(pnl_data[1][6])
            if len(pnl_data[1]) > 11:
                data["revenue_y10"] = format_currency(pnl_data[1][11])
            
            # EBITDA is typically row 6 (index 5)
            if len(pnl_data) > 5:
                if len(pnl_data[5]) > 2:
                    data["ebitda_y1"] = format_currency(pnl_data[5][2])
                if len(pnl_data[5]) > 6:
                    data["ebitda_y5"] = format_currency(pnl_data[5][6])
    except Exception as e:
        print(f"  Warning: Could not read P&L sheet: {e}")
    
    print(f"  Loaded {len(data)} data points from financial model")
    return data, spreadsheet_id


def format_currency(value):
    """Format a value as currency string."""
    try:
        num = float(str(value).replace("$", "").replace(",", ""))
        if num >= 1_000_000_000:
            return f"${num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"${num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"${num/1_000:.0f}K"
        else:
            return f"${num:,.0f}"
    except:
        return str(value)


def create_charts_in_spreadsheet(spreadsheet_id):
    """Create charts in the financial model spreadsheet for embedding into pitch deck."""
    creds = get_credentials()
    sheets_service = build("sheets", "v4", credentials=creds)
    
    # Get spreadsheet info
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_ids = {}
    for sheet in spreadsheet["sheets"]:
        sheet_ids[sheet["properties"]["title"]] = sheet["properties"]["sheetId"]
        # Check if charts already exist on this sheet
        if "charts" in sheet:
            for chart in sheet["charts"]:
                print(f"  Found existing chart (ID: {chart['chartId']}) on {sheet['properties']['title']}")
                return {"revenue_chart_id": chart["chartId"], "spreadsheet_id": spreadsheet_id}
    
    # Find the Pitch Deck Data sheet or P&L sheet
    chart_sheet_id = sheet_ids.get("Pitch Deck Data") or sheet_ids.get("P&L")
    if not chart_sheet_id:
        print("  Warning: No suitable sheet found for charts")
        return {}
    
    # First, expand the sheet if needed (add rows for chart placement)
    try:
        expand_request = {
            "requests": [{
                "appendDimension": {
                    "sheetId": chart_sheet_id,
                    "dimension": "ROWS",
                    "length": 20
                }
            }]
        }
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=expand_request).execute()
    except:
        pass  # Sheet may already have enough rows
    
    # Create Revenue chart - using Pitch Deck Data sheet if available
    pitch_data_id = sheet_ids.get("Pitch Deck Data")
    pnl_sheet_id = sheet_ids.get("P&L")
    
    # Use Pitch Deck Data for chart data (rows 3-12 have Year 1-10 data in columns A-D)
    if pitch_data_id:
        chart_request = {
            "requests": [{
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Revenue & EBITDA (10-Year Projection)",
                            "basicChart": {
                                "chartType": "COMBO",
                                "legendPosition": "BOTTOM_LEGEND",
                                "axis": [
                                    {"position": "BOTTOM_AXIS", "title": "Year"},
                                    {"position": "LEFT_AXIS", "title": "Amount ($)"}
                                ],
                                "domains": [{
                                    "domain": {
                                        "sourceRange": {
                                            "sources": [{
                                                "sheetId": pitch_data_id,
                                                "startRowIndex": 2, "endRowIndex": 12,  # Year 1-10
                                                "startColumnIndex": 0, "endColumnIndex": 1  # Column A (Year labels)
                                            }]
                                        }
                                    }
                                }],
                                "series": [
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [{
                                                    "sheetId": pitch_data_id,
                                                    "startRowIndex": 2, "endRowIndex": 12,
                                                    "startColumnIndex": 1, "endColumnIndex": 2  # Column B (Revenue)
                                                }]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS",
                                        "type": "COLUMN",
                                        "color": {"red": 0.13, "green": 0.59, "blue": 0.95}
                                    },
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [{
                                                    "sheetId": pitch_data_id,
                                                    "startRowIndex": 2, "endRowIndex": 12,
                                                    "startColumnIndex": 2, "endColumnIndex": 3  # Column C (EBITDA)
                                                }]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS",
                                        "type": "LINE",
                                        "color": {"red": 0.0, "green": 0.78, "blue": 0.62}
                                    }
                                ],
                                "headerCount": 0
                            }
                        },
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {"sheetId": pitch_data_id, "rowIndex": 55, "columnIndex": 0},
                                "widthPixels": 800,
                                "heightPixels": 400
                            }
                        }
                    }
                }
            }]
        }
    elif pnl_sheet_id:
        # Fallback to P&L sheet
        chart_request = {
            "requests": [{
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Revenue & EBITDA Projections",
                            "basicChart": {
                                "chartType": "COMBO",
                                "legendPosition": "BOTTOM_LEGEND",
                                "axis": [
                                    {"position": "BOTTOM_AXIS", "title": "Year"},
                                    {"position": "LEFT_AXIS", "title": "Amount ($)"}
                                ],
                                "domains": [{
                                    "domain": {
                                        "sourceRange": {
                                            "sources": [{
                                                "sheetId": pnl_sheet_id,
                                                "startRowIndex": 0, "endRowIndex": 1,
                                                "startColumnIndex": 1, "endColumnIndex": 12
                                            }]
                                        }
                                    }
                                }],
                                "series": [
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [{
                                                    "sheetId": pnl_sheet_id,
                                                    "startRowIndex": 1, "endRowIndex": 2,
                                                    "startColumnIndex": 1, "endColumnIndex": 12
                                                }]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS",
                                        "type": "COLUMN",
                                        "color": {"red": 0.13, "green": 0.59, "blue": 0.95}
                                    },
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [{
                                                    "sheetId": pnl_sheet_id,
                                                    "startRowIndex": 3, "endRowIndex": 4,
                                                    "startColumnIndex": 1, "endColumnIndex": 12
                                                }]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS",
                                        "type": "LINE",
                                        "color": {"red": 0.0, "green": 0.78, "blue": 0.62}
                                    }
                                ],
                                "headerCount": 1
                            }
                        },
                        "position": {
                            "newSheet": True  # Create chart on a new sheet
                        }
                    }
                }
            }]
        }
    else:
        return {}
    
    try:
        response = sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=chart_request
        ).execute()
        chart_id = response["replies"][0]["addChart"]["chart"]["chartId"]
        print(f"  Created revenue chart (ID: {chart_id})")
        return {"revenue_chart_id": chart_id, "spreadsheet_id": spreadsheet_id}
    except Exception as e:
        print(f"  Warning: Could not create chart: {e}")
        return {}


# =============================================================================
# MAIN PITCH DECK CREATION
# =============================================================================

def create_pitch_deck(company_name, content, deck_type="startup", financial_model_url=None):
    """
    Create a pitch deck from scratch with proper formatting.
    
    Args:
        company_name: Name of the company
        content: Dictionary with pitch deck content
        deck_type: Type of deck (minimal, seed, startup, investor, series_a, full)
        financial_model_url: Optional URL to Google Sheets financial model
        
    Returns:
        Dictionary with presentation_id, title, url
    """
    creds = get_credentials()
    slides_service = build("slides", "v1", credentials=creds)
    
    # Load financial data if provided
    chart_info = None
    if financial_model_url:
        print(f"\n Loading financial data from spreadsheet...")
        financial_data, spreadsheet_id = load_financial_data(financial_model_url)
        
        # Merge financial data into content
        for key, value in financial_data.items():
            if key not in content or not content[key]:
                content[key] = value
        
        # Create charts for embedding
        print("  Creating charts in spreadsheet...")
        chart_info = create_charts_in_spreadsheet(spreadsheet_id)
    
    # Add company name to content
    content["company_name"] = company_name
    
    # Get slide sequence for this deck type
    slides_to_create = DECK_TYPES.get(deck_type, DECK_TYPES["startup"])
    
    print(f"\n Creating {deck_type.upper()} pitch deck for {company_name}")
    print(f"   Slides: {', '.join(slides_to_create)}")
    
    # Create presentation
    presentation = slides_service.presentations().create(
        body={"title": f"{company_name} - Pitch Deck"}
    ).execute()
    presentation_id = presentation["presentationId"]
    
    # Delete default blank slide
    default_slides = presentation.get("slides", [])
    if default_slides:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": [{"deleteObject": {"objectId": default_slides[0]["objectId"]}}]}
        ).execute()
    
    # Build ALL slide requests in one batch to reduce API calls
    print("   Building all slides...")
    all_requests = []
    slide_ids = []
    
    # First, create all blank slides
    for i, slide_type in enumerate(slides_to_create):
        slide_id = f"slide_{i}_{slide_type}"
        slide_ids.append((slide_type, slide_id))
        all_requests.append({
            "createSlide": {
                "objectId": slide_id,
                "slideLayoutReference": {"predefinedLayout": "BLANK"}
            }
        })
    
    # Execute slide creation in one batch
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": all_requests}
    ).execute()
    
    # Now build content for each slide
    content_builders = {
        "title": build_title_content,
        "executive_summary": build_executive_summary_content,
        "problem": build_problem_content,
        "solution": build_solution_content,
        "product": build_product_content,
        "market": build_market_content,
        "tam_sam_som": build_tam_sam_som_content,
        "competition": build_competition_content,
        "business_model": build_business_model_content,
        "unit_economics": build_unit_economics_content,
        "traction": build_traction_content,
        "team": build_team_content,
        "financials": lambda sid, c: build_financials_content(sid, c, chart_info),
        "projections": lambda sid, c: build_projections_content(sid, c, chart_info),
        "roadmap": build_roadmap_content,
        "ask": build_ask_content,
        "references": build_references_content,
    }
    
    all_content_requests = []
    for slide_type, slide_id in slide_ids:
        builder = content_builders.get(slide_type)
        if builder:
            requests = builder(slide_id, content)
            all_content_requests.extend(flatten(requests))
    
    # Execute all content in batches of 50 requests (to avoid hitting limits)
    print(f"   Adding content ({len(all_content_requests)} requests)...")
    batch_size = 50
    for i in range(0, len(all_content_requests), batch_size):
        batch = all_content_requests[i:i + batch_size]
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": batch}
        ).execute()
        if i + batch_size < len(all_content_requests):
            import time
            time.sleep(1)  # Small delay between batches
    
    url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    
    print(f"\n Pitch deck created successfully!")
    print(f"   URL: {url}")
    print(f"   Total slides: {len(slides_to_create)}")
    
    return {
        "presentation_id": presentation_id,
        "title": f"{company_name} - Pitch Deck",
        "url": url,
        "slides": slides_to_create,
        "total_slides": len(slides_to_create)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Create professional pitch decks from scratch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_pitch_deck.py --company "MyStartup" --content-file content.json
  python create_pitch_deck.py --company "MyStartup" --type investor --financial-model "SHEET_URL"
  python create_pitch_deck.py --company "MyStartup" --type minimal

Deck types:
  minimal   - 5 slides: title, problem, solution, market, ask
  seed      - 7 slides: + business_model, traction
  startup   - 10 slides: + product, team, financials
  investor  - 12 slides: + competition, roadmap
  series_a  - 14 slides: + executive_summary, projections
  full      - 16 slides: + tam_sam_som, unit_economics
        """
    )
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--type", choices=list(DECK_TYPES.keys()), default="startup", help="Deck type")
    parser.add_argument("--content-file", help="JSON file with pitch content")
    parser.add_argument("--financial-model", help="Google Sheets URL of financial model")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--copilot", action="store_true", help="JSON output for Copilot")
    
    args = parser.parse_args()
    
    # Load content
    content = {}
    if args.content_file and os.path.exists(args.content_file):
        with open(args.content_file, "r", encoding="utf-8-sig") as f:
            content = json.load(f)
    
    # Create pitch deck
    result = create_pitch_deck(
        company_name=args.company,
        content=content,
        deck_type=args.type,
        financial_model_url=args.financial_model
    )
    
    if args.copilot:
        print(json.dumps(result, indent=2))
    
    if args.output:
        with open(args.output, "w", encoding="ascii") as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
