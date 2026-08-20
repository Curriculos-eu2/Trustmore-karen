# Página da Karen (Trustmore) — como publicar no GitHub Pages

Este pacote tem 4 arquivos soltos (sem pasta): `index.html`, `README.md`,
`karen-foto.jpg` e `fundo.jpg`. Não precisa instalar nada — só subir esses
arquivos pro GitHub e ativar o GitHub Pages. Leva uns 5 minutos.

## Passo a passo

1. Crie uma conta gratuita em [github.com](https://github.com) (se ainda não tiver).
2. Clique em **New repository** (repositório novo).
   - Nome sugerido: `trustmore-karen`.
   - Deixe como **Public**.
   - Pode marcar "Add a README file" se quiser (a gente troca pelo nosso depois) ou deixar desmarcado.
   - Clique em **Create repository**.
3. Na página do repositório, clique em **Add file → Upload files**.
4. Arraste os 4 arquivos de uma vez (`index.html`, `README.md`, `karen-foto.jpg`,
   `fundo.jpg`) pra área de upload — todos soltos, sem pasta, então é só
   arrastar e soltar.
5. Desce a página, escreve algo como "primeira versão" na caixa de mensagem, e clica no botão verde **Commit changes**.
6. Vá em **Settings → Pages** (menu lateral esquerdo).
7. Em **Build and deployment → Source**, escolha **Deploy from a branch**.
8. Em **Branch**, escolha `main` e a pasta `/ (root)`, depois **Save**.
9. Espere cerca de 1 minuto. O GitHub mostra o link final, algo como:
   `https://SEUUSUARIO.github.io/trustmore-karen/`

Esse é o link que a Karen vai mandar pros clientes dela.

## Como atualizar depois (foto, avaliações, etc.)

Não precisa reenviar o arquivo inteiro. No GitHub:

1. Abra o arquivo `index.html` dentro do repositório.
2. Clique no ícone de lápis (**Edit**) no canto superior direito.
3. Procure o bloco `const CONFIG = { ... }` perto do final do arquivo.
4. Para adicionar uma avaliação real, adicione uma linha assim dentro de `reviews: [ ]`:

   ```js
   { name: "Fernanda", rating: 5, text: "A Karen é super caprichosa!", date: "ago/2026" },
   ```

5. Para trocar a foto de perfil, suba a nova imagem pelo mesmo **Add file →
   Upload files** e troque o nome do arquivo na linha
   `photoUrl: "karen-foto.jpg"`.
6. Clique em **Commit changes** — a página atualiza sozinha em cerca de 1 minuto.

## Marca

O nome "Trustmore" já está configurado na linha `brandName: "Trustmore"` dentro
do `CONFIG`. Se um dia quiserem trocar o nome do produto, é só editar essa
linha — atualiza automaticamente o topo da página, o título da aba e o rodapé.
