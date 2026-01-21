# ModernWpf Design Features - DROID WPF GUI

このドキュメントでは、新しい WPF GUI に適用されている ModernWpf のモダンデザイン機能について説明します。

## ModernWpf とは

[ModernWpf](https://github.com/Kinnara/ModernWpf) は、WPF アプリケーションに Windows 10/11 の Fluent Design System を導入するライブラリです。

## 適用されたモダンデザイン要素

### 1. モダンウィンドウスタイル

```xaml
ui:WindowHelper.UseModernWindowStyle="True"
```

- Windows 11 スタイルのウィンドウ枠
- アクリル効果（半透明）のサポート
- モダンなタイトルバー

### 2. ModernWpf テーマシステム

```xaml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ui:ThemeResources />
            <ui:XamlControlsResources />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

- 自動的にシステムテーマ（ライト/ダーク）に対応
- Windows 11 のアクセントカラーを使用
- 統一されたデザイン言語

### 3. モダンコントロール

#### SimpleStackPanel
```xaml
<ui:SimpleStackPanel Grid.Row="1" Margin="0,0,0,10" Spacing="10">
```

標準の StackPanel よりも洗練されたスペーシングと配置を提供します。

#### AccentButtonStyle
```xaml
<Button Style="{StaticResource AccentButtonStyle}" />
```

「実行」ボタンに適用され、アクセントカラーで強調表示されます。

### 4. モダンなコントロールスタイリング

以下のコントロールが自動的にモダンスタイルになります：

- **TextBox**: 丸みを帯びた角、フォーカス時のアニメーション
- **ComboBox**: モダンなドロップダウンスタイル
- **Button**: ホバー効果、押下時のアニメーション
- **GroupBox**: 洗練されたボーダーとヘッダースタイル
- **ListBox**: モダンな選択スタイル

### 5. レイアウトとスペーシング

- 一貫した余白（Margin）とパディング（Padding）
- グリッドベースのレスポンシブレイアウト
- 適切な視覚的階層

### 6. タイポグラフィ

```xaml
FontSize="12"  <!-- 本文テキスト -->
FontSize="13"  <!-- ラベル -->
FontFamily="Consolas"  <!-- ステータス表示（等幅フォント） -->
```

## UI構造

### メインレイアウト

```
┌─────────────────────────────────────────────┐
│ DROID Desktop GUI (Modern Title Bar)       │
├─────────────────────────────────────────────┤
│                                             │
│ プロンプト (Prompt) *                       │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ │  Multi-line TextBox                     │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─ オプション設定 ───────────────────────┐ │
│ │ 作業ディレクトリ:  [_________] [参照]  │ │
│ │ モデル:            [dropdown ▼]        │ │
│ │ 自動化レベル:      [dropdown ▼]        │ │
│ │ ログディレクトリ:  [_________] [参照]  │ │
│ │ AGENTS.mdファイル: [_________] [参照]  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─ 参照ファイル/フォルダ ─────────────────┐ │
│ │ ┌──────────────────┐  [ファイル追加]   │ │
│ │ │                  │  [フォルダ追加]   │ │
│ │ │   ListBox        │  [削除]           │ │
│ │ │                  │                   │ │
│ │ └──────────────────┘                   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─ 実行進捗・ステータス ───────────────────┐ │
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ 待機中                              │ │ │
│ │ │                                     │ │ │
│ │ │ (Console-style status display)      │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│                   [読み込み][保存][実行]    │
└─────────────────────────────────────────────┘
```

## デザインの利点

### ユーザーエクスペリエンス
- **直感的**: Windows 11 の標準UIに準拠
- **一貫性**: システム全体と統一されたデザイン
- **アクセシビリティ**: 視認性の高いコントラストと適切なフォントサイズ

### 視覚的魅力
- **モダン**: 最新の Windows デザイン言語
- **洗練**: 丸みを帯びた角とスムーズなアニメーション
- **プロフェッショナル**: 統一感のある配色とレイアウト

### テーマサポート
- **ライトテーマ**: 明るい背景で見やすい
- **ダークテーマ**: 暗い環境での目の疲労を軽減
- **自動切り替え**: Windows のシステム設定に自動的に追従

## カスタマイズ

ModernWpf を使用することで、以下のカスタマイズが容易になります：

### アクセントカラーの変更
```csharp
ThemeManager.Current.AccentColor = Colors.Blue;
```

### テーマの手動切り替え
```csharp
ThemeManager.Current.ApplicationTheme = ApplicationTheme.Dark;
```

### カスタムリソースの追加
```xaml
<ui:ThemeResources>
    <ui:ThemeResources.ThemeDictionaries>
        <ResourceDictionary x:Key="Light">
            <!-- ライトテーマのカスタマイズ -->
        </ResourceDictionary>
        <ResourceDictionary x:Key="Dark">
            <!-- ダークテーマのカスタマイズ -->
        </ResourceDictionary>
    </ui:ThemeResources.ThemeDictionaries>
</ui:ThemeResources>
```

## Windows Forms版との比較

| 項目 | Windows Forms | WPF + ModernWpf |
|------|--------------|-----------------|
| ウィンドウスタイル | 従来型 | Windows 11 スタイル |
| コントロールデザイン | Windows XP/7 風 | Windows 11 Fluent Design |
| テーマサポート | なし | ライト/ダーク自動切り替え |
| アニメーション | なし | スムーズな遷移効果 |
| スケーリング | DPI 対応が困難 | 自動 DPI スケーリング |
| カスタマイズ性 | 限定的 | 高度にカスタマイズ可能 |

## 参考リンク

- [ModernWpf GitHub](https://github.com/Kinnara/ModernWpf)
- [ModernWpf サンプル](https://github.com/Kinnara/ModernWpf/tree/master/samples)
- [Windows Fluent Design System](https://docs.microsoft.com/en-us/windows/apps/design/signature-experiences/design-principles)
