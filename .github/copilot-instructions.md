日本語で応答して
下記の要件に従ってコーディングして
ghコマンドは既に認証できてます！

始めに、プロジェクトファイル全体を読み取り、プロジェクトの内容を理解してください。

あなたのレート制限を避けるために、実行をステップに分けてください。
ステップが１つ終わるごとに、わたしにつづけるか確認してください。
ステップでは何を実行しているか明記し、タイトルをつけてください。
タイトルの前には内容に適した絵文字を入れて。


---


## リポジトリ要件定義プロンプト
### 基本方針
- **言語ポリシー**  
  - コード中の変数名・関数名・クラス名・ファイル名などのコード要素：英語  
  - コメント、README、ドキュメント、コミットメッセージ：日本語
- **README作成・整備**  
  - `README.md`を必ず作成し、日本語で記述すること。  
  - `README.md`には、`assets`ディレクトリに格納したSVGヘッダー画像を使用し、中央揃えで配置する。  
    - SVGは角を丸めた形状、グラデーション、図形・テキスト・グラデーションに対するアニメーションを付与し、英語の洗練された表現を入れること。  
  - `README.md`は変更が生じるたびに更新すること。  
  - 重複コンテンツは避け、情報源を一元化する。
　- READMEの章には絵文字を付与して可読性を高めて
### コーディング原則
1. **DRY（Don't Repeat Yourself）**  
   - 同一・類似処理は関数・モジュール化することで再利用性を高める。
2. **責務の分離（Separation of Concerns）**  
   - 各モジュール・クラス・関数は単一責務を明確にし、表現・ロジック・データ処理を分離する。
3. **KISS（Keep It Simple, Stupid）**  
   - コードは可能な限りシンプルに保ち、過度な複雑化を避ける。
4. **分割統治（Divide and Conquer）**  
   - 大きな問題は小さな単位に分割し、テスト・保守性を向上させる。
5. **防御的プログラミング（Defensive Programming）**  
   - 入力値検証、例外処理、エラー対策を行い、堅牢性とセキュリティを確保する。
6. **YAGNI（You Aren't Gonna Need It）**  
   - 現在の要件に集中し、不要な将来予測による過剰実装を避ける。
7. **可読性とドキュメンテーション**  
   - 変数・関数・クラス名は英語で、役割が一目でわかるような命名を行う。  
   - コメントやREADMEでコードの意図・ロジックを日本語で明確に説明する。
8. **テスト駆動開発（TDD）とユニットテスト**  
   - 基本機能にはユニットテストを用意する。  
   - TDDを推奨し、要件定義→テスト→実装→リファクタリングのサイクルを確立する。
9. **バージョン管理とコードレビュー**  
   - Gitで変更履歴を管理し、プルリクエストを通じてコードレビューを行う。  
   - ファイルを変更したら、変更があったファイルごとにコミットを行い、履歴管理を明確化すること。
10. **SOLID原則の適用**  
    - SRP, OCP, LSP, ISP, DIPを考慮し、拡張性・保守性の高い設計を行う。
### コミットメッセージ形式
- コミットメッセージは以下の形式に従うこと:

<絵文字> <タイプ>: <タイトル>
<本文>
<フッター>

- タイトル（コミットメッセージの1行目）の先頭には必ず絵文字を付与し、日本語で記述すること。  
- タイプは以下のいずれかとする：
- **feat**: 新機能  
- **fix**: バグ修正  
- **docs**: ドキュメントの変更  
- **style**: コードスタイルの変更（動作に影響しない）  
- **refactor**: リファクタリング  
- **perf**: パフォーマンス改善  
- **test**: テストの追加・修正  
- **chore**: ビルドプロセスやツールの変更


### 追加要件（必要に応じて）
- **CI/CD導入**: 自動テスト、ビルド、デプロイを行うパイプラインを整備し、品質と迅速なリリースを実現する。  
- **パフォーマンス最適化**: 必要に応じて計測・改善を行い、効率的なスケールを実現する。  
- **アクセシビリティ・国際化対応**: ターゲットユーザに応じてi18nやアクセシビリティ対応を検討する。