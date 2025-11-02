import marimo
__generated_with = "0.16.5"
app = marimo.App(width="medium")

@app.cell
def get_api_keys():
    import os
    os.environ["STEEL_API_KEY"] = "UNESI-SVOJ"
    os.environ["GOOGLE_API_KEY"] = "UNESI-SVOJ"

    STEEL_API_KEY = os.getenv("STEEL_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not STEEL_API_KEY or not GOOGLE_API_KEY:
        raise ValueError("Postavi API ključeve!")

    print("🔑 API keys učitani.")
    return STEEL_API_KEY, GOOGLE_API_KEY

@app.cell
def steel_fetch_text():
    import requests
    from bs4 import BeautifulSoup

    def steel_fetch_text(url: str, api_key: str) -> str:
        if not api_key:
            return "ERROR: STEEL_API_KEY nije postavljen."
        try:
            import json
            resp = requests.post(
                "https://api.steel.dev/v1/scrape",
                headers={
                    "steel-api-key": api_key,
                    "content-type": "application/json",
                    "accept": "application/json",
                },
                json={
                    "url": url,
                    "extract": "html",  # get raw HTML for parsing
                    "useProxy": False,
                    "delay": 1,
                    "fullPage": True,
                    "region": "",
                },
            )
            ct = resp.headers.get("content-type", "")
            if "application/json" in ct:
                data = resp.json()
                if isinstance(data, dict):
                    html = (
                        data.get("html")
                        or data.get("content", {}).get("html")
                        or data.get("content", {}).get("body")
                    )
                    if isinstance(html, str) and html.strip():
                        return html
                    return str(data)
            return resp.text
        except Exception as e:
            return f"ERROR contacting Steel: {e}"

    return steel_fetch_text


@app.cell
def scrape_steam(STEEL_API_KEY, steel_fetch_text):
    url = "https://store.steampowered.com/search/?filter=topsellers"
    html_content = steel_fetch_text(url, STEEL_API_KEY)

    print("✅ Scrapan HTML/Text (prvih 2000 znakova):")
    print(html_content[:2000])
    return html_content


@app.cell
def parse_games(html_content):
    from bs4 import BeautifulSoup as _BeautifulSoup
    soup = _BeautifulSoup(html_content, "html.parser")

    games = []
    game_rows = soup.select("a.search_result_row")

    for row in game_rows[:5]:
        title = row.select_one(".title")
        released = row.select_one(".search_released")
        review = row.select_one(".search_review_summary")
        price = row.select_one(".discount_final_price")

        games.append({
            "title": title.get_text(strip=True) if title else "N/A",
            "release_date": released.get_text(strip=True) if released else "N/A",
            "review": review.get("data-tooltip-html", "N/A") if review else "N/A",
            "price": price.get_text(strip=True) if price else "N/A",
        })

    print("🔥 Top 5 Steam bestsellers:")
    for g in games:
        print(f"{g['title']} — {g['price']} — {g['release_date']}")
    return games

@app.cell
def ai_analysis(GOOGLE_API_KEY, games):
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-flash-latest")

    prompt = "Ovo su trenutno top 5 najprodavanijih igara na Steamu:\n"
    for game in games:
        prompt += f"- {game['title']} ({game['price']}, datum izlaska: {game['release_date']})\n"

    prompt += (
        "\nAnaliziraj trendove na tržištu: koji žanrovi ili stilovi igara dominiraju, "
        "ima li više novih izdanja ili etabliranih serijala, i što to može značiti za industriju."
    )

    result = model.generate_content(prompt)
    print("🧠 AI analiza trendova:\n")
    print(result.text)
    return result.text


if __name__ == "__main__":
    app.run()