"""
API データ取得・変換ツール - メインスクリプト

実装のスターターテンプレート
"""

import sys
import requests
import json
import csv
import pandas as pd
import argparse
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

# 設定ファイルのインポート
from config import API_ENDPOINTS, DATA_MAPPING, REQUEST_TIMEOUT, SUPPORTED_FORMATS, DEFAULT_OUTPUT_FILENAME

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIDataTool:
    """API データ取得・変換ツールのメインクラス"""
    
    def __init__(self):
        self.data_cache: Dict[str, Any] = {}
    
    def fetch_api_data(self, api_name: str) -> Optional[Dict[str, Any]]:
        """
        指定されたAPIからデータを取得
        
        Args:
            api_name: API名（config.pyで定義）
            
        Returns:
            取得したJSONデータ（辞書形式）
        """

        if api_name not in API_ENDPOINTS:
            logger.error(f"API '{api_name}' はサポートされていません。")
            return None
        
        url = API_ENDPOINTS[api_name]
        logger.info(f"Fetching data from {url} for API '{api_name}'")
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTPリクエストエラー: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSONデコードエラー: {e}")
            return None
        except Exception as e:
            logger.error(f"予期しないエラー: {api_name}: {e}")
            return None
    
    def fetch_all_apis(self, selected_apis: List[str]) -> Dict[str, Any]:
        """
        複数のAPIからデータを取得
        
        Args:
            selected_apis: 取得するAPI名のリスト
            
        Returns:
            API名をキーとしたデータ辞書
        """
        # TODO: 実装してください
        # ヒント:
        # 1. selected_apisをループ
        # 2. 各APIに対してfetch_api_data()を呼び出し
        # 3. 結果を辞書に格納

        results: Dict[str, Any] = {}
        for api_name in selected_apis:            
            json_result = self.fetch_api_data(api_name)
            if json_result is not None:
                results[api_name] = json_result            

        return results
    
    def normalize_data(self, api_name: str, raw_data: Any) -> List[Dict[str, Any]]:
        """
        APIデータを統一形式に変換
        
        Args:
            api_name: API名
            raw_data: APIから取得した生データ
            
        Returns:
            正規化されたデータのリスト
        """
        # TODO: 実装してください
        # ヒント:
        # 1. DATA_MAPPINGを参照してフィールドマッピング
        # 2. APIごとの特殊処理（リスト・ネスト構造）
        # 3. 共通フィールドの追加（source, fetched_at等）

        if not raw_data:
            logger.warning(f"API '{api_name}' のデータが空です。")
            return []
        if api_name not in DATA_MAPPING:
            logger.warning(f"API '{api_name}' のデータマッピングが定義されていません。")
            return []
        # raw_dataをDATA_MAPPINGに基づいて変換する処理を実装
        logger.info(f"生データの確認: {raw_data}")
        match api_name:
            case 'jsonplaceholder':
                raw_data = raw_data if isinstance(raw_data, list) else [raw_data]
            case 'catfacts':
                raw_data = raw_data.get('data', [])
            case 'randomuser':
                raw_data = raw_data.get('results', [])
            case 'github':
                raw_data = raw_data if isinstance(raw_data, list) else [raw_data]

        if not isinstance(raw_data, list):
            raw_data = [raw_data]  # 単一のオブジェクトをリストに変換

        normalized_data = []
        mapping = DATA_MAPPING.get(api_name, {})

        for record in raw_data:
            normalized_record = {
                'source': api_name,
                'fetched_at': datetime.now().isoformat()
            }

            for key, mapped_field in mapping.items():
                value = self._get_nested_value(record, mapped_field)
                normalized_record[key] = value

            normalized_data.append(normalized_record)

        return normalized_data
    
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
    
    def json_to_csv(self, data: Dict[str, Any], output_file: str) -> None:
        """
        JSONデータをCSVに変換
        
        Args:
            data: 変換するデータ
            output_file: 出力ファイル名
        """
        # TODO: 実装してください
        # ヒント:
        # 1. データの正規化
        # 2. pandas.DataFrame()でデータフレーム作成
        # 3. to_csv()でCSV出力
        try:
            all_records = []
            
            # 各APIのデータを正規化して統合
            for api_name, raw_data in data.items():
                normalized_records = self.normalize_data(api_name, raw_data)
                all_records.extend(normalized_records)
            
            if not all_records:
                logger.warning("CSVに出力するデータがありません")
                return
            
            # DataFrameに変換してCSV出力
            df = pd.DataFrame(all_records)
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"CSV出力完了: {len(all_records)}件のレコードを{output_file}に保存")
            
        except Exception as e:
            logger.error(f"CSV変換エラー: {e}")
            raise
    
    def json_to_excel(self, data: Dict[str, Any], output_file: str) -> None:
        """
        JSONデータをExcelに変換
        
        Args:
            data: 変換するデータ
            output_file: 出力ファイル名
        """
        # TODO: 実装してください
        # ヒント:
        # 1. ExcelWriterを使用
        # 2. 各API用のシートを作成
        # 3. サマリーシートの作成
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
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
            
            logger.info(f"Excel出力完了: {output_file}")
            
        except Exception as e:
            logger.error(f"Excel変換エラー: {e}")
            raise
    
    def save_data(self, data: Dict[str, Any], output_file: str, format_type: str) -> None:
        """
        データを指定フォーマットで保存
        
        Args:
            data: 保存するデータ
            output_file: 出力ファイル名
            format_type: 出力フォーマット ('csv', 'excel', 'both')
        """
        # TODO: 実装してください
        # ヒント:
        # 1. format_typeに応じた処理分岐
        # 2. 適切なファイル拡張子の付与
        # 3. 保存完了メッセージの出力
        try:
            if format_type == 'csv' or format_type == 'both':
                csv_file = f"{output_file}.csv"
                self.json_to_csv(data, csv_file)
                logger.info(f"CSVファイルを保存しました: {csv_file}")
            
            if format_type == 'excel' or format_type == 'both':
                excel_file = f"{output_file}.xlsx"
                self.json_to_excel(data, excel_file)
                logger.info(f"Excelファイルを保存しました: {excel_file}")
                
        except Exception as e:
            logger.error(f"ファイル保存エラー: {e}")
            raise


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    コマンドライン引数の設定
    
    Returns:
        設定済みのArgumentParser
    """
    # TODO: 実装してください
    # ヒント:
    # 1. ArgumentParserの作成
    # 2. --format, --output, --apis等のオプション追加
    # 3. ヘルプメッセージの設定
    parser = argparse.ArgumentParser(description='API Data Tool')  # TODO: 詳細な実装
    parser.add_argument("--format", choices=SUPPORTED_FORMATS, default='both', help="出力フォーマット")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_FILENAME, help="出力ファイル名")
    parser.add_argument("--apis", nargs='+', choices=list(API_ENDPOINTS.keys()),
                       default=list(API_ENDPOINTS.keys()), 
                       help="取得するAPI名のリスト（スペース区切り、例: --apis jsonplaceholder catfacts）")
    return parser


def main():
    """メイン関数"""
    try:
        # コマンドライン引数の解析
        parser = setup_argument_parser()
        args = parser.parse_args()
        apis = args.apis
        format_type = str(args.format)
        output_file_name = str(args.output)
        
        logger.info(f"開始: APIs={apis}, Format={format_type}, Output={output_file_name}")
        
        # APIDataToolのインスタンス化
        api_data_tool = APIDataTool()
        
        # APIデータの取得
        api_results = api_data_tool.fetch_all_apis(apis)

        if not api_results:
            logger.error("APIデータの取得に失敗しました。")
            sys.exit(1)

        # データの保存
        api_data_tool.save_data(api_results, output_file_name, format_type)

        logger.info(f"処理が完了しました: {output_file_name} ({format_type})")
        
    except Exception as e:
        logger.error(f"メイン処理でエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
