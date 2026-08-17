// Função para carregar a tabelacom os produtos do banco
function carregar_produtos() {
  let tabela = document.getElementById("table-produtos");
  tabela.innerHTML = `
    <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Preço(R$)</th>
        <th>Estoque</th>
    </tr>`;

  fetch(`${window.API_URL}/api/produtos`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao recuperar arquivos");
      }
      return resposta.json();
    })
    .then((dados) => {
      for (let produto of dados) {
        let linha = document.createElement("tr");
        linha.innerHTML = `
                <td>${produto.id}</td>
                <td>${produto.nome}</td>
                <td>${produto.preco_de_venda.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td>${produto.estoque}</td>
                `;

        linha.dataset.registro = JSON.stringify(produto);

        tabela.appendChild(linha);
      }
    });
}

// Função para adicionar produto ao banco
function add_produto() {
  const nome = document.getElementById("nome").value;
  const preco = document.getElementById("preco").value;
  if (!nome || !preco) {
    alert("Todos os campos precisam ser preenchidos");
    return;
  }

  fetch(`${window.API_URL}/api/produtos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: nome,
      preco_de_venda: preco,
    }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao adicionar produto!");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      limpar_campos();
      carregar_produtos();
    });
}

function limpar_campos() {
  let div_but = document.getElementById("update-delete-produto");
  let but_add = document.getElementById("but-add-produto");
  let nome = document.getElementById("nome");
  let preco = document.getElementById("preco");

  nome.value = "";
  preco.value = null;
  div_but.style.display = "none";
  but_add.disabled = false;
  toggle = false;
  return;
}

function select_produto() {
  let linha = event.target.closest("tr");
  let div_but = document.getElementById("update-delete-produto");
  let but_add = document.getElementById("but-add-produto");
  let nome = document.getElementById("nome");
  let preco = document.getElementById("preco");

  if (
    !linha ||
    (registro && registro.id == JSON.parse(linha.dataset.registro).id && toggle)
  ) {
    limpar_campos();
    return;
  }

  registro = JSON.parse(linha.dataset.registro);
  nome.value = registro.nome;
  preco.value = registro.preco_de_venda;
  but_add.disabled = true;
  toggle = true;
  div_but.style.display = "block";
}

function del_produto() {
  let conf = confirm("Deletar produto selecionado?");

  if (conf) {
    fetch(`${window.API_URL}/api/produtos/${registro.id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    })
      .then((resposta) => {
        if (!resposta.ok) {
          throw new Error("Erro ao deletar produto.");
        }
        return resposta.json();
      })
      .then((dados) => {
        alert(dados.message);
        limpar_campos();
        carregar_produtos();
      });
  }
}

function upt_produto() {
  const nome = document.getElementById("nome").value;
  const preco = document.getElementById("preco").value;
  if (!nome || !preco) {
    alert("Preencha todos os campos obrigatórios");
    return;
  }

  fetch(`${window.API_URL}/api/produtos/${registro.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: nome,
      preco_de_venda: preco,
    }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao editar produto.");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      limpar_campos();
      carregar_produtos();
    });
}

function carregar_estatisticas() {
  let endpoint;
  if (mesAno.value) {
    let [selectedAno, selectedMes] = mesAno.value.split("-");
    endpoint = `${window.API_URL}/api/estatisticas?mes=${selectedMes}&ano=${selectedAno}`;
  } else {
    endpoint = `${window.API_URL}/api/estatisticas`;
  }

  fetch(endpoint, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao recuperar estatísticas.");
      }
      return resposta.json();
    })
    .then((dados) => {
      receita.innerHTML = `
      <h2>Receita</h2>
      <p>${dados.receita.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>`;

      despesa.innerHTML = `
      <h2>Despesa</h2>
      <p>${dados.despesa.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>`;

      lucro.innerHTML = `
      <h2>Lucro</h2>
      <p>${dados.lucro.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>`;

      carregar_grafico(dados.vendaveis);
    });
}

function carregar_grafico(dados) {
  if (chart != null) {
    chart.destroy();
  }

  let labels = dados.map((item) => item.nome);
  let values = dados.map((item) => item.valor);

  chart = new Chart(canva, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{ label: "Receita por produto", data: values }],
    },
  });
}

let registro, toggle, chart;
let canva = document.getElementById("chart");
let tabela = document.getElementById("table-produtos");
let mesAno = document.getElementById("mes");
let receita = document.getElementById("receita");
let despesa = document.getElementById("despesa");
let lucro = document.getElementById("lucro");
tabela.addEventListener("click", select_produto);
mesAno.addEventListener("change", carregar_estatisticas);
carregar_produtos();
carregar_estatisticas();
