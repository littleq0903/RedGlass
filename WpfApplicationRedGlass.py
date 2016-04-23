import wpf

from System.Windows import Application, Window
from System.Windows import MessageBox
from System.ComponentModel import BackgroundWorker


class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplicationRedGlass.xaml')
        
        self.startButton.Click += self.startButton_Click
        self.stopButton.Click += self.stopButton_Click 

        self.bw = BackgroundWorker()
        #// 進捗状況の更新を可能にする
        self.bw.WorkerReportsProgress = True
        #// キャンセルを可能にする
        self.bw.WorkerSupportsCancellation = True

        #// バックグラウンド行う処理
        self.bw.DoWork += self.bw_DoWork
        #// 進捗状況の更新を行う処理
        self.bw.ProgressChanged += self.bw_ProgressChanged
        #// バックグラウンドでの処理が終了後の処理
        self.bw.RunWorkerCompleted += self.bw_RunWorkerCompleted
    
    #// 時間のかかる処理
    def bw_DoWork(self, sender, e):
        import System
        for i in range(1,10001):
            if (self.bw.CancellationPending == True):
                #// キャンセルされたので処理を終了
                e.Cancel = True
                break

            #// 現在の進捗状況（数値）
            currentValue = i

            #// currentValue以外の進捗状況を表す情報（オプション）
            status = str(i) + " / 10000"

            #// 進捗状況を報告
            self.bw.ReportProgress(currentValue, status)

            #// 何らかの処理（ここではスリープさせるだけ）
            System.Threading.Thread.Sleep(1)

        #// 操作の結果を渡したい場合はe.Resultを使う
        e.Result = "[終了結果]"

    #// 進捗状況の更新処理
    def bw_ProgressChanged(self, sender, e):
        #// プログレスバーの値を更新
        self.progressBar.Value = e.ProgressPercentage

        #// プログレスバー以外の状況更新
        self.statusTextBlock.Text = e.UserState.ToString()

    #// 時間のかかる処理が終わった後の後処理
    def bw_RunWorkerCompleted(self, sender, e):
        self.statusTextBlock.Text = ""
        self.progressBar.Value = 0

        if (e.Cancelled == True):
            MessageBox.Show("処理を中断しました。")
        else:
            MessageBox.Show("処理が終了しました。" + e.Result.ToString())

        self.startButton.IsEnabled = True
        self.stopButton.IsEnabled = False

    #// 処理開始
    def startButton_Click(self, sender, e):
        self.startButton.IsEnabled = False
        self.stopButton.IsEnabled = True

        #// 時間のかかる処理を実行する
        self.bw.RunWorkerAsync()
    
    #// 作業を途中で止める
    def stopButton_Click(self, sender, e):
       self.bw.CancelAsync()


if __name__ == '__main__':
    Application().Run(MyWindow())
