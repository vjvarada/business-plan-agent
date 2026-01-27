#!/usr/bin/env python3
"""
Market research using SerpAPI - search Google, analyze competitors, track trends.
Part of the Business Planning Agent toolkit.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

try:
    from serpapi import GoogleSearch
except ImportError:
    print("Installing serpapi...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-search-results"])
    from serpapi import GoogleSearch

load_dotenv()


def search_market(query, num_results=10, location="United States", language="en"):
    """
    Perform a Google search for market research.
    
    Args:
        query: Search query
        num_results: Number of results to return
        location: Geographic location for search
        language: Language code
        
    Returns:
        Dictionary with search results
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "location": location,
        "hl": language
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract organic results
    organic_results = []
    for result in results.get("organic_results", []):
        organic_results.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet"),
            "position": result.get("position")
        })
    
    # Extract related questions (People Also Ask)
    related_questions = []
    for question in results.get("related_questions", []):
        related_questions.append({
            "question": question.get("question"),
            "snippet": question.get("snippet")
        })
    
    return {
        "query": query,
        "total_results": results.get("search_information", {}).get("total_results"),
        "organic_results": organic_results,
        "related_questions": related_questions,
        "timestamp": datetime.now().isoformat()
    }


def analyze_competitors(company_name, industry=None, num_results=20):
    """
    Analyze competitors for a given company or industry.
    
    Args:
        company_name: Name of the company
        industry: Optional industry context
        num_results: Number of results
        
    Returns:
        Dictionary with competitor analysis
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    
    # Search for competitors
    query = f"{company_name} competitors"
    if industry:
        query = f"{company_name} competitors {industry}"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    competitors = []
    for result in results.get("organic_results", []):
        competitors.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        })
    
    # Also search for market share
    market_query = f"{industry or company_name} market share analysis"
    params["q"] = market_query
    market_search = GoogleSearch(params)
    market_results = market_search.get_dict()
    
    market_insights = []
    for result in market_results.get("organic_results", [])[:5]:
        market_insights.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        })
    
    return {
        "company": company_name,
        "industry": industry,
        "competitors": competitors,
        "market_insights": market_insights,
        "timestamp": datetime.now().isoformat()
    }


def get_industry_trends(industry, timeframe="today 12-m"):
    """
    Get industry trends using Google Trends.
    
    Args:
        industry: Industry or keyword to track
        timeframe: Time range (today 12-m, today 3-m, today 1-m)
        
    Returns:
        Dictionary with trend data
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    
    params = {
        "engine": "google_trends",
        "q": industry,
        "api_key": api_key,
        "date": timeframe,
        "data_type": "TIMESERIES"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    interest_over_time = results.get("interest_over_time", {})
    timeline_data = interest_over_time.get("timeline_data", [])
    
    trend_points = []
    for point in timeline_data:
        trend_points.append({
            "date": point.get("date"),
            "values": point.get("values", [])
        })
    
    # Get related queries
    params["data_type"] = "RELATED_QUERIES"
    related_search = GoogleSearch(params)
    related_results = related_search.get_dict()
    
    related_queries = {
        "rising": related_results.get("related_queries", {}).get("rising", []),
        "top": related_results.get("related_queries", {}).get("top", [])
    }
    
    return {
        "industry": industry,
        "timeframe": timeframe,
        "trend_data": trend_points,
        "related_queries": related_queries,
        "timestamp": datetime.now().isoformat()
    }


def search_news(query, num_results=10):
    """
    Search for news articles related to a topic.
    
    Args:
        query: Search query
        num_results: Number of results
        
    Returns:
        Dictionary with news results
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    news_results = []
    for article in results.get("news_results", []):
        news_results.append({
            "title": article.get("title"),
            "link": article.get("link"),
            "source": article.get("source", {}).get("name"),
            "date": article.get("date"),
            "snippet": article.get("snippet")
        })
    
    return {
        "query": query,
        "news_results": news_results,
        "timestamp": datetime.now().isoformat()
    }


def extract_market_sources(industry: str, num_results: int = 5) -> dict:
    """
    Extract and format market data sources for financial model.
    Performs multiple searches to gather TAM/SAM/SOM and industry metrics.
    
    Args:
        industry: Industry name/description
        num_results: Number of results per search
        
    Returns:
        Dictionary formatted for financial model Sources sheet
    """
    sources = {
        'retrieval_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Search for TAM
    try:
        tam_results = search_market(f"{industry} market size TAM total addressable market", num_results)
        if tam_results.get('organic_results'):
            top = tam_results['organic_results'][0]
            sources['tam_source'] = top.get('title', '')
            sources['tam_url'] = top.get('link', '')
            sources['tam_value'] = top.get('snippet', '')[:200] if top.get('snippet') else ''
    except Exception as e:
        print(f"Warning: TAM search failed: {e}")
    
    # Search for industry growth rate
    try:
        growth_results = search_market(f"{industry} industry growth rate CAGR forecast", num_results)
        if growth_results.get('organic_results'):
            top = growth_results['organic_results'][0]
            sources['growth_rate_source'] = top.get('title', '')
            sources['growth_rate_url'] = top.get('link', '')
            sources['growth_rate_value'] = top.get('snippet', '')[:200] if top.get('snippet') else ''
    except Exception as e:
        print(f"Warning: Growth rate search failed: {e}")
    
    # Search for CAC benchmarks
    try:
        cac_results = search_market(f"{industry} customer acquisition cost CAC benchmark average", num_results)
        if cac_results.get('organic_results'):
            top = cac_results['organic_results'][0]
            sources['cac_benchmark_source'] = top.get('title', '')
            sources['cac_benchmark_url'] = top.get('link', '')
            sources['cac_benchmark_value'] = top.get('snippet', '')[:200] if top.get('snippet') else ''
    except Exception as e:
        print(f"Warning: CAC benchmark search failed: {e}")
    
    # Search for pricing benchmarks
    try:
        pricing_results = search_market(f"{industry} pricing benchmark average price", num_results)
        if pricing_results.get('organic_results'):
            top = pricing_results['organic_results'][0]
            sources['price_source'] = top.get('title', '')
            sources['price_url'] = top.get('link', '')
            sources['price_value'] = top.get('snippet', '')[:200] if top.get('snippet') else ''
    except Exception as e:
        print(f"Warning: Pricing search failed: {e}")
    
    # Search for LTV:CAC benchmarks
    try:
        ltv_results = search_market(f"{industry} LTV CAC ratio benchmark unit economics", num_results)
        if ltv_results.get('organic_results'):
            top = ltv_results['organic_results'][0]
            sources['ltv_cac_benchmark_source'] = top.get('title', '')
            sources['ltv_cac_benchmark_url'] = top.get('link', '')
            sources['ltv_cac_benchmark_value'] = top.get('snippet', '')[:200] if top.get('snippet') else ''
    except Exception as e:
        print(f"Warning: LTV:CAC search failed: {e}")
    
    # Get industry news
    try:
        news_results = search_news(f"{industry} industry news", num_results=3)
        if news_results.get('news_results'):
            for i, article in enumerate(news_results['news_results'][:2], 1):
                sources[f'news{i}_title'] = article.get('title', '')
                sources[f'news{i}_source'] = article.get('source', '')
                sources[f'news{i}_url'] = article.get('link', '')
    except Exception as e:
        print(f"Warning: News search failed: {e}")
    
    return sources


def compile_research_report(industry: str, company_name: str | None = None) -> dict:
    """
    Compile a comprehensive research report with all sources.
    
    Args:
        industry: Industry name/description
        company_name: Optional company name for competitor analysis
        
    Returns:
        Dictionary with full research report and sources
    """
    report = {
        'industry': industry,
        'company_name': company_name,
        'timestamp': datetime.now().isoformat(),
        'sources': extract_market_sources(industry),
        'research': {}
    }
    
    # Get market overview
    try:
        market_research = search_market(f"{industry} market overview size trends", 10)
        report['research']['market_overview'] = market_research
    except Exception as e:
        print(f"Warning: Market overview search failed: {e}")
    
    # Get competitor analysis if company name provided
    if company_name:
        try:
            competitors = analyze_competitors(company_name, industry, 10)
            report['research']['competitors'] = competitors
            
            # Add competitor sources
            if competitors.get('top_competitors'):
                for i, comp in enumerate(competitors['top_competitors'][:3], 1):
                    report['sources'][f'competitor{i}_name'] = comp.get('name', '')
                    report['sources'][f'competitor{i}_info'] = comp.get('description', '')[:200] if comp.get('description') else ''
                    report['sources'][f'competitor{i}_url'] = comp.get('link', '')
        except Exception as e:
            print(f"Warning: Competitor analysis failed: {e}")
    
    # Get industry trends
    try:
        trends = get_industry_trends(industry, 'today 12-m')
        report['research']['trends'] = trends
    except Exception as e:
        print(f"Warning: Trends search failed: {e}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Market Research with SerpAPI')
    parser.add_argument('--mode', required=True,
                        choices=['search', 'competitors', 'trends', 'news', 'sources', 'full-report'],
                        help='Research mode')
    parser.add_argument('--query', required=True, help='Search query or company name')
    parser.add_argument('--industry', help='Industry context (for competitor analysis)')
    parser.add_argument('--num-results', type=int, default=10, help='Number of results')
    parser.add_argument('--location', default='United States', help='Geographic location')
    parser.add_argument('--timeframe', default='today 12-m',
                        help='Timeframe for trends (today 12-m, today 3-m, today 1-m)')
    parser.add_argument('--output', help='Output JSON file path')

    args = parser.parse_args()

    try:
        if args.mode == 'search':
            result = search_market(
                query=args.query,
                num_results=args.num_results,
                location=args.location
            )
        elif args.mode == 'competitors':
            result = analyze_competitors(
                company_name=args.query,
                industry=args.industry,
                num_results=args.num_results
            )
        elif args.mode == 'trends':
            result = get_industry_trends(
                industry=args.query,
                timeframe=args.timeframe
            )
        elif args.mode == 'news':
            result = search_news(
                query=args.query,
                num_results=args.num_results
            )
        elif args.mode == 'sources':
            # Extract sources for financial model
            result = extract_market_sources(
                industry=args.query,
                num_results=args.num_results
            )
        elif args.mode == 'full-report':
            # Full research report with all sources
            result = compile_research_report(
                industry=args.query,
                company_name=args.industry  # Use industry arg as company name
            )

        print(json.dumps(result, indent=2))

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResult saved to: {args.output}")

        return result

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()