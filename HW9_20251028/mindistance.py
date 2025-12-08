def min_edit_distance(str1, str2):
    """
    計算兩個字串之間的最小編輯距離 (Levenshtein Distance)
    使用動態規劃 (Dynamic Programming)
    """
    m = len(str1)
    n = len(str2)

    # 1. 建立一個二維表格 (Matrix) 來儲存計算結果
    # dp[i][j] 代表 str1 的前 i 個字與 str2 的前 j 個字的最小距離
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # 2. 初始化表格的第一列與第一行
    # 如果 str2 是空字串，str1 要變成它需要刪除所有字元 (距離為 i)
    for i in range(m + 1):
        dp[i][0] = i
    # 如果 str1 是空字串，要變成 str2 需要插入所有字元 (距離為 j)
    for j in range(n + 1):
        dp[0][j] = j

    # 3. 開始填表 (由左上往右下)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            # 如果字元相同，不需要做任何操作，距離維持不變
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                # 如果字元不同，替換操作的成本為 1
                cost = 1
            
            # 核心狀態轉移方程式：取三者中的最小值
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # 刪除 (Deletion)
                dp[i][j - 1] + 1,      # 插入 (Insertion)
                dp[i - 1][j - 1] + cost # 替換 (Substitution)
            )

    # 4. 表格右下角的值即為最終結果
    return dp[m][n]

# --- 測試程式 ---
if __name__ == "__main__":
    s1 = ""
    s2 = "sitting"
    
    distance = min_edit_distance(s1, s2)
    
    print(f"字串 1: {s1}")
    print(f"字串 2: {s2}")
    print(f"最小編輯距離: {distance}")
    
    # # 驗證邏輯：
    # # 1. k -> s (替換)
    # # 2. e -> i (替換)
    # # 3. 尾部插入 g (插入)
    # # 總共 3 步

    # # --- 這就是自動測試 ---
    # # 測試 1: 測試 kitten 變 sitting
    # result1 = min_edit_distance("kitten", "sitting")
    # assert result1 == 3, f"錯誤！預期是 3，但算出 {result1}"
    
    # # 測試 2: 測試 kitte 變 sitting
    # result2 = min_edit_distance("kitte", "sitting")
    # assert result2 == 4, f"錯誤！預期是 4，但算出 {result2}"

    # # 測試 3: 測試完全一樣的字串 (距離應為 0)
    # result3 = min_edit_distance("abc", "abc")
    # assert result3 == 0, f"錯誤！預期是 0，但算出 {result3}"

    # print("恭喜！所有測試都通過了！(All tests passed)")