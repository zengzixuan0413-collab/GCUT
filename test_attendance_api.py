import requests
from datetime import datetime

# ===================== 你的信息（已填好）=====================
APP_KEY = "dingvqtvggnsle3mlouu"
APP_SECRET = "2BBn9g9PIExrmkPAYgDsYoKnwOUXndeySApXnFxk-rFGRGex63rTLLKSR1LziIGK"
# 你的UserID（曾子萱），替换成你自己的
OP_USER_ID = "01424704215126096223"
# 要查询的员工ID列表（先查你自己，测试用）
USER_ID_LIST = ["01424704215126096223"]
# ==========================================================

def get_access_token():
    url = f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}"
    res = requests.get(url)
    data = res.json()
    if data.get("errcode") != 0:
        raise Exception(f"获取token失败: {data}")
    return data["access_token"]

def get_attendance_records(token):
    # 钉钉拉取考勤记录的正确接口
    url = f"https://oapi.dingtalk.com/topapi/attendance/list?access_token={token}"
    
    # 今天的日期，格式：yyyy-MM-dd HH:mm:ss
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 查询今天0点到现在的打卡记录
    data = {
        "op_userid": OP_USER_ID,
        "userid_list": USER_ID_LIST,
        "check_date_from": f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00",
        "check_date_to": today
    }
    
    res = requests.post(url, json=data)
    return res.json()

if __name__ == "__main__":
    try:
        print("正在获取access_token...")
        token = get_access_token()
        print("正在拉取考勤记录...")
        result = get_attendance_records(token)
        print("\n=== API返回结果 ===")
        print(result)
        
        if result.get("errcode") == 0:
            records = result.get("recordresult", [])
            if records:
                print(f"\n✅ 成功拉取到 {len(records)} 条考勤记录！")
                for r in records:
                    print(f"姓名：{r['name']} 打卡时间：{r['checkTime']} 状态：{r['checkType']}")
            else:
                print("\n❌ 拉取成功，但暂无考勤数据（请先在钉钉App打卡）")
        else:
            print(f"\n❌ 接口调用失败: {result.get('errmsg')}")
            
    except Exception as e:
        print("\n❌ 出错:", e)