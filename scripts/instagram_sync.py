#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza a seção "Acompanhe a OLIMAIS no Instagram" do site.

A cada execução (roda sozinho no GitHub, a cada poucas horas):
  1. uma vez por semana, renova a chave do Instagram (ela vale 60 dias);
  2. busca os posts e reels mais recentes da conta, pela API oficial do Instagram;
  3. baixa a imagem de cada um (nos reels, a capa), recorta em quadrado, reduz e
     guarda em img/instagram/ (os endereços de imagem do Instagram expiram em poucos
     dias, por isso as imagens são guardadas no próprio site);
  4. grava data/instagram.json, que é o arquivo que o site lê.

SEGURANÇA
  - A chave vem do segredo INSTAGRAM_TOKEN do GitHub. Ela NUNCA é escrita em arquivo e
    NUNCA aparece nos registros (logs) da execução, que são públicos neste repositório.
  - Se qualquer coisa falhar (chave vencida, Instagram fora do ar, imagem inválida...),
    NADA é alterado: o site continua mostrando os últimos posts que já tinha.

CONFIGURAÇÃO (variáveis de ambiente; só a primeira é obrigatória)
  INSTAGRAM_TOKEN          chave de acesso (vem do segredo do GitHub)
  INSTAGRAM_POSTS          quantos posts mostrar (padrão 4; de 1 a 12)
  INSTAGRAM_REFRESH        "1" para renovar a chave nesta execução
  INSTAGRAM_FORCE          "1" para baixar de novo todas as imagens
  INSTAGRAM_API_BASE       endereço da API (padrão https://graph.instagram.com)
  INSTAGRAM_ALLOW_INSECURE "1" aceita imagens em http:// (só para testes)
  INSTAGRAM_RETRY_DELAY    segundos entre tentativas (padrão 3; testes usam 0)
"""
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOKEN = os.environ.get("INSTAGRAM_TOKEN", "").strip()
API = os.environ.get("INSTAGRAM_API_BASE", "https://graph.instagram.com").rstrip("/")
INSECURE = os.environ.get("INSTAGRAM_ALLOW_INSECURE") == "1"
FORCE = os.environ.get("INSTAGRAM_FORCE") == "1"
REFRESH = os.environ.get("INSTAGRAM_REFRESH") == "1"
try:
    RETRY_DELAY = float(os.environ.get("INSTAGRAM_RETRY_DELAY", "3"))
except ValueError:
    RETRY_DELAY = 3.0
try:
    MAX_POSTS = max(1, min(12, int(os.environ.get("INSTAGRAM_POSTS", "4"))))
except ValueError:
    MAX_POSTS = 4

ROOT = Path(os.environ.get("SITE_ROOT") or Path(__file__).resolve().parent.parent)
DATA_FILE = ROOT / "data" / "instagram.json"
IMG_DIR = ROOT / "img" / "instagram"
TILE = 640               # lado do quadrado, em pixels (o site mostra a ~280 px; sobra para telas retina)
MAX_IMAGE_BYTES = 8 * 1024 * 1024
FIELDS = "id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp"
UA = "OLIMAIS-site-instagram-sync/1.0 (+https://olimais.com.br)"

ID_RE = re.compile(r"^[0-9A-Za-z_-]{1,40}$")
PERMALINK_RE = re.compile(r"^https://(www\.)?instagram\.com/(p|reel|reels|tv)/[A-Za-z0-9_-]+/?(\?[^\s]*)?$")


# --------------------------------------------------------------------------- mensagens
def scrub(text):
    """Tira a chave de qualquer texto antes de ele ser mostrado."""
    text = str(text)
    return text.replace(TOKEN, "***") if TOKEN else text


def say(msg):
    print(scrub(msg), flush=True)


def warn(msg):
    print("::warning::" + scrub(msg).replace("\n", " "), flush=True)


def die(msg):
    print("::error::" + scrub(msg).replace("\n", " "), flush=True)
    sys.exit(1)


class ApiError(Exception):
    def __init__(self, code, kind, message, status):
        super().__init__(message)
        self.code, self.kind, self.status = code, kind, status

    def short(self):
        partes = [p for p in (f"código {self.code}" if self.code else "", str(self)[:140]) if p]
        return ", ".join(partes) or "erro desconhecido"


def explain(e):
    """Traduz o erro do Instagram para uma orientação clara."""
    if e.code == 190 or e.status == 401:
        return ("O Instagram recusou a chave (vencida ou cancelada). Gere uma nova chave no painel da Meta "
                "e atualize o segredo INSTAGRAM_TOKEN no GitHub (veja o GUIA-INSTAGRAM). "
                "O site continua mostrando os últimos posts.")
    if e.code in (4, 17, 32, 613) or e.status == 429:
        return "O Instagram limitou as consultas por agora. Tenta de novo na próxima execução. Nada foi alterado."
    if e.code in (10, 200, 283):
        return ("A chave não tem permissão para ler os posts. Confira, no painel da Meta, se a permissão "
                "instagram_business_basic está ativa e gere a chave de novo. Nada foi alterado.")
    return f"O Instagram respondeu com erro ({e.short()}). Nada foi alterado."


# --------------------------------------------------------------------------- rede
def http_get(url, limit=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(limit + 1) if limit else r.read()
            if limit and len(data) > limit:
                raise ValueError("arquivo grande demais")
            return r.status, data
    except urllib.error.HTTPError as e:
        try:
            body = e.read(65536)
        except Exception:
            body = b""
        return e.code, body


def api_get(path, params):
    """Chama a API do Instagram (com novas tentativas se houver instabilidade)."""
    query = dict(params)
    query["access_token"] = TOKEN
    url = f"{API}/{path.lstrip('/')}?{urllib.parse.urlencode(query)}"
    ultimo = ApiError(None, None, "falha de rede", None)
    for tentativa in range(3):
        if tentativa:
            time.sleep(RETRY_DELAY * tentativa)
        try:
            status, body = http_get(url)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            ultimo = ApiError(None, None, f"falha de rede ({type(e).__name__})", None)
            continue
        try:
            data = json.loads(body.decode("utf-8", "replace"))
        except ValueError:
            data = None
        if status == 200 and isinstance(data, dict):
            return data
        if isinstance(data, dict) and isinstance(data.get("error"), dict):
            err = data["error"]
            erro = ApiError(err.get("code"), err.get("type"), str(err.get("message", "")), status)
            if status >= 500 or erro.code in (1, 2):      # instabilidade do Instagram: tenta de novo
                ultimo = erro
                continue
            raise erro
        if status >= 500 or status == 429:
            ultimo = ApiError(None, None, f"instabilidade do Instagram (HTTP {status})", status)
            continue
        raise ApiError(None, None, f"resposta inesperada (HTTP {status})", status)
    raise ultimo


# --------------------------------------------------------------------------- chave
def refresh_token():
    """Renova a chave por mais 60 dias. Falhar aqui não impede o resto (a chave atual segue valendo)."""
    try:
        data = api_get("refresh_access_token", {"grant_type": "ig_refresh_token"})
    except ApiError as e:
        warn(f"Não deu para renovar a chave agora ({e.short()}). Segue com a chave atual.")
        return
    try:
        dias = int(data.get("expires_in", 0)) // 86400
    except (TypeError, ValueError):
        dias = 0
    if str(data.get("access_token", "")) not in ("", TOKEN):
        warn("O Instagram devolveu uma chave com texto diferente ao renovar. A chave atual continua em uso; "
             "se o feed parar de atualizar em cerca de 2 meses, gere uma chave nova (veja o GUIA-INSTAGRAM).")
    say(f"Chave renovada: vale por mais {dias} dias.")


# --------------------------------------------------------------------------- posts
def alt_text(caption, video):
    """Texto alternativo da imagem: a primeira linha da legenda, limpa e curta."""
    texto = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", str(caption or ""))
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    texto = re.sub(r"\s+", " ", linhas[0] if linhas else "").strip()
    if len(texto) > 110:
        texto = texto[:110].rstrip() + "…"
    if video:
        return ("Vídeo do Instagram: " + texto) if texto else "Vídeo do Instagram da OLIMAIS"
    return texto or "Publicação do Instagram da OLIMAIS"


def candidate(item):
    """Valida um post da API e escolhe a imagem. Devolve None se não servir."""
    if not isinstance(item, dict):
        return None
    pid, link = str(item.get("id", "")), str(item.get("permalink", ""))
    if not ID_RE.match(pid) or not PERMALINK_RE.match(link):
        return None
    video = item.get("media_type") == "VIDEO"
    src = item.get("thumbnail_url") if video else item.get("media_url")
    esquemas = ("https://", "http://") if INSECURE else ("https://",)
    if not isinstance(src, str) or not src.startswith(esquemas):
        return None
    data = str(item.get("timestamp", ""))[:10]
    return {"id": pid, "url": link, "src": src, "video": video,
            "alt": alt_text(item.get("caption"), video),
            "date": data if re.match(r"^\d{4}-\d{2}-\d{2}$", data) else ""}


def make_tile(raw):
    """Recorta no centro (um pouco acima, onde costumam ficar os rostos) e reduz para TILE x TILE."""
    from PIL import Image, ImageOps
    Image.MAX_IMAGE_PIXELS = 60_000_000
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA", "P"):
            rgba = im.convert("RGBA")
            fundo = Image.new("RGB", rgba.size, (255, 255, 255))
            fundo.paste(rgba, mask=rgba.split()[-1])
            im = fundo
        else:
            im = im.convert("RGB")
        im = ImageOps.fit(im, (TILE, TILE), method=Image.LANCZOS, centering=(0.5, 0.4))
        out = io.BytesIO()
        im.save(out, "JPEG", quality=82, optimize=True, progressive=True)   # sem metadados
        return out.getvalue()


def load_existing():
    try:
        d = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def github_output(**kv):
    caminho = os.environ.get("GITHUB_OUTPUT")
    if caminho:
        with open(caminho, "a", encoding="utf-8") as f:
            for k, v in kv.items():
                f.write(f"{k}={v}\n")


def main():
    if not TOKEN:
        die("Falta o segredo INSTAGRAM_TOKEN (no GitHub: Settings > Secrets and variables > Actions).")
    if REFRESH:
        refresh_token()

    try:
        lista = api_get("me/media", {"fields": FIELDS, "limit": str(min(50, MAX_POSTS * 4 + 4))}).get("data")
    except ApiError as e:
        die(explain(e))
    if not isinstance(lista, list):
        die("O Instagram respondeu sem a lista de posts. Nada foi alterado.")

    existente = {p.get("id"): p for p in (load_existing().get("posts") or []) if isinstance(p, dict)}
    posts, imagens = [], {}
    for item in lista:
        if len(posts) >= MAX_POSTS:
            break
        c = candidate(item)
        if not c:
            continue
        nome = f"{c['id']}.jpg"
        destino = IMG_DIR / nome
        if destino.exists() and not FORCE and c["id"] in existente:
            pass                                    # imagem já guardada: não baixa de novo
        else:
            try:
                status, raw = http_get(c["src"], limit=MAX_IMAGE_BYTES)
                if status != 200:
                    raise ValueError(f"HTTP {status}")
                imagens[nome] = make_tile(raw)
            except Exception as e:                  # imagem expirada, corrompida, grande demais...
                warn(f"Post {c['id']}: a imagem não pôde ser usada ({type(e).__name__}); pulei este.")
                continue
        posts.append({"id": c["id"], "url": c["url"], "image": f"img/instagram/{nome}",
                      "alt": c["alt"], "video": c["video"], "date": c["date"]})

    if not posts:
        die("Nenhum post com imagem utilizável foi encontrado. Nada foi alterado.")

    antigo = load_existing().get("posts")
    mudou = bool(imagens) or antigo != posts or any(not (ROOT / p["image"]).exists() for p in posts)
    if not mudou:
        say(f"Sem novidades: os {len(posts)} posts mais recentes já estão no site.")
        github_output(changed="false")
        return

    # tudo pronto: só agora grava (primeiro as imagens, depois a lista)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for nome, dados in imagens.items():
        (IMG_DIR / nome).write_bytes(dados)
    manter = {Path(p["image"]).name for p in posts}
    for velho in IMG_DIR.glob("*.jpg"):
        if velho.name not in manter:
            velho.unlink()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    saida = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "posts": posts}
    DATA_FILE.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    say(f"Atualizado: {len(posts)} posts ({len(imagens)} imagem(ns) nova(s)).")
    github_output(changed="true")


if __name__ == "__main__":
    main()
