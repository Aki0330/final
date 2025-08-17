好的，我帮你把两个子项目整合成一个总 README，同时加入你提到的 Conda 环境配置与启动说明，保持专业、清晰、可操作性强的风格。以下是整合后的示例文档：

---

# AI 驱动的行业与公司智能分析系统

本项目整合了 **行业智能分析系统** 与 **Q-MacroAgent**，构建一个面向行业、地区及单公司多维度分析的智能平台。系统支持企业关系网络分析、产业集群识别、量子特征分析、多 Agent 公司研究以及自动报告生成。

---

## 🔹 核心功能

### 1. 行业与地区分析

* **企业因子分析**：基于 CSV 数据进行企业指标计算。
* **企业关系网络**：构建企业关系图并进行可视化。
* **产业集群识别**：识别行业或地区的企业集群。
* **枢纽企业识别**：量化企业协同效应，找出核心企业。
* **量子特征分析**：基于量子特征向量进行企业相似度分析。
* **AI智能分析**：使用 DeepSeek LLM 自动生成投资建议和风险分析报告。

### 2. 智能公司研究（Q-MacroAgent）

* **自动收集数据**：公司财务、新闻、竞争信息。
* **多维度分析**：行业趋势、竞争对手、市场动态。
* **报告生成**：生成专业 PDF 研究报告。
* **多 Agent 协作**：使用 LangGraph 构建多 Agent 工作流，实现自动化分析。
* **Web 界面交互**：直观展示分析结果并支持实时操作。

### 3. 可视化功能

* 企业关系网络图（精简版）
* 产业集群热力图
* 量子特征向量分析

---

## 💻 技术栈

* **后端**：Python 3.9.18, NetworkX, NumPy, Pandas, FastAPI
* **AI**：DeepSeek LLM, LangChain, LangGraph, 量子特征分析
* **前端**：Streamlit / React + TypeScript + Tailwind CSS
* **可视化**：Matplotlib, Graphviz
* **数据格式**：CSV, JSON

---

## 🗂 项目结构

```
项目根目录/
├── agent/                  # 智能代理模块
│   ├── industry_agent.py
│   ├── regional_agent.py
│   └── supply_chain_agent.py
├── tools/                  # 数据与图分析工具
│   ├── data_loader.py
│   ├── graph_utils.py
│   ├── regional_loader.py
│   ├── regional_graph_utils.py
│   └── IndustryReport_loader.py
├── llm/                    # 大语言模型接口
│   └── deepseek_llm.py
├── configs/
│   └── config.py           # 环境配置
├── data/                   # 数据存储
├── backend/                # Q-MacroAgent 后端
│   ├── classes/
│   ├── nodes/
│   ├── services/
│   └── utils/
├── ui/                     # 前端代码
│   ├── src/
│   │   ├── components/
│   │   └── types/
├── static/                 # 静态资源
├── knowledge_base/         # 知识库
├── web_app.py              # 行业/地区分析前端
├── main.py                 # 命令行入口
├── run_all.py              # 启动整个系统
└── requirements.txt        # 依赖包
```

---

## ⚙️ 安装与运行

### 1. 环境要求

* **Python 3.9.18**
* **Anaconda**

### 2. 配置 Conda 环境

```bash
# 创建虚拟环境
conda create -n py3918 python=3.9.18 -y

# 激活虚拟环境
conda activate py3918
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件，并配置：

```
TAVILY_API_KEY=your_api_key
TAVILY_API_URL=your_api_url
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_API_URL=your_api_url
MODEL_NAME=your_model_name
```
---

### ⚙️ 环境变量配置示例

在项目根目录创建 `.env` 文件，并参考以下示例填写：

```env
# Tavily API 配置
TAVILY_API_KEY=your_tavily_api_key
TAVILY_API_URL=https://api.tavily.com

# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions

# 模型名称（用于 DeepSeek LLM）
MODEL_NAME=your_model_name

# 可选：OpenAI API（Q-MacroAgent 可选功能）
OPENAI_API_KEY=your_openai_api_key
```

**说明**：

* `TAVILY_API_KEY`、`DEEPSEEK_API_KEY`、`OPENAI_API_KEY`：请替换为你自己的 API Key。
* `TAVILY_API_URL` 和 `DEEPSEEK_API_URL` 默认保持示例值即可。
* `MODEL_NAME` 根据你的 DeepSeek 模型选择填写。
* OPENAI\_API\_KEY 可选，仅用于 Q-MacroAgent 中调用 OpenAI 模型的功能。

---



### 5. 启动系统

```bash
# 启动整个系统
python run_all.py
```

> 运行后，终端会显示本地访问链接，点击即可在浏览器中访问 Web 界面。

---

## 📝 使用示例

### 行业分析

1. 上传 CSV 企业因子数据。
2. 选择“行业分析”模块。
3. 系统生成企业网络、集群分析及投资建议报告。

### 地区分析

1. 上传同地区多家企业 JSON 报告。
2. 输入地区名称，系统生成地区企业网络和产业集群分析。
3. 输出协同效应分数及枢纽企业识别。

### 单公司研究（Q-MacroAgent）

1. 输入公司名称，可选填写行业、总部位置、网址。
2. 点击“开始研究”，系统自动收集数据、多轮分析。
3. 生成 PDF 研究报告，可在线浏览或下载。

---

## 🔗 协同使用说明

1. 先使用行业/地区分析系统识别核心企业与产业集群。
2. 将关键企业导入 Q-MacroAgent 进行深度研究。
3. 量化指标（协同分数、枢纽节点）可作为 Q-MacroAgent 报告分析的重要参考。

---

## 📄 贡献指南

欢迎提交 Issue 或 Pull Request 来改进项目。

## 📜 许可证

MIT License

## 📬 联系方式

通过 GitHub Issues 提交问题或建议。

---


