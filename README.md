# TSMS_API


## 環境設置

> 以下提到的資料 (dll檔, mdf檔)，
> 都可以在公司的 [Google Drive](https://drive.google.com/drive/folders/1sFkGbrx-y_jS64qBEkq9rF0ZUn6klMW7) 找到

1. 確認使用當前版本的 `TSMS_API.dll` (在根目錄下的)

2. 確認使用當前版本的 `TSMS_TANFB.mdf` 及 `TSMS_TANFB.ldf` (可使用 SQL Server Studio 設定)

   相關資料庫設定請見 [TSMS_TANFB 整體架構](https://code.nuwainfo.com/trac/phantasos/wiki/TSMS_TANFB%E6%95%B4%E9%AB%94%E6%9E%B6%E6%A7%8B)

3. 設定 `Config.ini` (在根目錄下)，
   
   其中 `OutputDirectory` 指明創造出來的照片等等所放的資料夾；
   
   `DataFileRootDir` 指明當伺服器要求靜態檔案時，要去哪個地方搜尋；
   
   `ConnectionString` 為設定與資料庫連線的字串，
   `Data Source` 指明連線的位址與 Port，`User Name` 與 `Password` 分別為該資料庫使用者的帳號密碼

## 更新版本步驟

> 圖文說明請看 [更新 TSMS_API_Web 流程
](https://code.nuwainfo.com/trac/phantasos/wiki/TSMS_TANFB%E6%95%B4%E9%AB%94%E6%9E%B6%E6%A7%8B#%E6%9B%B4%E6%96%B0TSMS_API_Web%E6%B5%81%E7%A8%8B)

1. 更改 `TSMS_API_Web/Properties/AssemblyInfo.cs` 的版本號

2. Commit 後看 Revision 號碼
   
3. 在剛剛的 `TSMS_API_Web/Properties/AssemblyInfo.cs` 改 Revision 號

4. 重編譯專案 (rebuild)

   (點選 `Build/Batch Build`，勾選 Debug 和 Release 版本，選擇 Rebuild)

5. 最後再 commit 一次
