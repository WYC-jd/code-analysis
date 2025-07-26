import requests, json
from bs4 import BeautifulSoup

session = requests.Session()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

# 清理 HTML 内容，提取纯文本
def clean_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def get_problem_by_id(question_id):
    """
    根据题目编号获取题目详细信息
    """
    # 获取所有题目列表
    url = "https://leetcode.com/api/problems/all/"
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    resp = session.get(url, headers=headers, timeout=10)
    
    question_list = json.loads(resp.content.decode('utf-8'))
    
    # 查找对应编号的题目
    question_slug = None
    for question in question_list['stat_status_pairs']:
        if question['stat']['question_id'] == question_id:
            question_slug = question['stat']['question__title_slug']
            break
    
    if not question_slug:
        print(f"未找到编号为 {question_id} 的题目")
        return

    # 获取题目详细信息
    return get_problem_details(question_slug)

def get_problem_details(question_slug):
    """
    根据题目的 slug 获取题目详细信息
    """
    url = "https://leetcode.com/graphql"
    query = '''query getQuestionDetail($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            questionTitle
            questionTitleSlug
            content
            difficulty
            stats
            similarQuestions
            categoryTitle
            topicTags {
                name
                slug
            }
        }
    }'''

    params = {
        'operationName': "getQuestionDetail",
        'variables': {'titleSlug': question_slug},  # 使用题目的 slug 获取信息
        'query': query
    }
    
    json_data = json.dumps(params).encode('utf-8')
    headers = {
        'User-Agent': user_agent,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': f'https://leetcode.com/problems/{question_slug}'
    }
    
    resp = session.post(url, data=json_data, headers=headers, timeout=10)
    
    if resp.status_code == 200:
        content = resp.json()
        question = content['data']['question']
        
        cleaned_description = clean_html_content(f"{question['content']}")#[:300]截取前300个字符
        # 解析 JSON 数据
        similar_questions = json.loads(f"{question['similarQuestions']}")

        # 打印题目基本信息
        print(f"题目 ID: {question['questionId']}")
        print(f"题目名称: {question['questionTitle']}")
        print(f"标签: {', '.join([tag['name'] for tag in question['topicTags']])}")

        # 返回题目描述
        return cleaned_description, question['questionId'], question['questionTitle']

    else:
        print(f"请求失败，状态码: {resp.status_code}")
        return



