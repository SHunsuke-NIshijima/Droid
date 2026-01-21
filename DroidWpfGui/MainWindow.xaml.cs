using System.IO;
using System.Text;
using System.Text.Json;
using System.Windows;
using System.Diagnostics;
using Microsoft.Win32;
using System.Windows.Forms;
using MessageBox = System.Windows.MessageBox;

namespace DroidWpfGui;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    private readonly string scriptDir;
    private readonly string promptFile;
    private readonly string psScript;

    public MainWindow()
    {
        InitializeComponent();
        
        // スクリプトのディレクトリを取得
        scriptDir = AppDomain.CurrentDomain.BaseDirectory;
        // 実行ファイルの親ディレクトリを取得（bin/Debug/net8.0-windows の親）
        var exeDir = new DirectoryInfo(scriptDir);
        if (exeDir.Parent?.Parent?.Parent != null)
        {
            scriptDir = exeDir.Parent.Parent.Parent.FullName;
        }
        
        promptFile = Path.Combine(scriptDir, "prompt.json");
        psScript = Path.Combine(scriptDir, "invoke-droid.ps1");
        
        // 初回起動時に設定を読み込み
        LoadSettings();
    }

    private void BrowseWorkDir_Click(object sender, RoutedEventArgs e)
    {
        using var dialog = new FolderBrowserDialog
        {
            Description = "作業ディレクトリを選択",
            SelectedPath = scriptDir
        };
        
        if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
        {
            txtWorkDir.Text = dialog.SelectedPath;
        }
    }

    private void BrowseLogDir_Click(object sender, RoutedEventArgs e)
    {
        using var dialog = new FolderBrowserDialog
        {
            Description = "ログディレクトリを選択",
            SelectedPath = scriptDir
        };
        
        if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
        {
            txtLogDir.Text = dialog.SelectedPath;
        }
    }

    private void BrowseAgentsFile_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFileDialog
        {
            Filter = "Markdown Files (*.md)|*.md|All Files (*.*)|*.*",
            Title = "AGENTS.mdファイルを選択",
            InitialDirectory = scriptDir
        };
        
        if (dialog.ShowDialog() == true)
        {
            txtAgentsFile.Text = dialog.FileName;
        }
    }

    private void AddFile_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFileDialog
        {
            Multiselect = true,
            Title = "参照ファイルを選択",
            InitialDirectory = scriptDir
        };
        
        if (dialog.ShowDialog() == true)
        {
            foreach (var file in dialog.FileNames)
            {
                lstRef.Items.Add(file);
            }
        }
    }

    private void AddFolder_Click(object sender, RoutedEventArgs e)
    {
        using var dialog = new FolderBrowserDialog
        {
            Description = "参照フォルダを選択",
            SelectedPath = scriptDir
        };
        
        if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
        {
            lstRef.Items.Add(dialog.SelectedPath);
        }
    }

    private void Remove_Click(object sender, RoutedEventArgs e)
    {
        if (lstRef.SelectedIndex >= 0)
        {
            lstRef.Items.RemoveAt(lstRef.SelectedIndex);
        }
    }

    private void LoadSettings()
    {
        if (File.Exists(promptFile))
        {
            try
            {
                var jsonContent = File.ReadAllText(promptFile, Encoding.UTF8);
                using var document = JsonDocument.Parse(jsonContent);
                var root = document.RootElement;

                if (root.TryGetProperty("prompt", out var promptProp))
                {
                    txtPrompt.Text = promptProp.GetString() ?? "";
                }

                if (root.TryGetProperty("options", out var options))
                {
                    if (options.TryGetProperty("working_directory", out var workDir))
                    {
                        txtWorkDir.Text = workDir.GetString() ?? ".";
                    }

                    if (options.TryGetProperty("model", out var model))
                    {
                        var modelStr = model.GetString();
                        for (int i = 0; i < cmbModel.Items.Count; i++)
                        {
                            if ((cmbModel.Items[i] as System.Windows.Controls.ComboBoxItem)?.Content?.ToString() == modelStr)
                            {
                                cmbModel.SelectedIndex = i;
                                break;
                            }
                        }
                    }

                    if (options.TryGetProperty("auto_level", out var autoLevel))
                    {
                        var levelStr = autoLevel.GetString();
                        for (int i = 0; i < cmbAutoLevel.Items.Count; i++)
                        {
                            if ((cmbAutoLevel.Items[i] as System.Windows.Controls.ComboBoxItem)?.Content?.ToString() == levelStr)
                            {
                                cmbAutoLevel.SelectedIndex = i;
                                break;
                            }
                        }
                    }

                    if (options.TryGetProperty("log_directory", out var logDir))
                    {
                        txtLogDir.Text = logDir.GetString() ?? "logs";
                    }

                    if (options.TryGetProperty("agents_file", out var agentsFile))
                    {
                        txtAgentsFile.Text = agentsFile.GetString() ?? "";
                    }

                    if (options.TryGetProperty("ref_filepath", out var refPaths) && refPaths.ValueKind == JsonValueKind.Array)
                    {
                        lstRef.Items.Clear();
                        foreach (var path in refPaths.EnumerateArray())
                        {
                            var pathStr = path.GetString();
                            if (!string.IsNullOrEmpty(pathStr))
                            {
                                lstRef.Items.Add(pathStr);
                            }
                        }
                    }
                }

                txtStatus.Text = "設定を読み込みました。";
            }
            catch (Exception ex)
            {
                txtStatus.Text = $"設定の読み込みに失敗しました: {ex.Message}";
                MessageBox.Show($"設定の読み込みに失敗しました:\n{ex.Message}", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        else
        {
            txtStatus.Text = "prompt.jsonが見つかりません。デフォルト設定を使用します。";
        }
    }

    private bool SaveSettings()
    {
        if (string.IsNullOrWhiteSpace(txtPrompt.Text))
        {
            MessageBox.Show("プロンプトを入力してください。", "警告", MessageBoxButton.OK, MessageBoxImage.Warning);
            return false;
        }

        var refPaths = new List<string>();
        foreach (var item in lstRef.Items)
        {
            refPaths.Add(item.ToString() ?? "");
        }

        var data = new Dictionary<string, object>
        {
            ["prompt"] = txtPrompt.Text,
            ["options"] = new Dictionary<string, object>
            {
                ["working_directory"] = txtWorkDir.Text,
                ["model"] = (cmbModel.SelectedItem as System.Windows.Controls.ComboBoxItem)?.Content?.ToString() ?? "",
                ["auto_level"] = (cmbAutoLevel.SelectedItem as System.Windows.Controls.ComboBoxItem)?.Content?.ToString() ?? "",
                ["log_directory"] = txtLogDir.Text
            }
        };

        var options = (Dictionary<string, object>)data["options"];

        if (!string.IsNullOrWhiteSpace(txtAgentsFile.Text))
        {
            options["agents_file"] = txtAgentsFile.Text;
        }

        if (refPaths.Count > 0)
        {
            options["ref_filepath"] = refPaths;
        }

        try
        {
            var json = JsonSerializer.Serialize(data, new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            });
            
            File.WriteAllText(promptFile, json, new UTF8Encoding(false));
            txtStatus.Text = "設定を保存しました。";
            return true;
        }
        catch (Exception ex)
        {
            txtStatus.Text = $"設定の保存に失敗しました: {ex.Message}";
            MessageBox.Show($"設定の保存に失敗しました:\n{ex.Message}", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
            return false;
        }
    }

    private void Reload_Click(object sender, RoutedEventArgs e)
    {
        LoadSettings();
    }

    private void Save_Click(object sender, RoutedEventArgs e)
    {
        if (SaveSettings())
        {
            MessageBox.Show("設定をprompt.jsonに保存しました。", "成功", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }

    private async void Execute_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(txtPrompt.Text))
        {
            MessageBox.Show("プロンプトを入力してください。", "警告", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        txtStatus.Text = "設定を保存しています...\n";
        
        if (!SaveSettings())
        {
            return;
        }

        if (!File.Exists(psScript))
        {
            txtStatus.Text = $"エラー: invoke-droid.ps1が見つかりません";
            MessageBox.Show($"invoke-droid.ps1が見つかりません: {psScript}", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
            return;
        }

        btnExecute.IsEnabled = false;
        btnSave.IsEnabled = false;
        btnReload.IsEnabled = false;

        txtStatus.Text += "DROIDを実行中...\n";

        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                Arguments = $"-NoProfile -ExecutionPolicy Bypass -File \"{psScript}\"",
                WorkingDirectory = scriptDir,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = false,
                StandardOutputEncoding = Encoding.UTF8
            };

            using var process = new Process { StartInfo = processInfo };
            
            process.OutputDataReceived += (s, ev) =>
            {
                if (!string.IsNullOrEmpty(ev.Data))
                {
                    Dispatcher.Invoke(() =>
                    {
                        txtStatus.AppendText(ev.Data + "\n");
                        txtStatus.ScrollToEnd();
                    });
                }
            };

            process.Start();
            process.BeginOutputReadLine();

            await Task.Run(() => process.WaitForExit());

            var stderr = await process.StandardError.ReadToEndAsync();

            if (process.ExitCode == 0)
            {
                txtStatus.AppendText("\n実行完了しました。");
                MessageBox.Show("DROIDの実行が完了しました。", "完了", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            else
            {
                var errorMsg = string.IsNullOrWhiteSpace(stderr) 
                    ? $"実行が失敗しました (終了コード: {process.ExitCode})" 
                    : stderr;
                txtStatus.AppendText($"\nエラー: {errorMsg}");
                MessageBox.Show($"DROIDの実行に失敗しました。\n{errorMsg}", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        catch (Exception ex)
        {
            txtStatus.AppendText($"\n実行エラー: {ex.Message}");
            MessageBox.Show($"実行中にエラーが発生しました:\n{ex.Message}", "エラー", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            btnExecute.IsEnabled = true;
            btnSave.IsEnabled = true;
            btnReload.IsEnabled = true;
        }
    }
}