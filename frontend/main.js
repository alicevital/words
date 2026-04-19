
const API_URL = "http://127.0.0.1:8000";
const hoje = new Date().toISOString().slice(0, 10);

console.log("SCRIPT INICIOU");

let progresso = JSON.parse(localStorage.getItem("termo")) || {};

if (!progresso[hoje]) {
  progresso[hoje] = {
    tentativas: [],
    venceu: false
  };
}

function render() {
  const rows = document.querySelectorAll(".row");

  rows.forEach(row => {
    Array.from(row.children).forEach(cell => {
      cell.innerText = "";
    });
  });

  progresso[hoje].tentativas.slice(0,5).forEach((palavra, i) => {
    const cells = rows[i].children;

    palavra.split("").forEach((letra, j) => {
      cells[j].innerText = letra;
    });
  });
}

async function enviar() {
  const input = document.getElementById("input");
  const palavra = input.value.toLowerCase();

  if (palavra.length !== 5) {
    alert("Digite 5 letras");
    return;
  }

  if (progresso[hoje].venceu) {
    alert("Você já venceu hoje!");
    return;
  }

  if (progresso[hoje].tentativas.length >= 5){
    alert("ACABOU SUAS TENTATIVAS");
    return;
  }

  try {
    const res = await fetch(API_URL + "/guess", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ palavra })
    });

    let data;

    try {
        data = await res.json();
    } catch {
        alert("Erro inesperado no servidor");
        return;
    }

    if (!res.ok) {
      alert(typeof data.detail == "string"
        ? data.detail
        : data.detail?.[0]?.msg || "Erro desconhecido"
      );
      render();
      return;
    }

    
    progresso[hoje].tentativas.push(palavra);

    
    const venceu = data.resultado.every(r => r === "correct");

    if (venceu) {
      progresso[hoje].venceu = true;
      alert("Você venceu!");
    }

    
    localStorage.setItem("termo", JSON.stringify(progresso));

    render();

    input.value = "";

  } catch (err) {
    alert("Erro ao conectar com API");
  }
}

const grid = document.getElementById("grid");

function criarGrid() {

  console.log("CRIANDO GRID");

  grid.innerHTML = "";

  for (let i = 0; i < 5; i++) {
    const row = document.createElement("div");
    row.classList.add("row");

    for (let j = 0; j < 5; j++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      row.appendChild(cell);
    }

    grid.appendChild(row);
  }
}

criarGrid();
render();