import json
import re
import asyncio
from typing import Dict, Tuple, List
from playwright.async_api import async_playwright
import google.generativeai as genai

class LocalizationAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.var_pattern = re.compile(r'(\{[a-zA-Z0-9_]+\}|%[sdf]|\<[^>]+\>)')
        if api_key:
            genai.configure(api_key=api_key)

    def mask_variables(self, text: str) -> Tuple[str, List[str]]:
        variables = []
        def replace(match):
            variables.append(match.group(0))
            return f"__VAR_{len(variables) - 1}__"
        
        masked_text = self.var_pattern.sub(replace, str(text))
        return masked_text, variables

    def unmask_variables(self, translated_text: str, variables: List[str]) -> str:
        for i, var in enumerate(variables):
            placeholder = f"__VAR_{i}__"
            translated_text = translated_text.replace(placeholder, var)
        return translated_text

    def translate_payload(self, text_dict: Dict[str, str], target_lang: str) -> Dict[str, str]:
        masked_dict = {}
        vars_store = {}

        for key, value in text_dict.items():
            masked_text, variables = self.mask_variables(value)
            masked_dict[key] = masked_text
            vars_store[key] = variables

        prompt = (
            f"You are a professional software UI localizer. Translate the values in this JSON to language code '{target_lang}'. "
            f"CRITICAL RULES:\n"
            f"1. Keep all placeholders like '__VAR_0__' intact and unchanged.\n"
            f"2. Keep translations concise and natural for software interfaces/buttons.\n"
            f"3. Return ONLY valid JSON format without markdown code blocks.\n\n"
            f"JSON to translate:\n{json.dumps(masked_dict, ensure_ascii=False)}"
        )

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            clean_text = response.text.strip().replace("```json", "").replace("```", "")
            translated_masked = json.loads(clean_text)
        except Exception as e:
            print(f"Translation fallback due to error: {e}")
            translated_masked = masked_dict

        final_dict = {}
        for key, trans_text in translated_masked.items():
            variables = vars_store.get(key, [])
            final_dict[key] = self.unmask_variables(trans_text, variables)

        return final_dict

class VisualQAAgent:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def audit_ui_layout(self, target_lang: str, translated_strings: Dict[str, str]) -> List[Dict]:
        overflow_issues = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 375, "height": 667},
                locale=target_lang
            )
            page = await context.new_page()
            await page.goto(self.base_url, wait_until="networkidle", timeout=15000)

            js_detector = """
            () => {
                const elements = document.querySelectorAll('button, a, p, span, h1, h2, h3, div');
                const broken = [];
                elements.forEach(el => {
                    const hasHorizontalOverflow = el.scrollWidth > el.clientWidth + 1;
                    const style = window.getComputedStyle(el);
                    const isHidden = style.overflow === 'hidden' || style.textOverflow === 'ellipsis';
                    if (hasHorizontalOverflow && isHidden) {
                        broken.push({
                            tagName: el.tagName,
                            text: el.innerText,
                            selector: el.className || el.id || 'UI_Element',
                            scrollWidth: el.scrollWidth,
                            clientWidth: el.clientWidth
                        });
                    }
                });
                return broken;
            }
            """
            issues = await page.evaluate(js_detector)
            for item in issues:
                overflow_issues.append({
                    "language": target_lang,
                    "element": item["selector"],
                    "broken_text": item["text"],
                    "difference": item["scrollWidth"] - item["clientWidth"]
                })
            await browser.close()
        return overflow_issues
