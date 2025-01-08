import asyncio
from typing import List
from saju_rag.component.connector.base import BaseConnector
from saju_rag.core.entity.document import ConnectorInput, ConnectorOutput
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


class WebConnector(BaseConnector):
    def __init__(self, model, tokenizer):
        super().__init__(model, tokenizer)
        self.playwright = None
        self.browser = None

    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    def connector_info(self) -> str:
        return '{ "connector" : "WebConnector", "description" : "웹 커넥터는 구글, 네이버에서 정보를 조회합니다." }'

    async def get_document(self, input: ConnectorInput) -> List[ConnectorOutput]:
        await self.init_browser()
        naver_post, google_post = await asyncio.gather(
            self.search_naver_post(input.query), self.search_google_post(input.query)
        )
        post = naver_post + google_post
        result = self.find_similar_chunks(input.query, post, top_n=5, chunk_size=8192)
        return [
            ConnectorOutput(content=chunk, similarity=similarity)
            for chunk, similarity in result
        ]

    async def search_naver_post(self, query: str) -> List[str]:
        texts = []
        try:
            page = await self.browser.new_page()
            await page.goto(f"https://search.naver.com/search.naver?query={query}")
            links = await page.query_selector_all("#main_pack a")
            urls = [await link.get_attribute("href") for link in links]
            await page.close()
            # 각 링크에 대해 HTML 본문을 비동기로 가져오기
            html_bodies = await asyncio.gather(
                *(self.fetch_html_body(url) for url in urls), return_exceptions=True
            )
            # HTML 본문에서 순수 텍스트 추출
            texts = [self.extract_text_from_html(html) for html in html_bodies if html]
        except Exception as e:
            pass
        finally:
            await page.close()

        return texts

    async def search_google_post(self, query: str) -> List[str]:
        texts = []
        try:
            # 구글 검색 결과에서 링크 추출
            page = await self.browser.new_page()
            await page.goto(
                f"https://www.google.co.kr/search?q={query}",
                wait_until="domcontentloaded",
            )
            links = await page.query_selector_all("div#search a")
            urls = [await link.get_attribute("href") for link in links]
            await page.close()
            # 각 링크에 대해 HTML 본문을 비동기로 가져오기
            html_bodies = await asyncio.gather(
                *(self.fetch_html_body(url) for url in urls), return_exceptions=True
            )
            # HTML 본문에서 순수 텍스트 추출
            texts = [self.extract_text_from_html(html) for html in html_bodies if html]
        finally:
            await page.close()

        return texts

    async def fetch_html_body(self, url):
        page = await self.browser.new_page()
        try:
            if "naver" in url:
                page.evaluate(
                    """
                    const domain = window.location.origin;
                    const iframe = document.querySelector("iframe");
                    if (iframe && iframe.src) {
                        const iframeUrl = new URL(iframe.src, domain).href;
                        window.location.href = iframeUrl;
                    }
                """
                )
                await page.wait_for_selector("body")
            await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            html_content = await page.content()  # HTML 본문을 가져옴
        except Exception as e:
            html_content = None
        finally:
            await page.close()  # 페이지 사용 후 닫기
        return html_content

    def extract_text_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator=" ", strip=True)  # 텍스트만 추출
