#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def main():
    """
    自動更新スクリプトを実行するためのラッパー
    """
    print("🔄 サイト自動更新ツールを起動します...")
    
    # スクリプトのパス
    script_path = os.path.join('.github', 'scripts', 'update_site.py')
    
    # スクリプトが存在するか確認
    if not os.path.exists(script_path):
        print(f"❌ エラー: スクリプトが見つかりません: {script_path}")
        sys.exit(1)
    
    try:
        # スクリプトを実行
        print(f"⚙️ {script_path} を実行中...")
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        # 結果を出力
        print("📋 実行結果:")
        print(result.stdout)
        
        # エラーがあれば表示
        if result.stderr:
            print("⚠️ エラー出力:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ サイト更新が正常に完了しました！")
        else:
            print(f"❌ サイト更新に失敗しました。終了コード: {result.returncode}")
            
    except Exception as e:
        print(f"❌ エラー: スクリプト実行中に例外が発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
