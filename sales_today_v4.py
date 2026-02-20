import csv

class SalesAnalyzer:

    def __init__(self):
        self.data = self.read_sales_today()

    def read_sales_today(self):
        try:
            with open("sales_today.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            print("sales_today.csv が見つかりません")
            return []


    def total_by_column(self, column_name, data=None):
        if data is None:
            data = self.data
        result = {}
        for row in data:
            key = row[column_name] # 指定された列を取得
            try:
                price = int(row["単価"]) # 単価列を取得
                quantity = int(row["数量"]) # 数量列を取得
            except ValueError:
                print("数値変換エラー:", row)
                continue
                
            result[key] = result.get(key, 0) + price * quantity
        return result # 指定された列ごとの合計を返す

    def export_csv(self, filename, header1, header2, result):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer =csv.writer(f)
            writer.writerow([header1, header2])
            for key, value in result.items():
                writer.writerow([key, value])

    def filter_by_period(self, start_date, end_date):
        filtered =[]
        for row in self.data:
            date = row["日付"]
            if start_date <= date <= end_date: # datetaimeオブジェクト同士の比較に変更
                filtered.append(row)
        return filtered



    def menu(self):
        while True:

            print("\n1: 商品別")
            print("2: 日付別")
            print("3: 支払方法別")
            print("4: 担当者別")
            print("5: 店舗別")
            print("6: 期間指定で集計")
            print("0: 終了")

            choice = input("番号を選んでください: ")

            if choice == "0":
                print("終了します")
                break

            # ---- 通常集計 ----
            if choice in ["1", "2", "3", "4", "5"]:

                if choice == "1":
                    column = "商品"
                elif choice == "2":
                    column = "日付"
                elif choice == "3":
                    column = "支払方法"
                elif choice == "4":
                    column = "担当者"
                elif choice == "5":
                    column = "店舗"

                result = self.total_by_column(column)

            # ---- 期間指定集計 ----
            elif choice == "6":

                start = input("開始日を入力してください (YYYY-MM-DD): ")
                end = input("終了日を入力してください (YYYY-MM-DD): ")

                print("1: 商品別")
                print("2: 日付別")
                print("3: 支払方法別")
                print("4: 担当者別")
                print("5: 店舗別")

                sub_choice = input("集計方法を選んでください: ")

                if sub_choice == "1":
                    column = "商品"
                elif sub_choice == "2":
                    column = "日付"
                elif sub_choice == "3":
                    column = "支払方法"
                elif sub_choice == "4":
                    column = "担当者"
                elif sub_choice == "5":
                    column = "店舗"
                else:
                    print("無効な番号です")
                    continue

                filtered = self.filter_by_period(start, end)
                result = self.total_by_column(column, filtered)

            else:
                print("無効な番号です")
                continue

            # ---- 結果表示 ----
            for key, total in sorted(result.items(), key=lambda x: x[1], reverse=True):
                print(f"{key}: {total} 円")

            save = input("CSV保存しますか？ (y/n): ")

            if save == "y":
                filename = f"{column}_total_today.csv"
                self.export_csv(filename, column, "合計金額", result)
                print(f"{filename} を作成しました")





if __name__ == "__main__":
    app = SalesAnalyzer()
    app.menu()
