# Muraena API 調査レポート

## 現状

### 確認したエンドポイント
| URL | 結果 | 備考 |
|-----|------|------|
| https://api.muraena.ai/v1/people/search | DNS解決不可 | ドキュメント記載のエンドポイント |
| https://app.muraena.ai/api/v1/people/search | HTML返却 | SPAのindex.html |
| https://app.muraena.ai/api/people/search | HTML返却 | - |
| https://app.muraena.ai/v1/people/search | HTML返却 | - |

### レスポンスヘッダー
```
content-type: text/html; charset=utf-8
server: cloudflare
```

## 考えられる原因

1. **APIエンドポイントが変更された**
   - ドキュメントが古い可能性
   - 新しいエンドポイントへの移行

2. **認証が必要な別ドメイン**
   - api.muraena.ai は存在しない
   - app.muraena.ai/api/* はフロントエンド用

3. **IP制限・地域制限**
   - 日本からのアクセスに制限がある可能性

## 推奨アクション

### 即座に行うこと
1. Muraenaサポートに問い合わせ
   - Email: support@muraena.ai
   - 正しいAPIエンドポイントを確認

2. ブラウザで動作確認
   - https://app.muraena.ai にログイン
   - ブラウザのDevToolsでネットワークリクエストを確認
   - 実際のAPI呼び出し先を特定

3. APIキーの状態確認
   - Businessプランに加入済みか確認
   - APIキーが有効か確認

### 仮実装（API解決まで）
```python
# モックデータで開発を進める
MOCK_MODE = True

if MOCK_MODE:
    # 国税庁データのみで開発
    # Muraena連携は後で実装
    pass
```

## 代替データソース（Muraenaが使えない場合）

1. **国税庁法人番号データ**（無料）
   - 日本企業の基本情報
   - 毎月更新

2. **LinkedIn API**（審査制）
   - 個人プロフィール
   - 制限あり

3. **Crunchbase API**（有料）
   - スタートアップ情報
   - 資金調達データ

4. **自社スクレイピング**
   - 企業HP
   - 有価証券報告書

