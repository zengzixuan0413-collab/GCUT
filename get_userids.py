import requests

# ===================== 【这里改成你自己的信息】 =====================
APP_KEY = "dingvqtvggnsle3mlouu"
APP_SECRET = "2BBn9g9PIExrmkPAYgDsYoKnwOUXndeySApXnFxk-rFGRGex63rTLLKSR1LziIGK"
DEPT_ID = 1  # 1 代表根部门，会查全公司员工
# ==================================================================

# 1. 获取 access_token
def get_token():
    url = f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}"
    res = requests.get(url)
    return res.json()["access_token"]

# 2. 获取部门下所有员工 userid
def get_users(access_token):
    # 这里修复成 GET 请求，就不会报 43001 了
    url = f"https://oapi.dingtalk.com/user/simplelist?access_token={access_token}&department_id={DEPT_ID}"
    res = requests.get(url)
    return res.json()

# 3. 执行并打印结果
if __name__ == "__main__":
    try:
        token = get_token()
        result = get_users(token)
        
        if result["errcode"] == 0:
            print("===== 员工ID列表 =====")
            for user in result["userlist"]:
                print(f"姓名：{user['name']} \t UserID：{user['userid']}")
        else:
            print("错误：", result)
    except Exception as e:
        print("出错啦：", e)