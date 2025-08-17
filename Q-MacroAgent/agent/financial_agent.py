import os
import requests
import json
import time

class FinancialAgent:
    def tavily_search(self, company_name: str):
        """使用Tavily搜索公司财务信息"""
        self.url = os.getenv("TAVILY_API_URL")
        payload = {
            "api_key": os.getenv("TAVILY_API_KEY"),
            "query": f"{company_name} financial reports, earnings, revenue, profit, annual report",
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": True,
            "max_results": 5,
            "include_domains": ["sec.gov", "investor.*", "finance.*"]
        }
        
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Tavily搜索失败: {response.status_code} {response.text}")
        
        data = response.json()
        
        # 提取关键财务信息（可根据需要扩展）
        financial_data = {
            "company": company_name,
            "sources": [result["url"] for result in data.get("results", [])],
            "financial_info": []
        }
        
        for result in data.get("results", []):
            if "revenue" in result["content"].lower() or "earnings" in result["content"].lower():
                financial_data["financial_info"].append({
                    "url": result["url"],
                    "title": result["title"],
                    "content": result["content"][:1000]  # 截取部分内容
                })
        
        return financial_data

    def deepseek_financial_analysis(self, company: str, financial_data: dict):
        """使用DeepSeek生成财务分析报告"""
        self.url = os.getenv("DEEPSEEK_API_URL")
        self.key = os.getenv("DEEPSEEK_API_KEY")
        # 构建分析提示词
        prompt = f"""
        你是一位资深财务分析师，请基于以下信息为{company}生成一份结构化财务分析报告：
        {json.dumps(financial_data, indent=2)}
        
        报告需包含以下部分：
        1. 以表格形式给出财务表现概览（收入、利润、增长趋势）
        2. 关键财务指标分析
        3. 风险因素与机遇
        4. 分析总结（未来展望）
        
        注意：
        -使用最新财务数据
        -使用专业财务术语
        -保持客观中立，不要胡乱编造
        -表述需要简洁清晰，但也要有足够的分析
        -给明数据来源：[提供的搜索结果]
        """
        
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一位专注财务分析的AI助手"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 2000
        }
        
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"DeepSeek API调用失败: {response.status_code} {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]