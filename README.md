
# 简介

> 通过 FastAPI 接入 FastGPT 平台的数据收集和数据总结模型。信息数据收集模型可接入微信、钉钉、飞书，对群聊聊天数据或者个人聊天数据进行收集。数据总结模型根据用户提问需求调用 AI 总结对应所需日期的数据总结。例如：8 月 14 日群聊中有多条重要未读消息，可询问数据总结模型，将 8 月 14 日的数据总结好。



基于大模型搭建的聊天机器人，同时支持微信公众号、企业微信应用、飞书、钉钉等接入。可选择 GPT-3.5/GPT-4.0/Claude/文心一言/讯飞星火/通义千问/Gemini/GLM-4/Claude/Kimi/LinkAI，能处理文本、语音和图片，访问操作系统和互联网，支持基于自有知识库进行定制企业智能客服。
最新版本支持的功能如下：
- ✅ **多端接入：** 支持微信公众号、企业微信、飞书、钉钉等多种接入方式
- ✅ **智能对话：** 处理文本、语音和图片，支持多轮会话上下文记忆
- ✅ **数据总结：** 基于 AI 的自动化数据总结功能
- ✅ **可定制化：** 支持基于自有知识库定制企业智能客服

[聊天机器人项目链接](https://github.com/zhayujie/chatgpt-on-wechat)

## 声明

1. 本项目仅用于技术研究和学习，使用本项目时需遵守所在地法律法规、相关政策以及企业章程，禁止用于任何违法或侵犯他人权益的行为。
2. 境内使用该项目时，请使用国内厂商的大模型服务，并进行必要的内容安全审核及过滤。
3. 任何个人、团队和企业，无论以何种方式使用该项目、对何对象提供服务，所产生的一切后果，本项目均不承担任何责任。

## 一、准备

1. **FastGPT 账号注册**  
   创建好账号后新创建两个 AI 应用：数据收集和数据总结模型。在数据收集模型应用中创建 API Key 并保存下来。

2. **运行环境**  
   支持 Linux、MacOS、Windows 系统（可在 Linux 服务器上长期运行），同时需要安装 `python`。  
   > 建议 Python 版本在 3.7.1 ~ 3.9.X 之间，推荐 3.8 版本，3.10 及以上版本在 MacOS 可用，其他系统上不确定能否正常运行。

### (1) 克隆项目代码

下载 GitHub 项目。
(https://github.com/respectheadsome/FastAPI-.git)

### (2) 安装核心依赖 (必选)

```bash
pip3 install -r requirements.txt
```

## 二、配置

### (1) .env 文件

`.env` 文件中需要配置 `API_URL` 和 `API_Key`。

### (2) 数据库的创建

```sql
CREATE TABLE conversations (
    id INTEGER NOT NULL,
    date VARCHAR,
    message VARCHAR, 
    year INTEGER, 
    month INTEGER, 
    day INTEGER,
    PRIMARY KEY (id)
);
CREATE INDEX ix_conversations_id ON conversations (id);
CREATE INDEX ix_conversations_date ON conversations (date);
```

### (3) 模型编排

数据收集和数据总结模型的高级编排如下：

<center>
<img src="https://s2.loli.net/2024/08/16/ku6STjwrMAn241P.png" alt="数据收集模型" width="600"/>  
<img src="https://s2.loli.net/2024/08/16/KcyejRgb5zWoBxi.png" alt="数据总结模型" width="600"/>  
<img src="https://s2.loli.net/2024/08/16/YNG5Av4Oj8fDUeM.png" alt="总结示例" width="1000"/>
</center>

## 三、运行

在 `fastgpt` 目录下执行：

```bash
uvicorn fastgpt.main:app --reload --host 0.0.0.0
```

同时在另一个终端执行：

```bash
streamlit run streamlit_app.py
```

可视化数据库中的数据，进行查询、删除操作。

### FastGPT 上运行模型

#### （1）数据收集

<center>
<img src="https://s2.loli.net/2024/08/16/mbK1BqN63Osnx4Q.png" alt="数据总结" width="600"/>
</center>

#### （2）数据总结

<center>
<img src="https://s2.loli.net/2024/08/16/CucUQ9hWbgy2vXZ.png" alt="数据收集" width="600"/>
</center>

**不足：目前数据收集无法归纳群聊名和用户名，所以数据总结模型无法总结特定群或者用户的数据。**
