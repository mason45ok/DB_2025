import mysql.connector
import faulthandler
faulthandler.enable()
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="@Mason45ok",
        database="db_2025"
    )
    print("連線成功")
    conn.close()
except mysql.connector.Error as err:
    print("MySQL 錯誤:", err)
except Exception as e:
    print("其他錯誤:", e)