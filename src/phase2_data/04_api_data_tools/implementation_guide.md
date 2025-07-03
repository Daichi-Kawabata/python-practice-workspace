# API データ取得・変換ツール - 実装ガイド

## 🎯 実装の進め方

### Phase 1: 基本的なAPI取得
1. `fetch_api_data()` メソッドを実装
2. 1つのAPIから正常にデータを取得できることを確認
3. エラーハンドリングを追加

### Phase 2: 複数API対応
1. `fetch_all_apis()` メソッドを実装
2. コマンドライン引数の処理を追加
3. 複数のAPIからデータを取得できることを確認

### Phase 3: データ変換
1. `normalize_data()` メソッドを実装
2. `json_to_csv()` メソッドを実装
3. CSV出力機能を完成

### Phase 4: Excel対応
1. `json_to_excel()` メソッドを実装
2. 複数シート対応
3. サマリーシートの作成

### Phase 5: 仕上げ
1. エラーハンドリングの強化
2. ログ機能の追加
3. テストの作成

## 💡 実装のヒント

### API データ取得の基本パターン
```python
def fetch_api_data(self, api_name: str) -> Optional[Dict[str, Any]]:
    try:
        if api_name not in API_ENDPOINTS:
            logger.error(f"Unknown API: {api_name}")
            return None
        
        url = API_ENDPOINTS[api_name]
        logger.info(f"Fetching data from {api_name}: {url}")
        
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully fetched {len(data)} records from {api_name}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {api_name}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {api_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for {api_name}: {e}")
        return None
```

### データ正規化の基本パターン
```python
def normalize_data(self, api_name: str, raw_data: Any) -> List[Dict[str, Any]]:
    if not raw_data:
        return []
    
    # APIごとの特殊処理
    if api_name == 'randomuser':
        # randomuser APIはresultsキーの下にデータが格納される
        raw_data = raw_data.get('results', [])
    elif api_name == 'catfacts':
        # catfacts APIはdataキーの下にデータが格納される
        raw_data = raw_data.get('data', [])
    
    # データがリストでない場合はリストに変換
    if not isinstance(raw_data, list):
        raw_data = [raw_data]
    
    normalized_records = []
    mapping = DATA_MAPPING.get(api_name, {})
    
    for record in raw_data:
        normalized_record = {
            'source': api_name,
            'fetched_at': datetime.now().isoformat()
        }
        
        # マッピング設定に基づいてフィールドを変換
        for new_field, old_field_path in mapping.items():
            value = self._get_nested_value(record, old_field_path)
            normalized_record[new_field] = value
        
        normalized_records.append(normalized_record)
    
    return normalized_records

def _get_nested_value(self, data: dict, path: str) -> Any:
    """ネストされたフィールドの値を取得"""
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and key.isdigit():
            index = int(key)
            if 0 <= index < len(current):
                current = current[index]
            else:
                return None
        else:
            return None
    
    return current
```

### CSV出力の基本パターン
```python
def json_to_csv(self, data: Dict[str, Any], output_file: str) -> None:
    try:
        all_records = []
        
        # すべてのAPIデータを正規化して統合
        for api_name, raw_data in data.items():
            normalized_records = self.normalize_data(api_name, raw_data)
            all_records.extend(normalized_records)
        
        if not all_records:
            logger.warning("No data to export to CSV")
            return
        
        # DataFrameに変換
        df = pd.DataFrame(all_records)
        
        # CSVファイルに出力
        csv_file = f"{output_file}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        logger.info(f"Successfully exported {len(all_records)} records to {csv_file}")
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        raise
```

### Excel出力の基本パターン
```python
def json_to_excel(self, data: Dict[str, Any], output_file: str) -> None:
    try:
        excel_file = f"{output_file}.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            summary_data = []
            
            # 各APIのデータを別シートに出力
            for api_name, raw_data in data.items():
                normalized_records = self.normalize_data(api_name, raw_data)
                
                if normalized_records:
                    df = pd.DataFrame(normalized_records)
                    df.to_excel(writer, sheet_name=api_name, index=False)
                    
                    # サマリー情報を収集
                    summary_data.append({
                        'API': api_name,
                        'Records': len(normalized_records),
                        'Columns': len(df.columns),
                        'Exported_at': datetime.now().isoformat()
                    })
            
            # サマリーシートを作成
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        logger.info(f"Successfully exported data to {excel_file}")
        
    except Exception as e:
        logger.error(f"Error exporting to Excel: {e}")
        raise
```

### コマンドライン引数の基本パターン
```python
def setup_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='API Data Tool - Fetch JSON data from APIs and convert to CSV/Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --format csv --output result --apis jsonplaceholder,countries
  %(prog)s --format excel --output mydata --apis all
  %(prog)s --format both --output combined --apis jsonplaceholder,countries,catfacts
        '''
    )
    
    parser.add_argument(
        '--format', 
        choices=SUPPORTED_FORMATS,
        default='csv',
        help='Output format (default: csv)'
    )
    
    parser.add_argument(
        '--output', 
        required=True,
        help='Output file name (without extension)'
    )
    
    parser.add_argument(
        '--apis',
        required=True,
        help='Comma-separated list of APIs to fetch (or "all" for all APIs)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser
```

## 🔧 デバッグのコツ

### 1. APIレスポンスの確認
```python
# 各APIの実際のレスポンス構造を確認
import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)
print(json.dumps(response.json()[:2], indent=2))  # 最初の2件を表示
```

### 2. ステップバイステップの実行
```python
# 各段階でデータを確認
tool = APIDataTool()
data = tool.fetch_api_data('jsonplaceholder')
print(f"Raw data type: {type(data)}")
print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

normalized = tool.normalize_data('jsonplaceholder', data)
print(f"Normalized records: {len(normalized)}")
print(f"Sample record: {normalized[0] if normalized else 'None'}")
```

### 3. エラーログの活用
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # DEBUGレベルでより詳細なログ
```

## 🚀 スタートアップガイド

1. **必要なライブラリのインストール**
```bash
pip install requests pandas openpyxl
```

2. **基本的な動作確認**
```python
# 単純なAPIテスト
import requests
response = requests.get('https://jsonplaceholder.typicode.com/posts')
print(response.status_code)
print(len(response.json()))
```

3. **段階的な実装**
- まずは1つのAPIから始める
- 小さく動作確認しながら進める
- エラーハンドリングは後から追加

頑張ってください！質問があれば遠慮なくお聞きください。
