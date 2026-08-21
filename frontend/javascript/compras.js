function carregar_compras() {
  let tabela = document.getElementById("table-compras");
  tabela.innerHTML = `
    <tr>
        <th>ID</th>
        <th>Dia</th>
        <th>Produto</th>
        <th>Preço(R$)</th>
        <th>Quantidade</th>
        <th>Fornecedor</th>
    </tr>
    `;

  fetch(`${window.API_URL}/api/compras`, {
    method: "GET",
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao recuperar compras.");
      }
      loading.style.display = "none";
      return resposta.json();
    })
    .then((dados) => {
      for (let compra of dados) {
        let linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${compra.id}</td>
            <td>${compra.dia}</td>
            <td>${compra.produto_id}</td>
            <td>${compra.preco.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>${compra.qtd}</td>
            <td>${compra.fornecedor}</td>
            `;
        linha.dataset.registro = JSON.stringify(compra);
        tabela.appendChild(linha);
      }
    })
    .catch(() => {
      loading.innerHTML = `
      <div id="loading">
        <h2>Não foi possível conectar ao servidor</h2>
        <p>Verifique sua conexão e tente novamente.</p>
        <button onclick="location.reload()">Recarregar</button>
      </div>`;
    });
}

function add_compra() {
  const dia = document.getElementById("dia").value;
  const produto_id = document.getElementById("produto_id").value;
  const preco = document.getElementById("preco").value;
  const qtd = document.getElementById("qtd").value;
  const fornecedor = document.getElementById("fornecedor").value;

  if (!dia || !produto_id || !preco || !qtd || !fornecedor) {
    alert("Todos os campos precisam ser preenchidos.");
    return;
  }

  fetch(`${window.API_URL}/api/compras`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dia: dia,
      produto_id: produto_id,
      preco: preco,
      qtd: qtd,
      fornecedor: fornecedor,
    }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao adicionar compra.");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      limpar_campos();
      carregar_compras();
    });
}

function limpar_campos() {
  let div_but = document.getElementById("update-delete-compra");
  let but_add = document.getElementById("but-add-compra");
  let dia = document.getElementById("dia");
  let produto = document.getElementById("produto_id");
  let preco = document.getElementById("preco");
  let qtd = document.getElementById("qtd");
  let fornecedor = document.getElementById("fornecedor");

  dia.value = "";
  produto.value = "";
  preco.value = "";
  qtd.value = "";
  fornecedor.value = "";
  but_add.disabled = false;
  div_but.style.display = "none";
  toggle = false;
  return;
}

function select_compra() {
  let linha = event.target.closest("tr");
  let div_but = document.getElementById("update-delete-compra");
  let but_add = document.getElementById("but-add-compra");

  let dia = document.getElementById("dia");
  let produto = document.getElementById("produto_id");
  let preco = document.getElementById("preco");
  let qtd = document.getElementById("qtd");
  let fornecedor = document.getElementById("fornecedor");

  if (
    !linha ||
    (registro && registro.id == JSON.parse(linha.dataset.registro).id && toggle)
  ) {
    limpar_campos();
    return;
  }

  registro = JSON.parse(linha.dataset.registro);
  dia.value = registro.dia;
  produto.value = registro.produto_id;
  preco.value = registro.preco;
  qtd.value = registro.qtd;
  fornecedor.value = registro.fornecedor;
  but_add.disabled = true;
  toggle = true;
  div_but.style.display = "block";
}

function del_compra() {
  let conf = confirm("Deletar registro selecionado?");

  if (conf) {
    fetch(`${window.API_URL}/api/compras/${registro.id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    })
      .then((resposta) => {
        if (!resposta.ok) {
          throw new Error("Erro ao deletar registro.");
        }
        return resposta.json();
      })
      .then((dados) => {
        alert(dados.message);
        limpar_campos();
        carregar_compras();
      });
  }
}

function upt_compra() {
  let dia = document.getElementById("dia").value;
  let produto = document.getElementById("produto_id").value;
  let preco = document.getElementById("preco").value;
  let qtd = document.getElementById("qtd").value;
  let fornecedor = document.getElementById("fornecedor").value;

  if (!dia || !produto || !preco || !qtd || !fornecedor) {
    alert("Preencha todos os campos obrigatórios");
    return;
  }

  fetch(`${window.API_URL}/api/compras/${registro.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dia: dia,
      produto_id: produto,
      preco: preco,
      qtd: qtd,
      fornecedor: fornecedor,
    }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao editar registro.");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      limpar_campos();
      carregar_compras();
    });
}

let registro, toggle;
let tabela = document.getElementById("table-compras");
let loading = document.getElementById("loading-modal");
tabela.addEventListener("click", select_compra);
carregar_compras();
