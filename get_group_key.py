import requests

# 你的信息
APP_KEY = "dingvqtvggnsle3mlouu"
APP_SECRET = "2BBn9g9PIExrmkPAYgDsYoKnwOUXndeySApXnFxk-rFGRGex63rTLLKSR1LziIGK"
OP_USER_ID = "01424704215126096223"  # 这是你自己的UserID（曾子萱）

def get_access_token():
    url = f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}"
    res = requests.get(url)
    data = res.json()
    if data.get("errcode") != 0:
        raise Exception(f"获取token失败: {data}")
    return data["access_token"]

def list_all_attendance_groups(token):
    url = f"https://oapi.dingtalk.com/topapi/attendance/group/list?access_token={token}"
    
    # 这里修复：必须传 op_user_id
    data = {
        "op_user_id": OP_USER_ID
    }
    
    res = requests.post(url, json=data)
    result = res.json()
    
    if result.get("errcode") != 0:
        raise Exception(f"获取考勤组失败: {result}")
    
    print("\n===== 你的考勤组信息 =====")
    groups = result.get("result", {}).get("groups", [])
    for g in groups:
        print(f"组名：{g['name']}")
        print(f"GROUP_KEY = \"{g['group_key']}\"\n")

if __name__ == "__main__":
    try:
        token = get_access_token()
        list_all_attendance_groups(token)
    except Exception as e:
        print("\n出错：", e)