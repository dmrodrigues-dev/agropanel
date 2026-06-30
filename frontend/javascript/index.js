// Função para carregar a tabelacom os produtos do banco
function carregar_produtos() {
  let tabela = document.getElementById("table-produtos");
  tabela.innerHTML = `
    <tr>
        <th>ID</th>
        <th>Nome</th>
    </tr>`;

  fetch("http://127.0.0.1:5000/api/produtos", {
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
                `;

        linha.dataset.registro = JSON.stringify(produto);

        tabela.appendChild(linha);
      }
    });
}

// Função para adicionar produto ao banco
function add_produto() {
  const nome = document.getElementById("nome").value;
  if (!nome) {
    alert("Insira um nome válido!");
    return;
  }

  fetch("http://127.0.0.1:5000/api/produtos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome: nome }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao adicionar produto!");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      carregar_produtos();
    });
}

function select_produto() {
  let linha = event.target.closest("tr");
  let div_but = document.getElementById("update-delete-produto");
  let but_add = document.getElementById("but-add-produto");
  let nome = document.getElementById("nome");

  if (
    !linha ||
    (registro && registro.id == JSON.parse(linha.dataset.registro).id && toggle)
  ) {
    nome.value = "";
    div_but.style.display = "none";
    but_add.disabled = false;
    toggle = false;
    return;
  }

  registro = JSON.parse(linha.dataset.registro);
  nome.value = registro.nome;
  but_add.disabled = true;
  toggle = true;
  div_but.style.display = "block";
}

function del_produto() {
  let conf = confirm("Deletar produto selecionado?");

  if (conf) {
    fetch(`http://127.0.0.1:5000/api/produtos/${registro.id}`, {
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
        let div_but = document.getElementById("update-delete-produto");
        div_but.style.display = "none";
        carregar_produtos();
      });
  }
}

function upt_produto() {
  const nome = document.getElementById("nome").value;
  if (!nome) {
    alert("Insira um nome válido.");
    return;
  }

  fetch(`http://127.0.0.1:5000/api/produtos/${registro.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome: nome }),
  })
    .then((resposta) => {
      if (!resposta.ok) {
        throw new Error("Erro ao editar produto.");
      }
      return resposta.json();
    })
    .then((dados) => {
      alert(dados.message);
      let div_but = document.getElementById("update-delete-produto");
      div_but.style.display = "none";
      carregar_produtos();
    });
}

function carregar_estatisticas() {
  fetch("http://127.0.0.1:5000/api/estatisticas", {
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
      console.log(dados);
    });
}

let registro, toggle;
let tabela = document.getElementById("table-produtos");
tabela.addEventListener("click", select_produto);
carregar_produtos();
carregar_estatisticas();
