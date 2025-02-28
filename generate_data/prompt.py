import re
from fastapi import HTTPException
import json

def prompt_relevance(first_text_order, second_text_order, option_oder: str = None):
	prompt = f'''
		以下のフォーマットで、短文1（Q）と短文2（D）のペアを100個生成してください。
		また、それぞれのペアに関連度スコア（0.0〜1.0）を付けてください。

		フォーマット:
		```json
		[
			{{
				"Q": "短文1",
				"D": "短文2",
				"score": 0.9
			}},
			{{
				"Q": "短文1",
				"D": "短文2",
				"score": 0.3
			}}
		]

		制約:
		- 50ペアは **高スコア（0.8〜1.0）** で、明確に関連があるものを作成する。
		- 50ペアは **低スコア（0.0〜0.4）** で、関連が薄いものを作成する。
		- **Q は{first_text_order}（20〜40文字）。**
		- **D は{second_text_order}（20〜40文字）。**
		- **ランダム性を持たせて、できるだけ多様な組み合わせを作る**。
		
    {option_oder}

		100ペアを生成してください。
	'''
	return prompt

def prompt_score(feature, option_oder: str = None):
	prompt = f'''
		以下のフォーマットで、短文とスコアを100個生成してください。  
		また、それぞれのペアに「{feature}の度合（0.0〜1.0）」のスコアを付けてください。

		### **フォーマット（JSON）**
		```json
		[
			{{
				"text": "短文",
				"score": 0.9
			}},
			{{
				"text": "別の短文",
				"score": 0.3
			}}
		]

		制約:
		- 50ペアは **高スコア（0.8〜1.0）** で、明確に{feature}の度合いが高いものを作成する。
		- 50ペアは **低スコア（0.0〜0.4）** で{feature}の度合が低いものを作成する。
		- **短文は（20〜40文字）。**
		- **ランダム性を持たせて、できるだけ多様な組み合わせを作る**。
		
		{option_oder}

		100ペアを生成してください。
	'''

	return prompt

def extract_json_block(text):
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def make_json(text):
	json_str = extract_json_block(text)

	if json_str is None:
		raise HTTPException(status_code=500, detail="responseからのJSONスニペット部の抜き出しに失敗しました")

	try:
		json_data = json.loads(json_str)
	except json.JSONDecodeError:
		raise HTTPException(status_code=500, detail="JSON化できませんでした")	
	
	return json_data
