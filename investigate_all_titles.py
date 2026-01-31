#!/usr/bin/env python3
"""
全役職名の効率的調査スクリプト
"""

import httpx
import asyncio
import json
from typing import List, Dict

API_KEY = "26436f1d1d93438a24321ef9627f16047c775c3d"

# 調査する役職名リスト
TITLES_TO_INVESTIGATE = {
    # C-Level (英語)
    "c_level_english": [
        "CEO", "CTO", "CFO", "COO", "CMO", "CHRO", "CIO", "CDO", "CPO", "CCO",
        "Chief Executive Officer", "Chief Technology Officer", "Chief Financial Officer",
        "Chief Operating Officer", "Chief Marketing Officer", "Chief Human Resources Officer",
        "Chief Information Officer", "Chief Digital Officer", "Chief Product Officer",
    ],
    
    # VPレベル
    "vp_level": [
        "VP", "Vice President", "SVP", "Senior Vice President", "EVP", "Executive Vice President",
        "AVP", "Assistant Vice President",
    ],
    
    # ディレクターレベル
    "director_level": [
        "Director", "Senior Director", "Executive Director", "Managing Director",
        "Regional Director", "Global Director", "Associate Director",
    ],
    
    # マネージャーレベル
    "manager_level": [
        "Manager", "Senior Manager", "General Manager", "District Manager",
        "Regional Manager", "Product Manager", "Project Manager", "Account Manager",
    ],
    
    # ヘッド・リード系
    "head_lead": [
        "Head of", "Head", "Lead", "Team Lead", "Technical Lead",
        "Head of Sales", "Head of Engineering", "Head of Marketing",
    ],
    
    # プレジデント・オフィサー系
    "president_officer": [
        "President", "Vice President", "Officer", "Executive Officer",
        "Managing Officer", "Senior Officer",
    ],
    
    # プロフェッショナル
    "professional": [
        "Partner", "Principal", "Associate", "Consultant", "Advisor",
        "Specialist", "Analyst", "Researcher", "Scientist",
    ],
    
    # 技術職
    "technical": [
        "Engineer", "Senior Engineer", "Staff Engineer", "Principal Engineer",
        "Software Engineer", "Developer", "Programmer", "Architect",
        "Data Scientist", "ML Engineer", "DevOps Engineer", "Security Engineer",
    ],
    
    # 営業職
    "sales": [
        "Sales", "Sales Representative", "Sales Executive", "Account Executive",
        "Business Development", "BD", "Sales Manager", "Sales Director",
        "Account Manager", "Key Account Manager", "Sales Engineer",
    ],
    
    # マーケティング
    "marketing": [
        "Marketing", "Marketing Manager", "Marketing Director",
        "Product Marketing", "Growth", "Growth Hacker", "Digital Marketing",
        "Brand Manager", "Content Manager", "SEO", "SEM",
    ],
    
    # 人事
    "hr": [
        "HR", "Human Resources", "HR Manager", "HR Director", "HRBP",
        "Recruiter", "Talent Acquisition", "People Operations",
        "Training", "L&D", "Learning and Development",
    ],
    
    # 財務・経理
    "finance": [
        "Finance", "Financial Analyst", "Accountant", "Controller",
        "Treasury", "Audit", "Tax", "FP&A",
    ],
    
    # 法務
    "legal": [
        "Legal", "General Counsel", "Attorney", "Lawyer", "Compliance",
        "Legal Counsel", "Corporate Counsel",
    ],
    
    # 購買・調達
    "procurement": [
        "Procurement", "Purchasing", "Sourcing", "Buyer", "Supply Chain",
        "Category Manager", "Vendor Manager",
    ],
    
    # 日本語役職
    "japanese_executive": [
        "社長", "代表取締役", "取締役", "会長", "副会長",
        "専務", "常務", "監査役",
    ],
    
    "japanese_management": [
        "本部長", "部長", "課長", "係長", "主任", "主査",
        "チームリーダー", "マネージャー", "リーダー",
    ],
    
    "japanese_chief": [
        "チーフ", "責任者", "担当", "主管", "主幹",
    ],
    
    # 日本語職種
    "japanese_engineer": [
        "技術部長", "技術課長", "技術担当", "エンジニア", "技術者",
        "開発部長", "開発課長", "開発担当",
        "研究部長", "研究課長", "研究者",
    ],
    
    "japanese_sales": [
        "営業部長", "営業課長", "営業担当", "営業",
        "セールス", "セールスマネージャー",
    ],
    
    # コンサル・監査
    "consulting_audit": [
        "Consultant", "Senior Consultant", "Managing Consultant",
        "Auditor", "Audit Manager", "CPA", "税理士",
    ],
    
    # オペレーション
    "operations": [
        "Operations", "Operations Manager", "Operations Director",
        "Plant Manager", "Factory Manager", "Production Manager",
    ],
    
    # 研究者・アカデミック
    "research_academic": [
        "Researcher", "Research Scientist", "Research Fellow",
        "Professor", "Associate Professor", "Lecturer",
        "Postdoc", "PhD",
    ],
    
    # その他
    "other": [
        "Founder", "Co-Founder", "Entrepreneur",
        "Investor", "Angel Investor", "VC",
        "Board Member", "Advisor", "Mentor",
    ],
}


async def check_title(client: httpx.AsyncClient, title: str) -> Dict:
    """単一の役職名をチェック"""
    try:
        resp = await client.post(
            'https://contacts.muraena.ai/api/client_api/search/',
            headers={'Authorization': f'Token {API_KEY}'},
            json={'person_job_titles': [title], 'limit': 1},
            timeout=10.0
        )
        data = resp.json()
        count = data.get('count', 0)
        return {
            'title': title,
            'count': count,
            'available': count > 0,
            'error': None
        }
    except Exception as e:
        return {
            'title': title,
            'count': 0,
            'available': False,
            'error': str(e)
        }


async def investigate_category(client: httpx.AsyncClient, category: str, titles: List[str]) -> List[Dict]:
    """カテゴリー内の全役職をチェック（レート制限対策で逐次処理）"""
    results = []
    print(f"\n🔍 Checking {category} ({len(titles)} titles)...")
    
    for i, title in enumerate(titles):
        result = await check_title(client, title)
        results.append(result)
        
        if result['available']:
            print(f"  ✅ {title}: {result['count']:,}")
        
        # レート制限対策（6リクエスト/分）
        if (i + 1) % 5 == 0:
            await asyncio.sleep(10)
    
    return results


async def main():
    """全カテゴリーの調査"""
    print("=" * 60)
    print("🔍 Muraena API - 全役職名調査")
    print("=" * 60)
    print(f"Total categories: {len(TITLES_TO_INVESTIGATE)}")
    print(f"Total titles to check: {sum(len(t) for t in TITLES_TO_INVESTIGATE.values())}")
    
    all_results = []
    
    async with httpx.AsyncClient() as client:
        for category, titles in TITLES_TO_INVESTIGATE.items():
            results = await investigate_category(client, category, titles)
            all_results.extend(results)
    
    # 結果集計
    available_titles = [r for r in all_results if r['available']]
    unavailable_titles = [r for r in all_results if not r['available'] and not r['error']]
    error_titles = [r for r in all_results if r['error']]
    
    # 上位20件
    top_titles = sorted(available_titles, key=lambda x: x['count'], reverse=True)[:20]
    
    # 日本語役職
    japanese_available = [r for r in available_titles if any(c in r['title'] for c in 'あ-んア-ン亜-熙')]
    
    print("\n" + "=" * 60)
    print("📊 調査結果サマリー")
    print("=" * 60)
    print(f"総チェック件数: {len(all_results)}")
    print(f"データあり: {len(available_titles)} ({len(available_titles)/len(all_results)*100:.1f}%)")
    print(f"データなし: {len(unavailable_titles)}")
    print(f"エラー: {len(error_titles)}")
    
    print("\n" + "=" * 60)
    print("🏆 TOP 20 役職（件数順）")
    print("=" * 60)
    for i, r in enumerate(top_titles, 1):
        print(f"{i:2d}. {r['title']:40s}: {r['count']:>10,}")
    
    print("\n" + "=" * 60)
    print("🇯🇵 日本語役職（データあり）")
    print("=" * 60)
    if japanese_available:
        for r in sorted(japanese_available, key=lambda x: x['count'], reverse=True):
            print(f"- {r['title']:30s}: {r['count']:>10,}")
    else:
        print("データなし")
    
    # カテゴリー別サマリー
    print("\n" + "=" * 60)
    print("📁 カテゴリー別サマリー")
    print("=" * 60)
    for category in TITLES_TO_INVESTIGATE.keys():
        cat_results = [r for r in all_results if r['title'] in TITLES_TO_INVESTIGATE[category]]
        available = len([r for r in cat_results if r['available']])
        print(f"{category:25s}: {available:3d}/{len(cat_results):3d} 役職でデータあり")
    
    # 詳細結果をJSON保存
    with open('title_investigation_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_checked': len(all_results),
                'available': len(available_titles),
                'unavailable': len(unavailable_titles),
                'errors': len(error_titles),
            },
            'top_20': top_titles,
            'japanese_available': japanese_available,
            'all_available': sorted(available_titles, key=lambda x: x['count'], reverse=True),
        }, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 結果を title_investigation_results.json に保存しました")


if __name__ == "__main__":
    asyncio.run(main())
