import streamlit as st
import pandas as pd
from agent.supply_chain_agent import SupplyChainAgent
from agent.regional_agent import RegionalAgent
from agent.industry_agent import IndustryAgent  # 确保路径正确
from agent.financial_agent import FinancialAgent
import tempfile
import os

st.set_page_config(page_title="行业智能分析", layout="wide")

st.title("行业智能分析助手")

# Tab切换：行业分析/地区分析
#tabs = st.tabs(["供应链分析", "地区分析"])
tabs = st.tabs(["供应链分析", "地区分析", "行业报告分析","财务报表分析"])

from pathlib import Path

# 当前脚本路径
current_file = Path(__file__).resolve()

# 项目根目录，假设 Q-MacroAgent 与 tavily-company-research 同级
project_root = current_file.parents[1]  # Q-MacroAgent/上一级 -> projects/

# ========== 供应链分析 Tab ==========
with tabs[0]:
    st.write("请上传包含企业因子和关联权重的CSV文件，系统将自动进行供应链&上下游趋势分析和预测。")
    uploaded_file = st.file_uploader("上传CSV文件", type=["csv"], key="industry_csv")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        df = pd.read_csv(tmp_path)
        st.subheader("数据预览")
        st.dataframe(df)
        st.subheader("供应链分析报告")
        with st.spinner("正在分析，请稍候..."):
            agent = SupplyChainAgent()
            report, graph_img_path = agent.analyze(tmp_path)
        st.success("分析完成！")
        st.markdown(f"```\n{report}\n```")
        # 可选：展示行业关系图
        # st.subheader("企业关系图可视化")
        # st.image(graph_img_path, caption="行业企业关系图")
    else:
        st.info("请先上传CSV文件。")

# ========== 地区分析 Tab ==========
# ========== 地区分析 Tab ========== 
with tabs[1]:
    st.write("请上传同一地区的企业JSON报告文件（可多选），或从知识库导入。系统将自动进行地区级企业网络与集群分析。")

    # 新增选项：是否从 knowledge_base 导入
    use_kb = st.checkbox("从知识库导入 JSON 文件", value=False)
    #knowledge_base_dir = r"d:\projects\tavily-company-research\knowledge_base\company_reports"
    knowledge_base_dir = project_root / "tavily-company-research" / "knowledge_base" / "company_reports"

    uploaded_jsons = []

    if use_kb:
        if os.path.exists(knowledge_base_dir):
            kb_files = [f for f in os.listdir(knowledge_base_dir) if f.endswith(".json")]

            # 关键词筛选
            filter_text = st.text_input("按关键词筛选知识库文件（可批量选中）", value="", key="region_kb_filter")
            if filter_text:
                matched_files = [f for f in kb_files if filter_text in f]
            else:
                matched_files = kb_files

            # 全选/取消全选
            select_all = st.checkbox("全选知识库文件", value=False, key="region_kb_all")
            default_selection = matched_files if select_all else []

            selected_files = st.multiselect(
                "选择知识库文件",
                options=kb_files,
                default=default_selection,
                key="region_kb_files"
            )

            for f in selected_files:
                file_path = os.path.join(knowledge_base_dir, f)
                class FileLike:
                    def __init__(self, path):
                        self.name = os.path.basename(path)
                        self._path = path
                    def getvalue(self):
                        with open(self._path, "rb") as _f:
                            return _f.read()
                uploaded_jsons.append(FileLike(file_path))
        else:
            st.warning(f"知识库文件夹不存在: {knowledge_base_dir}")
    else:
        uploaded_jsons = st.file_uploader(
            "上传企业JSON报告（可多选）", type=["json"], accept_multiple_files=True, key="region_jsons"
        )

    region_name = st.text_input("请输入地区名称（如：中国，北京市）", value="中国，北京市")

    if uploaded_jsons and region_name:
        # 将上传的JSON文件保存到临时目录
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for file in uploaded_jsons:
                safe_name = file.name.replace("，","_").replace(" ", "_")
                file_path = os.path.join(tmp_dir, safe_name)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
                file_paths.append(file_path)

            # 调试信息
            st.write("临时目录路径:", tmp_dir)
            st.write("文件列表:", file_paths)

            # 调用RegionalAgent分析
            with st.spinner("正在进行地区分析，请稍候..."):
                agent = RegionalAgent()
                report = agent.analyze_region(tmp_dir, region_name)

            if report:
                st.success("分析完成！")
                st.subheader("地区分析主要结论")
                st.markdown(f"**公司数量：** {report.get('companies_count', 0)}")
                st.markdown(f"**产业分布：** {report.get('industry_distribution', {})}")
                st.markdown(f"**产业集群强度：** {report.get('regional_insights', {}).get('economic_cluster_strength', {}).get('strength_level', '未知')}")
                st.markdown(f"**创新潜力：** {report.get('regional_insights', {}).get('innovation_potential', {}).get('potential_level', '未知')}")
                st.markdown(f"**协同分数：** {report.get('network_analysis', {}).get('synergy_score', '无')}")
                st.markdown(f"**枢纽企业：** {report.get('network_analysis', {}).get('hub_companies', [])}")
                st.markdown(f"**投资建议：** {report.get('investment_recommendations', {}).get('recommendation_level', '未知')}")

                if 'llm_report' in report:
                    st.subheader("AI智能分析报告")
                    st.markdown(report['llm_report'])

                graph_img = report.get('network_analysis', {}).get('graph_image', None)
                if graph_img and os.path.exists(graph_img):
                    st.subheader("企业网络关系图（精简版）")
                    st.image(graph_img, caption="地区企业关系网络")

                txt_path = f"regional_report_{region_name.replace('，','_')}.txt"
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        txt_content = f.read()
                    st.subheader("分析报告文本（可复制/下载）")
                    st.text_area("地区分析报告", txt_content, height=400)
                    st.download_button("下载txt报告", txt_content, file_name=txt_path)
            else:
                st.error("未生成地区分析报告，请检查数据格式或内容。")
    else:
        st.info("请上传企业JSON报告或选择知识库文件，并输入地区名称。")


# ========== 行业报告分析 Tab ==========
with tabs[2]:
    st.write("请上传一个行业下多个公司的JSON格式报告文件，或从知识库导入。系统将生成行业结构分析及智能摘要。")

    use_kb = st.checkbox("从知识库导入 JSON 文件", value=False, key="industry_kb")
    #knowledge_base_dir = r"d:\projects\tavily-company-research\knowledge_base\company_reports"
    knowledge_base_dir = project_root / "tavily-company-research" / "knowledge_base" / "company_reports"

    uploaded_jsons = []
    if use_kb:
        if os.path.exists(knowledge_base_dir):
            kb_files = [f for f in os.listdir(knowledge_base_dir) if f.endswith(".json")]

            filter_text = st.text_input("按关键词筛选知识库文件（可批量选中）", value="", key="industry_kb_filter")
            if filter_text:
                matched_files = [f for f in kb_files if filter_text in f]
            else:
                matched_files = kb_files

            select_all = st.checkbox("全选知识库文件", value=False, key="industry_kb_all")
            default_selection = matched_files if select_all else []

            selected_files = st.multiselect(
                "选择知识库文件",
                options=kb_files,
                default=default_selection,
                key="industry_kb_files"
            )

            for f in selected_files:
                file_path = os.path.join(knowledge_base_dir, f)
                class FileLike:
                    def __init__(self, path):
                        self.name = os.path.basename(path)
                        self._path = path
                    def getvalue(self):
                        with open(self._path, "rb") as _f:
                            return _f.read()
                uploaded_jsons.append(FileLike(file_path))
        else:
            st.warning(f"知识库文件夹不存在: {knowledge_base_dir}")
    else:
        uploaded_jsons = st.file_uploader(
            "上传行业公司报告（支持多文件上传）", type=["json"], accept_multiple_files=True, key="industry_jsons"
        )

    industry_name = st.text_input("请输入行业名称（如：证券、新能源、人工智能等）", value="证券")

    if uploaded_jsons and industry_name:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for file in uploaded_jsons:
                safe_name = file.name.replace("，","_").replace(" ", "_")
                file_path = os.path.join(tmp_dir, safe_name)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
                file_paths.append(file_path)

            st.write(f"已上传 {len(file_paths)} 个行业报告文件")
            output_json_path = os.path.join(tmp_dir, f"{industry_name}_industry_report.json")

            with st.spinner("正在生成行业分析报告，请稍候..."):
                agent = IndustryAgent()
                report = agent.analyze_industry(
                    industry_dir=tmp_dir,
                    industry_name=industry_name,
                    output_path=output_json_path
                )

            if report:
                st.success("行业分析完成！")
                st.markdown(f"📁 报告已保存至：`{output_json_path}`")

                st.subheader("行业结构摘要")
                st.markdown(f"**行业名称：** {report.get('industry_name', '未知')}")
                st.markdown(f"**公司数量：** {report.get('companies_count', 0)}")

                if "llm_report" in report:
                    st.subheader("LLM智能分析报告")
                    st.markdown(report["llm_report"])

                txt_path = output_json_path.replace(".json", ".txt")
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        txt_content = f.read()
                    st.subheader("分析报告文本（可复制/下载）")
                    st.text_area("行业分析报告", txt_content, height=400)
                    st.download_button("下载txt报告", txt_content, file_name=os.path.basename(txt_path))
            else:
                st.error("未生成分析报告，请检查上传的JSON文件或知识库文件格式是否正确。")
    else:
        st.info("请上传行业报告或选择知识库文件，并输入行业名称。")

# ========== 企业财务分析 Tab ==========
with tabs[3]:
    st.write("输入企业名称，系统将自动获取财务数据并生成专业分析报告")
    
    # 企业名称输入
    company_name = st.text_input("请输入企业名称（如：Apple Inc.）", value="Apple Inc.")
    
    # 高级选项
    with st.expander("高级选项"):
        max_results = st.slider("最大搜索结果数", 1, 10, 5)
        search_domains = st.multiselect(
            "限定搜索域名",
            options=["sec.gov", "investor.*", "finance.*", "nasdaq.com", "bloomberg.com"],
            default=["sec.gov", "investor.*", "finance.*"]
        )
    
    if st.button("生成财务分析报告", key="financial_analysis"):
        if company_name:
            with st.spinner("正在获取财务数据并生成分析报告..."):
                try:
                    # 初始化FinancialAgent
                    agent = FinancialAgent()
                    
                    # 第一步：获取财务数据
                    financial_data = agent.tavily_search(
                        company_name=company_name
                    )
                    
                    # 显示获取的财务数据摘要
                    st.subheader("获取的财务数据摘要")
                    st.json(financial_data)
                    
                    # 第二步：生成分析报告
                    analysis_report = agent.deepseek_financial_analysis(
                        company=company_name,
                        financial_data=financial_data
                    )
                    
                    # 显示分析报告
                    st.success("财务分析完成！")
                    st.subheader(f"{company_name} 财务分析报告")
                    st.markdown(analysis_report)
                    
                    # 提供下载功能
                    report_filename = f"{company_name.replace(' ', '_')}_financial_report.txt"
                    st.download_button(
                        label="下载财务分析报告",
                        data=analysis_report,
                        file_name=report_filename,
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"财务分析过程中出错: {str(e)}")
        else:
            st.warning("请输入企业名称")

#streamlit run web_app.py
# 我现在有两个项目（A B）需要合并为一个项目，其中项目A生成文件为.json格式的公司报告（多个），项目B则负责将报告投喂给LLM进行行业的分析；我的需求是当A完成时能够提供一个跳转的链接通往项目B；以下是项目A的代码：
