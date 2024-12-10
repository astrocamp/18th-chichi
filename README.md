# ChiChi

下載專案：
git clone

For venv user:

創立虛擬環境：$ python -m venv .venv
進入虛擬環境：$ source .venv/bin/activate

- 啟動成功的話應該會看到小括號裡字樣
  $ (.venv) %

安裝套件: $ pip install -r requirements.txt

- 確認有安裝好套件
  - $ pip list

For poetry user:

安裝套件: $ poetry install
進入虛擬環境：$ poetry shell

- 啟動成功的話應該會看到小括號裡字樣
  $ (chichi-py3.13) %

- 確認 poetry 有安裝好套件
  - poetry show

安裝 MySQL
確保你的系統上已經安裝了 MySQL。如果還沒有，根據你的作業系統來安裝它。可利用 Homebrew 安裝:

mac 用戶

1. $ brew install mysql
2. 啟動 MySQL 服務
   - brew services start mysql
3. 設定 root 密碼（可選），初次啟動 MySQL，可以設定 root 密碼：
   - mysql_secure_installation
4. 執行以下命令進入 MySQL：

   - mysql -u root (-p) 沒設密碼可以忽略後面-p

5. 如果能進入 MySQL shell，表示安裝成功。

windows 用戶：

- windows 用戶可以去官網安裝[MySQL](https://dev.mysql.com/downloads/mysql/)

創建資料庫：

1. 進入 MySQL shell
2. 創建本機資料庫

- CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3. 執行以下 SQL 指令檢查權限：
   - SELECT host, user FROM mysql.user WHERE user = 'myuser';
4. 創建 'myuser' 用戶並授權
   - CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
   - SHOW GRANTS FOR 'myuser'@'localhost';
   - GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';
   - FLUSH PRIVILEGES;

確認 Django 是否可以執行

- $ python manage.py runserver

安裝 VScode MySQL 套件
名稱: [MySQL](https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2)

確認 MySQL 執行

1. 左邊側邊欄進入套件
2. 設定
   - host:localhost
   - port:3306
   - Username:myuser
   - Password:mypassword
3. 進入 MySQL 資料庫
