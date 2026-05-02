const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

// 你的钉钉信息（已帮你填好）
const DINGTALK = {
  APP_KEY: "dingvqtvggnsle3mlouu",
  APP_SECRET: "2BBn9g9PIExrmkPAYgDsYoKnwOUXndeySApXnFxk-rFGRGex63rTLLKSR1LziIGK",
  AGENT_ID: "4470561814"
};

// 获取token
async function getToken() {
  const r = await axios.get("https://oapi.dingtalk.com/gettoken", {
    params: { appkey: DINGTALK.APP_KEY, appsecret: DINGTALK.APP_SECRET }
  });
  return r.data.access_token;
}

// 获取用户列表
async function getUserIds() {
  const t = await getToken();
  const r = await axios.post("https://oapi.dingtalk.com/topapi/user/listid", 
    { dept_id: 1 }, 
    { params: { access_token: t } }
  );
  return r.data.result?.userid_list || [];
}

// 考勤接口
app.post('/api/dingtalk/attendance', async (req, res) => {
  try {
    const t = await getToken();
    const users = await getUserIds();
    const { workDateFrom, workDateTo } = req.body;

    const r = await axios.post("https://oapi.dingtalk.com/attendance/listRecord", {
      userIds: users,
      checkDateFrom: workDateFrom,
      checkDateTo: workDateTo
    }, { params: { access_token: t } });

    res.json(r.data.recordresult || []);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// 启动
app.listen(3000, () => {
  console.log("✅ 后端启动成功：http://localhost:3000");
});