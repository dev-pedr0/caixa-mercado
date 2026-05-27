from bs4 import BeautifulSoup
import pandas as pd
import requests

def realizar_scraping_produtos(caminho_csv: str) -> bool:
    url = "https://pedrovncs.github.io/lindosprecos/produtos.html#"
    print(f"Buscando produtos em: {url}...")

    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code != 200:
            print(f"Erro ao acessar a página. Status Code: {resposta.status_code}")
            return False
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        cards_produtos = soup.find_all("div", class_="product-card")
        lista_produtos = []
        for card in cards_produtos:
            card_body = card.find("div", class_="card-body")
            if not card_body:
                continue

            nome = card_body.find("h5", class_="card-title")["data-nome"].strip()
            preco_raw = card_body.find("p", class_="card-price")["data-preco"]
            preco_limpo = preco_raw.replace("R$", "").replace("\xa0", "").replace(" ", "").replace(",", ".")
            preco = float(preco_limpo)
            qtd_raw = card_body.find("p", data_qtd=True) or card_body.find("p", {"data-qtd": True})
            quantidade = int(qtd_raw["data-qtd"])

            lista_produtos.append({
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco
            })
        
        if not lista_produtos:
            print("Nenhum produto foi encontrado durante a raspagem do HTML.")
            return False
        
        df = pd.DataFrame(lista_produtos)
        df.to_csv(caminho_csv, sep=',', index=False, encoding='utf-8')

        print(f"Web Scraping concluído! {len(df)} produtos salvos em '{caminho_csv}'.")
        return True
    except Exception as e:
        print(f"Erro crítico durante o processo de Web Scraping: {e}")
        return False