
# TSMS_API_WEB 測試說明

> 此專案為測試 TSMS_API.dll 使用的測試專案
>
> 有 Bookbase.py, Geology.py 等等的模組，
> 分別對應不同的功能測試
>
> 而 Test.py 為整合以上 test cases 的總體測試，
> 因此測試時只要跑這個檔案就好了 


## 測試步驟

1. 確認資料庫連線，確認使用與資料庫資料對應的 API (TSMS_API.dll)

   在 Config.ini 中，設定 SQL SERVER 的連線位址
   
   ![](img/ConfigSetting.PNG)
   
   (圖中 `127.0.0.1,1433` 處應設定為 SERVER 連線的位置，
    `User ID=TSMS;Password=TSMS` 則為進入資料庫的帳號密碼)

2. 使用 Iron Python 跑 Test.py 檔

   請先下載 Iron Python 並安裝完成，
   [點我前往 Iron Python 官網](http://ironpython.net/)
   
   請使用 Iron Python 裡的 ipy.exe，執行 Test.py
   
   以 Windows 系統為例，開啟 cmd，請先到 Test.py 的資料夾下，並使用以下指令
   
   ![](img/IronPythonInCmd.PNG)
   
   (圖中第一項指令為往 ipy.exe 的路徑，第二格參數放 Test.py)
   
   執行成功的話，就會開始跑測試程式
   
   ![](img/IronPythonProcess.PNG)
      
3. 確認結果

   全數通過測試，應顯示
   
   ![](img/TestsPassed.jpg)
   
   而假使有錯誤的話會顯示
   
   ![](img/TestsFailed.PNG)
   
   而往上就能看到是哪些方法(函式)出錯
   
   ![](img/TestsFailed2.PNG)
   
   (舉例來說，這張圖顯示了 test2_8_2 和 test2_2_2 出錯，
   
   而第一個產生的例外為 `Exception: DataNotExistException`)


## Debug 步驟

> 我們在測試檔的部分，增加了更多訊息，
> 並在出錯時，API 也會寫下 log 檔以利接下來的除錯。
> 以下將會以 test2_3_3 作為範例說明：

1. 查看錯誤
   
   ![](img/Debug1.PNG)
   
   可以由此看到 `test2_3_3` 出錯，例外類別是 `DataNotExistException`，
   
   時間和出錯函式都有標明，可以看到是 `QueryWebview3` 出了問題，是在 `06:51:41` 出的問題，
   
   不過這裡的函式是 `TSMS_Web.API` 裡面的，並非 `TSMS.API` 的，
   
   這時候就需要到 `API.log` 查看更深入的資訊。

2. 查看 API.log

   此時可以看到跟目錄下多了一個 API.log

   ![](img/Debug2.PNG)
   
   打開後，使用剛剛的時間搜尋，可以發現這時候呼叫了一次 API，
   
   ![](img/Debug3.PNG)
   
   後面帶的會是「相關物件的名子：呼叫的 API」
   
   ![](img/Debug4.PNG)
   
   上圖中，可以呼叫這個 API 是要取得 `WebView3.TunSectorEvaluationRecord`，
   
   有時候如果 testcase 結果顯示搜尋不到某些物件為空，就需要以這項去搜尋，如 test2_9_4:
   
   ![](img/Debug6.PNG)
   
   此例中，剛剛並無如此顯示，所以這一項暫時用不到。
   
   ![](img/Debug5.PNG)
   
   由此圖可以看出呼叫的 API 是
   
   `TSMS_API.Inspect.QueryService.QueryTunSectorEvaluationData(structureId=26, projectId=4, startSectorId=1, endSectorId=5, comparisonProjectId=0)`

   因此可能要檢查 `QueryTunSectorEvaluationData` 在帶這些參數時，發生了甚麼問題，去做進一步的處理。
   
   
