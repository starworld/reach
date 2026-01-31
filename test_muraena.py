#!/usr/bin/env python3
"""
Muraena API 動作確認テスト
API Key: 26436f1d1d93438a24321ef9627f16047c775c3d
"""

import os
import json
import asyncio
import httpx
from typing import Optional, List

API_KEY = "26436f1d1d93438a24321ef9627f16047c775c3d"
BASE_URL = "https://app.muraena.ai/api/v1"

class MuraenaClient:
    """Muraena API クライアント"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL
        
    async def search_people(
        self,
        job_titles: Optional[List[str]] = None,
        company_keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        company_size: Optional[str] = None,
        limit: int = 10
    ) -> dict:
        """
        人物検索
        
        日本市場向け検索例:
        - locations: ["Japan", "Tokyo", "Osaka", "Kyoto"]
        - job_titles: ["CEO", "CTO", "VP", "Director"]
        """
        url = f"{self.base_url}/people/search"
        
        payload = {"limit": limit}
        if job_titles:
            payload["jobTitles"] = job_titles
        if company_keywords:
            payload["companyKeywords"] = company_keywords
        if locations:
            payload["locations"] = locations
        if industries:
            payload["industries"] = industries
        if company_size:
            payload["companySize"] = company_size
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def reveal_contact(
        self,
        linkedin_url: Optional[str] = None,
        muraena_id: Optional[str] = None
    ) -> dict:
        """
        連絡先情報取得（1リクエスト = 1クレジット）
        
        メールが取得できない場合、クレジットは返還される
        """
        url = f"{self.base_url}/people/reveal"
        
        payload = {}
        if linkedin_url:
            payload["linkedinUrl"] = linkedin_url
        if muraura_id:
            payload["id"] = muraena_id
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_company_filters(self) -> dict:
        """利用可能な検索フィルタ一覧を取得"""
        url = f"{self.base_url}/filters"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()


async def test_api_connection():
    """API接続テスト"""
    print("=" * 60)
    print("🔌 Testing API Connection")
    print("=" * 60)
    
    client = MuraenaClient(API_KEY)
    
    try:
        # シンプルな検索で接続確認
        result = await client.search_people(
            locations=["Japan"],
            limit=1
        )
        print("✅ API Connection: SUCCESS")
        print(f"   Response keys: {list(result.keys())}")
        return True
    except Exception as e:
        print(f"❌ API Connection: FAILED")
        print(f"   Error: {e}")
        return False


async def test_japan_search():
    """日本市場検索テスト"""
    print("\n" + "=" * 60)
    print("🔍 Testing Japan Market Search")
    print("=" * 60)
    
    client = MuraenaClient(API_KEY)
    
    # 日本のテック企業のCXOを検索
    test_cases = [
        {
            "name": "日本のCEO検索",
            "params": {
                "job_titles": ["CEO", "代表取締役"],
                "locations": ["Japan", "Tokyo"],
                "company_keywords": ["technology", "software"],
                "limit": 3
            }
        },
        {
            "name": "日本のCTO検索",
            "params": {
                "job_titles": ["CTO", "技術責任者"],
                "locations": ["Japan", "Osaka", "Kyoto"],
                "limit": 3
            }
        },
        {
            "name": "製造業のVP検索",
            "params": {
                "job_titles": ["VP", "Director"],
                "locations": ["Japan"],
                "industries": ["manufacturing"],
                "limit": 3
            }
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Params: {json.dumps(test['params'], ensure_ascii=False)}")
        
        try:
            result = await client.search_people(**test['params'])
            
            # 結果解析
            total = result.get('total', 0)
            profiles = result.get('profiles', [])
            
            print(f"   ✅ Success")
            print(f"   Total results: {total}")
            print(f"   Returned: {len(profiles)}")
            
            if profiles:
                print(f"\n   Sample profile:")
                sample = profiles[0]
                print(f"   - Name: {sample.get('firstName', '')} {sample.get('lastName', '')}")
                print(f"   - Title: {sample.get('jobTitle', 'N/A')}")
                print(f"   - Company: {sample.get('companyName', 'N/A')}")
                print(f"   - Location: {sample.get('location', 'N/A')}")
                print(f"   - LinkedIn: {sample.get('linkedinUrl', 'N/A')[:50]}...")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")


async def test_filters():
    """検索フィルタ一覧取得"""
    print("\n" + "=" * 60)
    print("📋 Testing Get Filters")
    print("=" * 60)
    
    client = MuraenaClient(API_KEY)
    
    try:
        result = await client.get_company_filters()
        print("✅ Filters retrieved")
        print(f"   Available filters: {list(result.keys())}")
        
        # 業種一覧
        if 'industries' in result:
            industries = result['industries']
            print(f"\n   Industries ({len(industries)} total):")
            for ind in industries[:10]:
                print(f"   - {ind}")
            if len(industries) > 10:
                print(f"   ... and {len(industries) - 10} more")
                
    except Exception as e:
        print(f"❌ Failed: {e}")


async def test_reveal():
    """連絡先取得テスト（クレジット消費注意）"""
    print("\n" + "=" * 60)
    print("👤 Testing Contact Reveal (Credit Usage)")
    print("=" * 60)
    print("⚠️  This will consume 1 credit")
    print("Skipping in automated test")
    print("To test manually, uncomment the code below")
    
    # 手動テスト時のみ有効化
    # client = MuraenaClient(API_KEY)
    # result = await client.reveal_contact(
    #     linkedin_url="https://www.linkedin.com/in/example"
    # )
    # print(result)


async def main():
    """全テスト実行"""
    print("=" * 60)
    print("🚀 Muraena API Test Suite")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Base URL: {BASE_URL}")
    
    # 接続テスト
    connected = await test_api_connection()
    
    if connected:
        # 日本市場検索テスト
        await test_japan_search()
        
        # フィルタ取得
        await test_filters()
        
        # 連絡先取得（手動時のみ）
        await test_reveal()
    else:
        print("\n❌ Cannot proceed with tests - API connection failed")
    
    print("\n" + "=" * 60)
    print("✅ Test completed")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
