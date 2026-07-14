function carregar_vendas() {
  let tabela = document.getElementById("table-vendas");
  tabela.innerHTML = `
    <tr>
        <th>ID</th>
        <th>Dia</th>
        <th>Produto</th>
        <th>Preço(R$)</th>
        <th>Quantidade</th>
        <th>Comprador</th>
    </tr>
    `;

  fetch(`${window.API_URL}/api/vendas`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao recuperar vendas.");
      }
      return resposta.json();
    })
    .then((dados) => {
      for (let venda of dados) {
        let linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${venda.id}</td>
            <td>${venda.dia}</td>
            <td>${venda.produto_id}</td>
            <td>${venda.preco.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>${venda.qtd}</td>
            <td>${venda.comprador}</td>
            `;
        linha.dataset.registro = JSON.stringify(venda);
        tabela.appendChild(linha);
      }
    });
}

function add_venda() {
  const dia = document.getElementById("dia").value;
  const produto_id = document.getElementById("produto_id").value;
  const preco = document.getElementById("preco").value;
  const qtd = document.getElementById("qtd").value;
  const comprador = document.getElementById("comprador").value;

  if (!dia || !produto_id || !qtd) {
    alert("Todos os campos * precisam ser preenchidos.");
    return;
  }

  fetch(`${window.API_URL}/api/vendas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dia: dia,
      produto_id: produto_id,
      preco: preco,
      qtd: qtd,
      comprador: comprador,
    }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao adicionar venda.");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      limpar_campos();
      carregar_vendas();
    });
}

function limpar_campos() {
  let div_but = document.getElementById("update-delete-venda");
  let but_add = document.getElementById("but-add-venda");
  let dia = document.getElementById("dia");
  let produto = document.getElementById("produto_id");
  let preco = document.getElementById("preco");
  let qtd = document.getElementById("qtd");
  let comprador = document.getElementById("comprador");

  dia.value = "";
  produto.value = "";
  preco.value = "";
  qtd.value = "";
  comprador.value = "";
  but_add.disabled = false;
  div_but.style.display = "none";
  toggle = false;
  return;
}

function select_venda() {
  let linha = event.target.closest("tr");
  let div_but = document.getElementById("update-delete-venda");
  let but_add = document.getElementById("but-add-venda");

  let dia = document.getElementById("dia");
  let produto = document.getElementById("produto_id");
  let preco = document.getElementById("preco");
  let qtd = document.getElementById("qtd");
  let comprador = document.getElementById("comprador");

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
  comprador.value = registro.comprador;
  but_add.disabled = true;
  toggle = true;
  div_but.style.display = "block";
}

function del_venda() {
  let conf = confirm("Deletar registro selecionado?");

  if (conf) {
    fetch(`${window.API_URL}/api/vendas/${registro.id}`, {
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
        carregar_vendas();
      });
  }
}

function upt_venda() {
  let dia = document.getElementById("dia").value;
  let produto = document.getElementById("produto_id").value;
  let preco = document.getElementById("preco").value;
  let qtd = document.getElementById("qtd").value;
  let comprador = document.getElementById("comprador").value;

  if (!dia || !produto || !preco || !qtd) {
    alert("Preencha todos os campos obrigatórios");
    return;
  }

  fetch(`${window.API_URL}/api/vendas/${registro.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dia: dia,
      produto_id: produto,
      preco: preco,
      qtd: qtd,
      comprador: comprador,
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
      carregar_vendas();
    });
}

let registro, toggle;
let tabela = document.getElementById("table-vendas");
tabela.addEventListener("click", select_venda);
carregar_vendas();
