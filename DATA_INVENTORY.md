# Muraena API データインベントリ

## APIエンドポイント
```
Base URL: https://contacts.muraena.ai/api/client_api/
Auth: Token {API_KEY}
```

## データ量の実態

### 総プロファイル数
- **謳い文句**: 1.4億プロファイル（140 million）
- **検索可能**: person_job_titlesフィルタ使用時のみ
- **実際に確認できた検索結果**: 約7,000万件（役職別合計）

### 役職別内訳

| 役職 | 件数 | 全体比（推定） |
|------|------|---------------|
| **Manager** | 20,389,166 | 14.6% |
| **Director** | 8,254,128 | 5.9% |
| **Engineer** | 6,533,469 | 4.7% |
| **Owner** | 5,597,129 | 4.0% |
| **Sales** | 5,066,031 | 3.6% |
| **Marketing** | 2,748,348 | 2.0% |
| **President** | 2,831,573 | 2.0% |
| **Founder** | 1,618,303 | 1.2% |
| **CEO** | 1,339,857 | 1.0% |
| **Finance** | 1,093,245 | 0.8% |
| **HR** | 865,867 | 0.6% |
| **CTO** | 97,871 | 0.07% |
| **CFO** | 172,880 | 0.12% |
| **COO** | 117,399 | 0.08% |
| **CMO** | 26,256 | 0.02% |
| **VP** | 544,302 | 0.4% |
| **Operations** | 2,690,844 | 1.9% |
| **合計** | **約6,000万件** | **約43%** |

### 推定残り57%のデータ
- 役職が未設定/不明なプロファイル
- 非公開設定のプロファイル
- 削除・無効化されたプロファイル

## 利用可能なフィルタ

### ✅ 動作確認済み
| フィルタ | 型 | 例 |
|---------|-----|-----|
| person_job_titles | array | ["CEO", "CTO"] |

### ❌ 動作未確認/無効
| フィルタ | 期待動作 | 実際の結果 |
|---------|---------|-----------|
| company_industry | 業種で絞込 | 0件 |
| company_country | 国で絞込 | 0件 |
| person_location | 場所で絞込 | 0件 |
| company_name | 会社名で絞込 | 0件 |
| functional_area | 機能領域で絞込 | 0件 |

## 取得可能なフィールド

### 人物情報
```python
{
    "profile_id": int,
    "first_name": str,
    "last_name": str,
    "title": str,           # 役職
    "linkedin_url": str,
    "location": str,
    "country": str,
    "functional_area": [str],  # ["C-level/Leadership", "Sales"]
    "industry": str,        # 多くはnull
}
```

### 会社情報
```python
{
    "company": str,                    # 会社名
    "company_country": str,
    "company_domain": str,
    "company_industry": str,
    "company_linkedin_url": str,
}
```

## 業種一覧（100業種）

### トップ20業種（従業員数ベース）
| 業種 | 従業員数 |
|------|----------|
| Hospitals and Health Care | 5,348,765 |
| IT Services and IT Consulting | 5,138,177 |
| Financial Services | 4,326,446 |
| Software Development | 3,603,185 |
| Government Administration | 3,364,435 |
| Retail | 2,866,106 |
| E-Commerce | 2,641,562 |
| Banking | 2,345,555 |
| Construction | 2,271,961 |
| Real Estate | 1,998,482 |
| Business Consulting and Services | 1,974,384 |
| Insurance | 1,922,846 |
| Telecommunications | 1,785,646 |
| Artificial Intelligence (AI) | 1,685,042 |
| Oil and Gas | 1,486,165 |
| Non-profit Organizations | 1,471,868 |
| Enterprise Software | 1,422,761 |
| Motor Vehicle Manufacturing | 1,331,306 |
| Advertising Services | 1,277,135 |
| Manufacturing | 1,169,268 |

※業種フィルタは現在機能していない可能性あり

## 制限事項

### 検索制限
- person_job_titles以外のフィルタが効かない
- 地理位置情報での絞込不可
- 業種での絞込不可

### レート制限
- Search: 6リクエスト/分
- Reveal: 10リクエスト/分

### 日本データ
- 検索結果: 0件（確認済みパラメータ複数）
- 推定: 欧米中心のデータベース

## 利用価値の評価

### 強み
- ✅ 7,000万件以上のプロファイル
- ✅ 役職による絞込が可能
- ✅ LinkedIn URL取得可能
- ✅ 会社ドメイン取得可能

### 弱み
- ❌ 検索フィルタが限定される（job_titlesのみ確実）
- ❌ 日本データが少ない/なし
- ❌ 連絡先取得は有料（1件=1クレジット）

### 用途別評価
| 用途 | 評価 | 理由 |
|------|------|------|
| グローバル企業の役員検索 | ⭐⭐⭐⭐⭐ | CEO/C-level検索が強力 |
| 業種別リード獲得 | ⭐⭐☆☆☆ | industryフィルタが効かない |
| 地域別リード獲得 | ⭐☆☆☆☆ | locationフィルタが効かない |
| 日本市場 | ⭐☆☆☆☆ | データがほぼなし |

## 推奨用途

### 最適な使い方
1. **グローバル企業のC-levelリスト作成**
   - CEO, CTO, CFO, VP級の検索
   - 業界横断的なアプローチ

2. **多国籍企業の日本在籍者調査**
   - グローバル企業名で検索 → 日本在籍者を特定
   - 但しlocationフィルタが効かないため手動確認が必要

3. **営業ターゲットの候補リスト作成**
   - Manager, Director級の大量リスト
   - 上位企業のドメインから自社アプローチ

---

**調査日**: 2026-01-31
**調査者**: GLM-4.7 SubAgent
**API Key**: 26436f...（有効確認済み）
