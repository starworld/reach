#!/usr/bin/env python3
"""
Muraena API 成功テスト
"""

import httpx
import asyncio
import json

API_KEY = "26436f1d1d93438a24321ef9627f16047c775c3d"
BASE_URL = "https://contacts.muraena.ai/api/client_api"

async def test_search():
    """検索APIテスト"""
    print("=" * 60)
    print("🔍 Muraena API Search Test")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{BASE_URL}/search/",
            headers={
                "Authorization": f"Token {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "person_job_titles": ["CEO"],
                "limit": 2
            }
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        print(f"Total matching profiles: {data.get('count', 0):,}")
        print(f"Returned: {len(data.get('results', []))}")
        print()
        
        if data.get('results'):
            print("=== Sample Profile ===")
            p = data['results'][0]
            print(f"Name: {p.get('person_first_name', '')} {p.get('person_last_name', '')}")
            print(f"Title: {p.get('person_job_title', 'N/A')}")
            print(f"Company: {p.get('company_name', 'N/A')}")
            print(f"Industry: {p.get('company_industry', 'N/A')}")
            print(f"Location: {p.get('person_location', 'N/A')}")
            print(f"LinkedIn: {p.get('person_linkedin_url', 'N/A')}")
            print(f"Company LinkedIn: {p.get('company_linkedin_url', 'N/A')}")
            print()
            
            # 利用可能なフィールド一覧
            print("=== Available Fields ===")
            for key in sorted(p.keys()):
                value = p[key]
                preview = str(value)[:50] if value else "None"
                print(f"  {key}: {preview}")


async def test_filters():
    """利用可能なフィルタ一覧"""
    print("\n" + "=" * 60)
    print("📋 Available Filters")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{BASE_URL}/industries/",
            headers={"Authorization": f"Token {API_KEY}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            industries = data.get('results', [])[:20]
            print(f"Industries ({len(data.get('results', []))} total):")
            for ind in industries:
                print(f"  - {ind}")


async def main():
    await test_search()
    await test_filters()
    
    print("\n" + "=" * 60)
    print("✅ API Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
