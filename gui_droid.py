#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DROID Desktop GUI
Factory.ai DROIDを使用するためのデスクトップGUIアプリケーション
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import subprocess
import os
from pathlib import Path
import threading


class DroidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DROID Desktop GUI")
        self.root.geometry("800x700")
        self.root.minsize(800, 700)
        
        # スクリプトのディレクトリを取得
        self.script_dir = Path(__file__).parent.absolute()
        self.prompt_file = self.script_dir / "prompt.json"
        self.ps_script = self.script_dir / "invoke-droid.ps1"
        
        # 実行中フラグ
        self.is_running = False
        
        # GUI構築
        self.create_widgets()
        
        # 既存の設定を読み込み
        self.load_settings()
    
    def create_widgets(self):
        """GUIウィジェットを作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ウィンドウのグリッド設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # スクロール可能なキャンバス
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === プロンプト入力エリア ===
        prompt_frame = ttk.LabelFrame(scrollable_frame, text="プロンプト (Prompt) *", padding="5")
        prompt_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        prompt_frame.columnconfigure(0, weight=1)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=8, width=70, wrap=tk.WORD)
        self.prompt_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # === オプション設定エリア ===
        options_frame = ttk.LabelFrame(scrollable_frame, text="オプション設定", padding="5")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        options_frame.columnconfigure(1, weight=1)
        
        # 作業ディレクトリ
        row = 0
        ttk.Label(options_frame, text="作業ディレクトリ:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.working_dir_var = tk.StringVar(value=".")
        ttk.Entry(options_frame, textvariable=self.working_dir_var).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(options_frame, text="参照", command=self.browse_working_dir).grid(row=row, column=2, padx=5)
        
        # モデル選択
        row += 1
        ttk.Label(options_frame, text="モデル:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.model_var = tk.StringVar(value="claude-sonnet-4-20250514")
        models = [
            "claude-opus-4-5-20251101",
            "claude-sonnet-4-20250514",
            "claude-sonnet-4-5-20241022",
            "claude-haiku-4-20250116"
        ]
        model_combo = ttk.Combobox(options_frame, textvariable=self.model_var, values=models, state="readonly")
        model_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 自動化レベル
        row += 1
        ttk.Label(options_frame, text="自動化レベル:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.auto_level_var = tk.StringVar(value="medium")
        auto_levels = ["low", "medium", "high"]
        auto_combo = ttk.Combobox(options_frame, textvariable=self.auto_level_var, values=auto_levels, state="readonly")
        auto_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # ログディレクトリ
        row += 1
        ttk.Label(options_frame, text="ログディレクトリ:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.log_dir_var = tk.StringVar(value="logs")
        ttk.Entry(options_frame, textvariable=self.log_dir_var).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(options_frame, text="参照", command=self.browse_log_dir).grid(row=row, column=2, padx=5)
        
        # === 参照ファイル/フォルダエリア ===
        ref_frame = ttk.LabelFrame(scrollable_frame, text="参照ファイル/フォルダ", padding="5")
        ref_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ref_frame.columnconfigure(0, weight=1)
        
        # リストボックスとスクロールバー
        list_frame = ttk.Frame(ref_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        
        ref_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.ref_listbox = tk.Listbox(list_frame, height=6, yscrollcommand=ref_scrollbar.set)
        ref_scrollbar.config(command=self.ref_listbox.yview)
        self.ref_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ref_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # ボタンフレーム
        ref_btn_frame = ttk.Frame(ref_frame)
        ref_btn_frame.grid(row=0, column=1, padx=5)
        ttk.Button(ref_btn_frame, text="ファイル追加", command=self.add_file).grid(row=0, column=0, pady=2)
        ttk.Button(ref_btn_frame, text="フォルダ追加", command=self.add_folder).grid(row=1, column=0, pady=2)
        ttk.Button(ref_btn_frame, text="削除", command=self.remove_ref).grid(row=2, column=0, pady=2)
        
        # === ステータス表示エリア ===
        status_frame = ttk.LabelFrame(scrollable_frame, text="実行進捗・ステータス", padding="5")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=10, width=70, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # === ボタンエリア ===
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.E), pady=10)
        
        self.reload_btn = ttk.Button(button_frame, text="読み込み", command=self.load_settings)
        self.reload_btn.grid(row=0, column=0, padx=5)
        
        self.save_btn = ttk.Button(button_frame, text="保存", command=self.save_settings)
        self.save_btn.grid(row=0, column=1, padx=5)
        
        self.execute_btn = ttk.Button(button_frame, text="実行", command=self.execute_droid, style="Accent.TButton")
        self.execute_btn.grid(row=0, column=2, padx=5)
        
        # キャンバスとスクロールバーを配置
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 初期ステータスメッセージ
        self.update_status("待機中")
    
    def browse_working_dir(self):
        """作業ディレクトリを選択"""
        directory = filedialog.askdirectory(initialdir=self.script_dir, title="作業ディレクトリを選択")
        if directory:
            self.working_dir_var.set(directory)
    
    def browse_log_dir(self):
        """ログディレクトリを選択"""
        directory = filedialog.askdirectory(initialdir=self.script_dir, title="ログディレクトリを選択")
        if directory:
            self.log_dir_var.set(directory)
    
    def add_file(self):
        """参照ファイルを追加"""
        files = filedialog.askopenfilenames(initialdir=self.script_dir, title="参照ファイルを選択")
        for file in files:
            self.ref_listbox.insert(tk.END, file)
    
    def add_folder(self):
        """参照フォルダを追加"""
        folder = filedialog.askdirectory(initialdir=self.script_dir, title="参照フォルダを選択")
        if folder:
            self.ref_listbox.insert(tk.END, folder)
    
    def remove_ref(self):
        """選択した参照を削除"""
        selection = self.ref_listbox.curselection()
        if selection:
            self.ref_listbox.delete(selection[0])
    
    def update_status(self, message, append=False):
        """ステータスメッセージを更新"""
        self.status_text.config(state=tk.NORMAL)
        if not append:
            self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def load_settings(self):
        """prompt.jsonから設定を読み込み"""
        if not self.prompt_file.exists():
            self.update_status("prompt.jsonが見つかりません。デフォルト設定を使用します。")
            return
        
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # プロンプトを設定
            self.prompt_text.delete(1.0, tk.END)
            self.prompt_text.insert(1.0, data.get('prompt', ''))
            
            # オプションを設定
            options = data.get('options', {})
            self.working_dir_var.set(options.get('working_directory', '.'))
            self.model_var.set(options.get('model', 'claude-sonnet-4-20250514'))
            self.auto_level_var.set(options.get('auto_level', 'medium'))
            self.log_dir_var.set(options.get('log_directory', 'logs'))
            
            # 参照ファイル/フォルダを設定
            self.ref_listbox.delete(0, tk.END)
            ref_paths = options.get('ref_filepath', [])
            for path in ref_paths:
                self.ref_listbox.insert(tk.END, path)
            
            self.update_status("設定を読み込みました。")
        except Exception as e:
            self.update_status(f"設定の読み込みに失敗しました: {str(e)}")
            messagebox.showerror("エラー", f"設定の読み込みに失敗しました:\n{str(e)}")
    
    def save_settings_internal(self):
        """設定をprompt.jsonに保存（内部用、メッセージボックスなし）"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        # 参照パスを取得
        ref_paths = []
        for i in range(self.ref_listbox.size()):
            ref_paths.append(self.ref_listbox.get(i))
        
        # JSONデータを構築
        data = {
            "prompt": prompt,
            "options": {
                "working_directory": self.working_dir_var.get(),
                "model": self.model_var.get(),
                "auto_level": self.auto_level_var.get(),
                "log_directory": self.log_dir_var.get()
            }
        }
        
        # 参照パスがある場合のみ追加
        if ref_paths:
            data["options"]["ref_filepath"] = ref_paths
        
        with open(self.prompt_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def save_settings(self):
        """設定をprompt.jsonに保存"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("警告", "プロンプトを入力してください。")
            return
        
        try:
            self.save_settings_internal()
            self.update_status("設定を保存しました。")
            messagebox.showinfo("成功", "設定をprompt.jsonに保存しました。")
        except Exception as e:
            self.update_status(f"設定の保存に失敗しました: {str(e)}")
            messagebox.showerror("エラー", f"設定の保存に失敗しました:\n{str(e)}")
    
    def execute_droid(self):
        """DROIDを実行"""
        if self.is_running:
            messagebox.showwarning("警告", "既に実行中です。")
            return
        
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not prompt:
            messagebox.showwarning("警告", "プロンプトを入力してください。")
            return
        
        # まず設定を保存（ユーザーに確認）
        self.update_status("設定を保存しています...")
        self.save_settings_internal()  # 内部的な保存（メッセージボックスなし）
        
        # ボタンを無効化
        self.is_running = True
        self.execute_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.reload_btn.config(state=tk.DISABLED)
        
        # 別スレッドで実行
        thread = threading.Thread(target=self._execute_droid_thread)
        thread.daemon = True
        thread.start()
    
    def _execute_droid_thread(self):
        """DROIDを実行（スレッド内）"""
        try:
            self.update_status("DROIDを実行中...")
            
            # PowerShellスクリプトの存在を確認（セキュリティ対策）
            if not self.ps_script.exists():
                raise FileNotFoundError(f"PowerShellスクリプトが見つかりません: {self.ps_script}")
            
            # スクリプトが期待されるディレクトリ内にあることを確認
            if not self.ps_script.parent.samefile(self.script_dir):
                raise ValueError("PowerShellスクリプトが不正なディレクトリにあります")
            
            # PowerShellスクリプトを実行
            cmd = [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", str(self.ps_script)
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.script_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1
            )
            
            # リアルタイムで出力を読み取る
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.rstrip()
                if line:
                    # ステータス表示を更新
                    self.update_status(line, append=True)
            
            # プロセスの終了を待つ
            process.wait()
            
            # エラー出力を確認
            stderr_output = process.stderr.read()
            
            if process.returncode == 0:
                self.update_status("\n実行完了しました。", append=True)
                self.root.after(0, lambda: messagebox.showinfo("完了", "DROIDの実行が完了しました。"))
            else:
                error_msg = stderr_output if stderr_output else "不明なエラー"
                self.update_status(f"\nエラー: {error_msg}", append=True)
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("エラー", f"DROIDの実行に失敗しました:\n{msg}"))
        
        except Exception as e:
            self.update_status(f"\n実行エラー: {str(e)}", append=True)
            self.root.after(0, lambda err=str(e): messagebox.showerror("エラー", f"実行中にエラーが発生しました:\n{err}"))
        
        finally:
            # ボタンを有効化
            self.is_running = False
            self.root.after(0, lambda: self.execute_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.save_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.reload_btn.config(state=tk.NORMAL))


def main():
    """メイン関数"""
    root = tk.Tk()
    app = DroidGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
