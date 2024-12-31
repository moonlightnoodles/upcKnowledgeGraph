import time
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import pandas as pd
import numpy as np
# import snowflake.connector
import streamlit_option_menu
from streamlit_option_menu import option_menu
from scarper import scarper_tools



@st.cache_resource
def set_entities_and_relations():
    nodes = []
    edges = []
    # 获取企业名称
    name_entity_set = set(get_entity("股票名称"))
    field_entity_set = set(get_entity("行业分类"))
    relation_list = get_relation()
    for entity_dot in name_entity_set:
        nodes.append(Node(id=entity_dot,
                          label=entity_dot,
                          size=25,
                          shape='dot'
                          )
                     )

    for entity_dot in field_entity_set:
        nodes.append(Node(id=entity_dot,
                          label=entity_dot,
                          size=25,
                          shape='dot',
                          color='red'
                          )
                     )

    for (name, field) in relation_list:
        edges.append(Edge(source=name,
                          target=field,
                          label="隶属于",
                          )
                     )
    return nodes, edges


@st.cache_data
def get_entity(column_name):
    file_path = "data/business_data_1.csv"
    entity_df = pd.read_csv(file_path)
    # column_data = entity_df[["股票名称", "行业分类"]]
    # entity_tuple = [tuple(row) for row in column_data.values]
    entity_list = entity_df[column_name].tolist()
    return entity_list


@st.cache_data
def get_relation():
    file_path = "data/business_data_1.csv"
    entity_df = pd.read_csv(file_path)
    column_data = entity_df[["股票名称", "行业分类"]]
    entity_tuple = [tuple(row) for row in column_data.values]
    # entity_list = entity_df["股票名称"].tolist() + entity_df["行业分类"].tolist()
    return entity_tuple


@st.dialog("Cast your nodes")
def add_node(nodes,edges):
    with st.form("my_form"):
        node_a = st.text_input("输入第一个节点")
        relationship = st.text_input("输入关系")
        node_b = st.text_input("输入第二个节点")
        submitted = st.form_submit_button("Submit")
        if submitted:
            nodes.append(Node(id=node_a,
                              label=node_a,
                              size=25,
                              shape='dot',
                              color='green'))
            nodes.append(Node(id=node_b,
                              label=node_b,
                              size=25,
                              shape='dot',
                              color='orange'))
            edges.append(Edge(source=node_a,
                              target=node_b,
                              label=relationship,
                              )
                         )
            st.rerun()

st.set_page_config(
    page_title="知识图谱大作业",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# i = 0
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["获取股票数据", "实体与关系抽取", "知识图谱"],
        icons=["house", "gear", "activity"],
        # icons=["house", "gear", "activity", "snowflake", "envelope"],
        menu_icon="cast",
        default_index=0,
        # orientation = "horizontal",
    )
if selected == "获取股票数据":
    st.header('爬取原始数据')
    # Create a row layout
    c1, c2 = st.columns([1,1])
    c3, c4 = st.columns(2)

    with st.container():
        c1.write()
        c2.write()

    with c1:
        prompt = st.text_area(
            ":orange[**输入网址，爬取你的金融数据，本次实验的网址为 https://s.askci.com/stock/ ✍🏾**]",
            value="https://s.askci.com/stock/")
        if st.button(
            "爬取数据", type="primary", use_container_width=True):
            st.write("submit triggerred")
            st.write(scarper_tools.hello_hjy())
        st.link_button("访问该链接", "https://s.askci.com/stock", use_container_width=True)
        st.image("asset/website.png")
    with c2:
        prompt = st.subheader(
            "个人信息:sunglasses:", divider=True)
        col1, col2 = st.columns(2)
        col1.metric("姓名", "侯劲宇")
        col2.markdown("学号：2207020425")
        col2.markdown("班级：软件2204")

        st.image("asset/upc.png")
        # if st.button(
        #     "查看结果", type="primary", use_container_width=True):
        #     df = pd.read_csv('./data/business_data_1.csv')
        #     st.dataframe(df.head())

    with st.container():

        if st.button("查看爬取数据/下一页", type="primary"):
            i = 1
            # i %= 35
            df = pd.read_csv(f'data/business_data_{i}.csv')
            st.dataframe(df)

            @st.cache_data
            def convert_df(dataframe):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return dataframe.to_csv().encode("utf-8")

            csv = convert_df(df)
            st.download_button(
                # label="Download data as CSV",
                label="下载",
                data=csv,
                file_name="large_df.csv",
                mime="text/csv",
            )
        # 序号, 股票代码, 股票名称, 公司全称, 上市日期, 招股书, 公司财报, 行业分类, 主营业务
        else:
            column_names = ['序号', '股票代码', '股票名称', '公司全程', '上市日期',
                        '招股书', '公司财报', '行业分类', '主营业务']
            empty_df = pd.DataFrame(columns=column_names)
            st.dataframe(empty_df)
        import streamlit as st
if selected == "实体与关系抽取":

    from extraction.extraction_tools_jieba import extract_entity, extract_relation
    # st.subheader(f"**You Have selected {selected}**")

    entity_extraction_column, relation_extraction_column = st.columns(2)
    with entity_extraction_column:
        st.subheader("实体抽取")
        input_text = st.text_area(
            label="输入文本",
            placeholder="输入您的文本,"
                        "如：中国银行的主要业务是贷款",
            label_visibility='collapsed'
            # "我们将对文本段进行实体抽取"
        )
        # st.write(input_text)
        top_K = st.select_slider(
            ":red[**Define variable top_K**]",
            options=[
                1,
                5,
                10,
                15,
                20,
            ],
        )
        # st.write(top_K)
        if st.button("提取实体"):
            if input_text is not None and input_text != "":
                # 添加进度条
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()

                # with st.status("正在处理..."):
                #     time.sleep(1)
                # st.write(type(input_text))
                entity_extraction_result = extract_entity(input_text, top_k=top_K)
                entity_extraction_df = pd.DataFrame(entity_extraction_result, columns=["实体", "权重"])
                st.dataframe(entity_extraction_df,use_container_width=True, hide_index=True)
                # st.markdown(entity_extraction_result)
                # result = st.text_area(":orange[**运算结果**]", value=entity_extraction_result)
            else:
                st.error('文本为空，请输入文本', icon="🚨")
    with relation_extraction_column:
        st.subheader("关系抽取")
        relation_input_text = st.text_area(
            label="输入文本",
            placeholder="输入您的文本,"
                        "如：我爱喝橙汁",
            label_visibility='collapsed'
            # "我们将对文本段进行实体抽取"
        )
        # st.write(input_text)
        relation_top_K = st.select_slider(
            ":red[**Define variable top_K**]",
            options=[
                1,
                5,
                10,
            ],
        )
        # st.write(top_K)
        if st.button("提取关系"):
            if relation_input_text is not None and relation_input_text != "":
                # 添加进度条
                # relation_progress_text = "Operation in progress. Please wait."
                # relation_my_bar = st.progress(0, text=relation_progress_text)
                #
                # for percent_complete in range(100):
                #     time.sleep(0.01)
                #     relation_my_bar.progress(percent_complete + 1, text=relation_progress_text)
                # time.sleep(1)
                # relation_my_bar.empty()

                # with st.status("正在处理..."):
                #     time.sleep(1)
                # st.write(relation_input_text)
                relation_extraction_result = extract_relation(relation_input_text, top_k=relation_top_K)
                # st.markdown(relation_top_K)
                # st.markdown(relation_extraction_result)
                if relation_extraction_result is not None and relation_extraction_result != "":
                    relation_result = st.text_area(":orange[**运算结果**]", value=relation_extraction_result)
                else:
                    st.info("未检测到关系词")
            else:
                st.error('文本为空，请输入文本', icon="🚨")
if selected == "知识图谱":
    with st.container():

        nodes, edges = set_entities_and_relations()

            # st.write("nihaoaaa")
        config = Config(width=1000,
                        height=600,
                        directed=True,
                        physics=True,
                        # physics=False,
                        hierarchical=False,
                        # **kwargs
                        )
        return_value = agraph(nodes=nodes,
                              edges=edges,
                              config=config)

        _, button_place, button_place_right = st.columns([0.7, 1, 1])
        with button_place:
            st.markdown('''
                :rainbow[滑动鼠标滚轮缩小全局视图以查找知识图谱]     
                :rainbow[滑动鼠标滚轮放大知识图谱细节]
            ''')
            if st.button("添加新节点与关系",type="primary", use_container_width=True):
                add_node(nodes,edges)
        with button_place_right:
            st.markdown("")
            st.markdown(":blue-background[新节点用:green[绿色]和 :orange[橙色]表示]")
        # 例子
        # edges.append(Edge(source="Captain_Marvel",
        #                   label="friend_of",
        #                   target="Spiderman",
        #                   # **kwargs
        #                   )
        #              )
        #
        #
        # nodes.append(Node(id="Spiderman",
        #                   label="Peter Parker",
        #                   size=25,
        #                   shape="dot",
        #                   # image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png"
        #                   )
        #              )  # includes **kwargs
        # nodes.append(Node(id="Captain_Marvel",
        #                   label="Captain Marvel",
        #                   size=25,
        #                   shape="dot",
        #                   # image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png"
        #                   )
        #              )
        # edges.append(Edge(source="Captain_Marvel",
        #                   label="friend_of",
        #                   target="Spiderman",
        #                   # **kwargs
        #                   )
        #              )


    # st.button("nihao")
