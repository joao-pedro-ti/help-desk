// static/script.js
const chat = document.getElementById('chat');
const controls = document.getElementById('controls');
const API = '/api';

let etapaAtual = 'inicio';
let abrirChamado = false;

function addMessage(text, type = 'bot') {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.innerHTML = text.split('\n').map(l => `<p>${l}</p>`).join('');
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function clearControls() { controls.innerHTML = ''; }

function addButton(text, onClick, className = '') {
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.className = className;
    btn.onclick = onClick;
    controls.appendChild(btn);
}

async function chamar(payload) {
    const res = await fetch(`${API}/chamado`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    return await res.json();
}

function tratarResposta(data) {
    clearControls();

    if (data.status === 'encerrado') {
        addMessage(data.mensagem, 'bot');
        addButton('🔄 Reiniciar', () => location.reload(), 'secondary');
        return;
    }

    if (data.status === 'menu') {
        etapaAtual = data.proxima_etapa || 'menu';
        addMessage(data.mensagem + '\n' + data.opcoes.join('\n'), 'bot');
        [1, 2, 3].forEach(n => {
            addButton(data.opcoes[n - 1], () => enviarDuvida(n), 'option');
        });
        return;
    }

    if (data.status === 'solucao') {
        addMessage(data.mensagem, 'solucao');
        addMessage(data.pergunta_novo, 'bot');
        etapaAtual = 'novo';
        addButton('Sim, abrir novo', () => enviarNovo(true));
        addButton('Não, encerrar', () => enviarNovo(false), 'secondary');
        return;
    }

    if (data.status === 'erro' || data.status === 'erro_final') {
        addMessage(data.mensagem, 'erro');
        etapaAtual = data.proxima_etapa || 'aninhado';
        setTimeout(() => {
            addMessage(data.menu_mensagem + '\n' + data.opcoes.join('\n'), 'bot');
            clearControls();
            [1, 2, 3].forEach(n => {
                addButton(data.opcoes[n - 1], () => enviarDuvida(n), 'option');
            });
        }, 500);
        return;
    }
}

function perguntarAbrirChamado() {
    clearControls();
    addMessage('Você deseja abrir um chamado?', 'bot');
    addButton('Sim', () => iniciar(true));
    addButton('Não', () => iniciar(false), 'secondary');
}

async function iniciar(abrir) {
    addMessage(`Você deseja abrir um chamado?: ${abrir ? 'Sim' : 'Não'}`, 'user');
    abrirChamado = abrir;
    const data = await chamar({ etapa: 'inicio', abrir_chamado: abrir });
    tratarResposta(data);
}

async function enviarDuvida(duvida) {
    addMessage(`Opção escolhida: ${duvida}`, 'user');
    const data = await chamar({
        etapa: etapaAtual,
        abrir_chamado: abrirChamado,
        duvida: duvida
    });
    tratarResposta(data);
}

async function enviarNovo(abrir) {
    addMessage(`Você deseja abrir um novo chamado?: ${abrir ? 'Sim' : 'Não'}`, 'user');
    abrirChamado = abrir;
    const data = await chamar({ etapa: 'novo', abrir_chamado: abrir });
    tratarResposta(data);
}

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(perguntarAbrirChamado, 300);
});
