/* ============================================================
   Controle de Estoque — app.js
   Frontend conectado as APIs reais. Dados locais sao usados
   apenas como fallback silencioso.
   ============================================================ */

'use strict';

/* ------------------------------------------------------------
   CONFIGURAÇÃO / CONSTANTES
   ------------------------------------------------------------ */
function getApiConfig() {
  const isLocal =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1';

  return {
    PRODUCT_SERVICE_BASE: isLocal
      ? 'http://localhost:8081'
      : 'https://inventory-control-api.onrender.com',
    INVENTORY_SERVICE_BASE: isLocal
      ? 'http://localhost:8082'
      : 'https://inventory-stock-service.onrender.com',
    PRODUCT_API_BASE: isLocal
      ? 'http://localhost:8081/api'
      : 'https://inventory-control-api.onrender.com/api',
    INVENTORY_API_BASE: isLocal
      ? 'http://localhost:8082/api'
      : 'https://inventory-stock-service.onrender.com/api',
  };
}

const CONFIG = {
  ...getApiConfig(),
  EXPIRY_WINDOW_DAYS: 30,    // janela de "vencimento próximo"
};

/* ------------------------------------------------------------
   DADOS MOCKADOS
   ------------------------------------------------------------ */
let products = [
  { id: 1,  nome: 'Arroz Branco Tipo 1 5kg', sku: 'ARZ-5KG', unidade: 'PCT', estoqueMinimo: 20, categoria: 'Mercearia',  descricao: 'Pacote de 5kg, grão longo fino.' },
  { id: 2,  nome: 'Feijão Carioca 1kg',        sku: 'FJC-1KG', unidade: 'PCT', estoqueMinimo: 25, categoria: 'Mercearia',  descricao: 'Pacote de 1kg.' },
  { id: 3,  nome: 'Açúcar Refinado 1kg',       sku: 'ACU-1KG', unidade: 'PCT', estoqueMinimo: 30, categoria: 'Mercearia',  descricao: '' },
  { id: 4,  nome: 'Café Torrado e Moído 500g', sku: 'CAF-500', unidade: 'PCT', estoqueMinimo: 15, categoria: 'Mercearia',  descricao: 'Embalagem a vácuo.' },
  { id: 5,  nome: 'Leite Integral 1L',         sku: 'LEI-1L',  unidade: 'L',   estoqueMinimo: 40, categoria: 'Laticínios', descricao: 'Caixa Tetra Pak.' },
  { id: 6,  nome: 'Óleo de Soja 900ml',        sku: 'OLE-900', unidade: 'UN',  estoqueMinimo: 24, categoria: 'Mercearia',  descricao: '' },
  { id: 7,  nome: 'Farinha de Trigo 1kg',      sku: 'FAR-1KG', unidade: 'PCT', estoqueMinimo: 18, categoria: 'Padaria',    descricao: 'Tipo 1.' },
  { id: 8,  nome: 'Refrigerante Cola 2L',      sku: 'REF-2L',  unidade: 'UN',  estoqueMinimo: 36, categoria: 'Bebidas',    descricao: 'Garrafa PET.' },
  { id: 9,  nome: 'Queijo Mussarela 1kg',      sku: 'QJO-1KG', unidade: 'KG',  estoqueMinimo: 8,  categoria: 'Laticínios', descricao: 'Peça fatiada sob demanda.' },
  { id: 10, nome: 'Detergente Neutro 500ml',   sku: 'DET-500', unidade: 'UN',  estoqueMinimo: 20, categoria: 'Limpeza',    descricao: '' },
];

let stockItems = [
  { id: 101, productId: 5,  quantidade: 12, estoqueMinimo: 40, dataValidade: daysFromNow(6),   lote: 'L-2406A' },
  { id: 102, productId: 1,  quantidade: 85, estoqueMinimo: 20, dataValidade: daysFromNow(420), lote: 'L-ARZ12' },
  { id: 103, productId: 9,  quantidade: 0,  estoqueMinimo: 8,  dataValidade: daysFromNow(18),  lote: 'L-QJO04' },
  { id: 104, productId: 4,  quantidade: 9,  estoqueMinimo: 15, dataValidade: daysFromNow(210), lote: 'L-CAF77' },
  { id: 105, productId: 2,  quantidade: 60, estoqueMinimo: 25, dataValidade: daysFromNow(365), lote: 'L-FJC09' },
  { id: 106, productId: 8,  quantidade: 22, estoqueMinimo: 36, dataValidade: daysFromNow(95),  lote: 'L-REF31' },
  { id: 107, productId: 3,  quantidade: 48, estoqueMinimo: 30, dataValidade: daysFromNow(540), lote: 'L-ACU21' },
  { id: 108, productId: 6,  quantidade: 14, estoqueMinimo: 24, dataValidade: daysFromNow(160), lote: 'L-OLE55' },
  { id: 109, productId: 7,  quantidade: 33, estoqueMinimo: 18, dataValidade: daysFromNow(11),  lote: 'L-FAR02' },
  { id: 110, productId: 10, quantidade: 41, estoqueMinimo: 20, dataValidade: daysFromNow(800), lote: 'L-DET88' },
];

let movements = [
  { id: 9001, itemId: 102, tipo: 'entrada', quantidade: 50, motivo: 'Compra de fornecedor', data: hoursAgo(2) },
  { id: 9002, itemId: 105, tipo: 'saida',   quantidade: 8,  motivo: 'Venda balcão',          data: hoursAgo(4) },
  { id: 9003, itemId: 101, tipo: 'saida',   quantidade: 6,  motivo: 'Venda balcão',          data: hoursAgo(6) },
  { id: 9004, itemId: 107, tipo: 'entrada', quantidade: 24, motivo: 'Reposição',             data: hoursAgo(26) },
  { id: 9005, itemId: 103, tipo: 'saida',   quantidade: 4,  motivo: 'Perda / vencimento',    data: hoursAgo(30) },
];

/* sequências de IDs */
let seq = { product: 11, stock: 111, movement: 9006 };
const fallbackProducts = clone(products);
const fallbackStockItems = clone(stockItems);
const fallbackMovements = clone(movements);
let servicesOnline = false;

/* ------------------------------------------------------------
   CAMADA DE API
   ------------------------------------------------------------ */
const api = {
  async getProducts() {
    const data = await requestJson(`${CONFIG.PRODUCT_API_BASE}/products`);
    return data.map(mapProductFromApi);
  },
  async createProduct(payload) {
    if (!servicesOnline) {
      const p = { id: seq.product++, ...payload };
      products.push(p);
      return clone(p);
    }
    return mapProductFromApi(await requestJson(`${CONFIG.PRODUCT_API_BASE}/products`, postJson(mapProductToApi(payload))));
  },
  async updateProduct(id, payload) {
    if (!servicesOnline) {
      const i = products.findIndex(p => p.id === id);
      if (i > -1) products[i] = { ...products[i], ...payload };
      return clone(products[i]);
    }
    return mapProductFromApi(await requestJson(`${CONFIG.PRODUCT_API_BASE}/products/${id}`, postJson(mapProductToApi(payload), 'PUT')));
  },
  async deleteProduct(id) {
    if (!servicesOnline) {
      products = products.filter(p => p.id !== id);
      stockItems = stockItems.filter(s => s.productId !== id);
      return true;
    }
    await requestJson(`${CONFIG.PRODUCT_API_BASE}/products/${id}`, { method: 'DELETE' }, false);
    return true;
  },

  async getStockItems() {
    const data = await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items`);
    return data.map(mapStockFromApi);
  },
  async createStockItem(payload) {
    if (!servicesOnline) {
      const s = { id: seq.stock++, ...payload };
      stockItems.push(s);
      return clone(s);
    }
    return mapStockFromApi(await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items`, postJson(mapStockToApi(payload))));
  },
  async registerEntry(itemId, payload) {
    if (!servicesOnline) return applyMovement(itemId, 'entrada', payload);
    return mapMovementFromApi(await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items/${itemId}/entries`, postJson(mapMovementToApi(payload))));
  },
  async registerExit(itemId, payload) {
    if (!servicesOnline) return applyMovement(itemId, 'saida', payload);
    return mapMovementFromApi(await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items/${itemId}/exits`, postJson(mapMovementToApi(payload))));
  },
  async getLowStock() {
    const data = await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items/low-stock`);
    return data.map(mapStockFromApi);
  },
  async getExpiring() {
    const data = await requestJson(`${CONFIG.INVENTORY_API_BASE}/stock-items/expiring`);
    return data.map(mapStockFromApi);
  },
};

/* helpers de fetch */
function postJson(body, method = 'POST') {
  return { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) };
}
function clone(x) { return JSON.parse(JSON.stringify(x)); }
async function requestJson(url, options = {}, expectBody = true) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  if (!expectBody || response.status === 204) return null;
  return response.json();
}
function mapProductFromApi(p) {
  return {
    id: p.id,
    nome: p.name,
    sku: p.sku,
    unidade: p.unit,
    estoqueMinimo: p.minimumStock,
    categoria: p.category || 'Sem categoria',
    descricao: p.description || '',
  };
}
function mapProductToApi(p) {
  return {
    name: p.nome,
    sku: p.sku,
    unit: p.unidade,
    minimumStock: p.estoqueMinimo,
    category: p.categoria,
    description: p.descricao || null,
  };
}
function mapStockFromApi(s) {
  return {
    id: s.id,
    productId: s.productId,
    quantidade: s.quantity,
    estoqueMinimo: s.minimumStock,
    dataValidade: s.expirationDate || daysFromNow(365),
    lote: s.batchCode || 'Sem lote',
  };
}
function mapStockToApi(s) {
  return {
    productId: String(s.productId),
    quantity: s.quantidade,
    minimumStock: s.estoqueMinimo,
    expirationDate: s.dataValidade || null,
    batchCode: s.lote || null,
  };
}
function mapMovementToApi(m) {
  return { quantity: m.quantidade, reason: m.motivo || null };
}
function mapMovementFromApi(m) {
  return {
    id: m.id,
    itemId: m.stockItemId,
    productId: m.productId,
    tipo: String(m.type).toLowerCase() === 'entry' ? 'entrada' : 'saida',
    quantidade: m.quantity,
    motivo: m.reason || 'Movimentacao registrada',
    data: m.occurredAt,
  };
}

/* aplica entrada/saida ao fallback local e registra movimentacao */
function applyMovement(itemId, tipo, payload) {
  const item = stockItems.find(s => s.id === itemId);
  if (!item) return null;
  const qtd = Number(payload.quantidade) || 0;
  if (tipo === 'entrada') item.quantidade += qtd;
  else item.quantidade = Math.max(0, item.quantidade - qtd);
  const mv = { id: seq.movement++, itemId, tipo, quantidade: qtd, motivo: payload.motivo || '—', data: new Date().toISOString() };
  movements.unshift(mv);
  return clone(item);
}

/* ------------------------------------------------------------
   LÓGICA DE NEGÓCIO / STATUS
   ------------------------------------------------------------ */
function statusOf(item) {
  if (item.quantidade <= 0) return { key: 'out', label: 'Sem Estoque', cls: 'out' };
  if (isExpiring(item.dataValidade)) return { key: 'exp', label: 'Vencendo', cls: 'exp' };
  if (item.quantidade <= item.estoqueMinimo) return { key: 'low', label: 'Estoque Baixo', cls: 'low' };
  return { key: 'ok', label: 'Saudável', cls: 'ok' };
}
function isExpiring(dateStr) {
  const days = daysUntil(dateStr);
  return days >= 0 && days <= CONFIG.EXPIRY_WINDOW_DAYS;
}
function isExpired(dateStr) { return daysUntil(dateStr) < 0; }

/* ------------------------------------------------------------
   UTILITÁRIOS DE DATA / FORMATO
   ------------------------------------------------------------ */
function daysFromNow(n) { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); }
function hoursAgo(n) { const d = new Date(); d.setHours(d.getHours() - n); return d.toISOString(); }
function daysUntil(dateStr) {
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const target = new Date(dateStr + 'T00:00:00');
  return Math.round((target - today) / 86400000);
}
function fmtDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });
}
function fmtRelative(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const min = Math.floor(diff / 60000);
  if (min < 1) return 'agora mesmo';
  if (min < 60) return `há ${min} min`;
  const h = Math.floor(min / 60);
  if (h < 24) return `há ${h}h`;
  const d = Math.floor(h / 24);
  return `há ${d}d`;
}
function productById(id) { return products.find(p => String(p.id) === String(id)); }
function normalizeText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}
function getProductIcon(productName, category) {
  const text = normalizeText(`${productName} ${category}`);
  const matches = [
    ['arroz', 'mdi:rice'],
    ['feijao', 'mdi:seed'],
    ['queijo', 'mdi:cheese'],
    ['leite', 'mdi:milk-bottle'],
    ['cafe', 'mdi:coffee'],
    ['oleo', 'mdi:oil'],
    ['ovo', 'mdi:egg'],
    ['pao', 'mdi:bread-slice'],
    ['refrigerante', 'mdi:bottle-soda'],
    ['acucar', 'mdi:cube-outline'],
    ['farinha', 'mdi:sack'],
    ['detergente', 'mdi:bottle-tonic-outline'],
  ];
  const found = matches.find(([term]) => text.includes(term));
  const iconName = found ? found[1] : fallbackIconForCategory(category);
  return `https://api.iconify.design/${iconName}.svg`;
}
function fallbackIconForCategory(category) {
  const value = normalizeText(category);
  if (value.includes('bebida')) return 'mdi:bottle-soda';
  if (value.includes('limpeza')) return 'mdi:spray-bottle';
  if (
    value.includes('alimento') ||
    value.includes('mercearia') ||
    value.includes('hortifruti') ||
    value.includes('laticinio') ||
    value.includes('padaria') ||
    value.includes('carne')
  ) return 'mdi:food';
  return 'mdi:package-variant-closed';
}
function productIconAvatar(product) {
  const name = product ? product.nome : 'Produto';
  const category = product ? product.categoria : '';
  return `<div class="prod-avatar"><img src="${getProductIcon(name, category)}" alt="" loading="lazy" onerror="if(!this.dataset.fallback){this.dataset.fallback='1';this.src='https://api.iconify.design/mdi:package-variant-closed.svg';}else{this.remove();}" /></div>`;
}
function initials(name) {
  return name.split(' ').filter(w => w.length > 2).slice(0, 2).map(w => w[0]).join('').toUpperCase() || name.slice(0, 2).toUpperCase();
}
function escapeHtml(s) { return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])); }

/* ------------------------------------------------------------
   ESTADO DA UI
   ------------------------------------------------------------ */
const state = { route: 'dashboard', productSearch: '', stockSearch: '', editingProduct: null };

const SECTION_META = {
  dashboard:     { title: 'Dashboard',      subtitle: 'Visão geral da operação' },
  produtos:      { title: 'Produtos',       subtitle: 'Cadastro e catálogo de produtos' },
  estoque:       { title: 'Estoque',        subtitle: 'Itens, lotes e validade' },
  movimentacoes: { title: 'Movimentações',  subtitle: 'Entradas e saídas de estoque' },
  alertas:       { title: 'Alertas',        subtitle: 'Estoque baixo e vencimento próximo' },
};

/* ------------------------------------------------------------
   NAVEGAÇÃO
   ------------------------------------------------------------ */
function navigate(route) {
  state.route = route;
  document.querySelectorAll('.route').forEach(s => s.classList.toggle('is-hidden', s.dataset.section !== route));
  document.querySelectorAll('.nav__item').forEach(b => b.classList.toggle('is-active', b.dataset.route === route));
  const meta = SECTION_META[route];
  document.getElementById('sectionTitle').textContent = meta.title;
  document.getElementById('sectionSubtitle').textContent = meta.subtitle;
  renderRoute(route);
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
}

function renderRoute(route) {
  if (route === 'dashboard') renderDashboard();
  else if (route === 'produtos') renderProducts();
  else if (route === 'estoque') renderStock();
  else if (route === 'movimentacoes') renderMovements();
  else if (route === 'alertas') renderAlerts();
}

/* ------------------------------------------------------------
   RENDER: badges / componentes reutilizáveis
   ------------------------------------------------------------ */
function badge(status) {
  return `<span class="badge badge--${status.cls}"><span class="b-dot"></span>${status.label}</span>`;
}

/* ------------------------------------------------------------
   RENDER: DASHBOARD
   ------------------------------------------------------------ */
function renderDashboard() {
  const lowCount = stockItems.filter(s => ['low', 'out'].includes(statusOf(s).key)).length;
  const expCount = stockItems.filter(s => isExpiring(s.dataValidade)).length;
  const totalUnits = stockItems.reduce((a, s) => a + s.quantidade, 0);

  document.getElementById('metricsGrid').innerHTML = [
    metricCard('brand', iconBox, 'Total de Produtos', products.length, `${products.length} no catálogo`),
    metricCard('ok', iconLayers, 'Itens em Estoque', stockItems.length, `${totalUnits} unidades no total`),
    metricCard('low', iconAlert, 'Estoque Baixo', lowCount, lowCount ? 'Requer reposição' : 'Tudo sob controle', lowCount ? 'low' : ''),
    metricCard('exp', iconClock, 'Vencimento Próximo', expCount, expCount ? `Próx. ${CONFIG.EXPIRY_WINDOW_DAYS} dias` : 'Sem vencimentos', expCount ? 'exp' : ''),
  ].join('');

  // Produtos recentes (últimos cadastrados)
  const recent = [...products].slice(-5).reverse();
  document.getElementById('recentProducts').innerHTML = '<div class="list">' + recent.map(p => `
    <div class="list-item">
      ${productIconAvatar(p)}
      <div class="list-item__main">
        <div class="list-item__title">${escapeHtml(p.nome)}</div>
        <div class="list-item__sub">${escapeHtml(p.categoria)} · ${escapeHtml(p.sku)}</div>
      </div>
      <div class="list-item__right"><span class="mono cell-sub">mín. ${p.estoqueMinimo} ${p.unidade}</span></div>
    </div>`).join('') + '</div>';

  // Alertas críticos
  const critical = stockItems
    .map(s => ({ s, st: statusOf(s) }))
    .filter(x => x.st.key !== 'ok')
    .sort((a, b) => severityRank(b.st.key) - severityRank(a.st.key))
    .slice(0, 5);
  const ca = document.getElementById('criticalAlerts');
  if (!critical.length) {
    ca.innerHTML = emptyState('ok', 'Nenhum alerta crítico', 'Todos os itens estão saudáveis.');
  } else {
    ca.style.padding = '0';
    ca.innerHTML = '<div class="list">' + critical.map(({ s, st }) => {
      const p = productById(s.productId);
      return `<div class="list-item alert-item alert-item--${st.cls}" style="padding-left:24px">
        ${productIconAvatar(p)}
        <div class="list-item__main">
          <div class="list-item__title">${escapeHtml(p ? p.nome : '—')}</div>
          <div class="list-item__sub">Lote ${escapeHtml(s.lote)} · ${s.quantidade} ${p ? p.unidade : ''}</div>
        </div>
        <div class="list-item__right">${badge(st)}</div>
      </div>`;
    }).join('') + '</div>';
  }

  // Visão geral do estoque (tabela)
  const tbody = document.querySelector('#overviewTable tbody');
  tbody.innerHTML = stockItems.slice(0, 8).map(s => {
    const p = productById(s.productId); const st = statusOf(s);
    return `<tr>
      <td>
        <div class="prod-cell">
          ${productIconAvatar(p)}
          <div class="cell-strong">${escapeHtml(p ? p.nome : '—')}</div>
        </div>
      </td>
      <td class="mono">${escapeHtml(s.lote)}</td>
      <td class="num mono">${s.quantidade}</td>
      <td class="num mono">${s.estoqueMinimo}</td>
      <td>${expiryCell(s.dataValidade)}</td>
      <td>${badge(st)}</td>
    </tr>`;
  }).join('');
}

function severityRank(key) { return { out: 3, exp: 2, low: 1, ok: 0 }[key]; }

function metricCard(variant, icon, label, value, hint, hintMod = '') {
  return `<div class="metric metric--${variant}">
    <div class="metric__top">
      <span class="metric__label">${label}</span>
      <span class="metric__icon">${icon}</span>
    </div>
    <div class="metric__value">${value}</div>
    <div class="metric__hint ${hintMod ? 'metric__hint--' + hintMod : ''}">${hint}</div>
  </div>`;
}

function expiryCell(dateStr) {
  const days = daysUntil(dateStr);
  let sub = '';
  if (days < 0) sub = '<span class="cell-sub" style="color:var(--out-fg)">vencido</span>';
  else if (days <= CONFIG.EXPIRY_WINDOW_DAYS) sub = `<span class="cell-sub" style="color:var(--exp-fg)">em ${days} dia${days === 1 ? '' : 's'}</span>`;
  return `<div class="mono">${fmtDate(dateStr)}</div>${sub}`;
}

/* ------------------------------------------------------------
   RENDER: PRODUTOS
   ------------------------------------------------------------ */
function renderProducts() {
  const q = state.productSearch.toLowerCase();
  const rows = products.filter(p =>
    !q || p.nome.toLowerCase().includes(q) || p.sku.toLowerCase().includes(q) || p.categoria.toLowerCase().includes(q)
  );
  const tbody = document.querySelector('#productsTable tbody');

  if (!rows.length) {
    tbody.innerHTML = `<tr class="empty--row"><td colspan="6">${emptyState('box',
      q ? 'Nenhum produto encontrado' : 'Nenhum produto cadastrado',
      q ? 'Ajuste a busca e tente novamente.' : 'Cadastre seu primeiro produto para começar.')}</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map(p => `<tr>
    <td>
      <div class="prod-cell">
        ${productIconAvatar(p)}
        <div>
          <div class="cell-strong">${escapeHtml(p.nome)}</div>
          ${p.descricao ? `<div class="cell-sub">${escapeHtml(p.descricao)}</div>` : ''}
        </div>
      </div>
    </td>
    <td class="mono">${escapeHtml(p.sku)}</td>
    <td>${escapeHtml(p.categoria)}</td>
    <td>${escapeHtml(p.unidade)}</td>
    <td class="num mono">${p.estoqueMinimo}</td>
    <td class="actions-col">
      <div class="row-actions">
        <button class="icon-btn" title="Editar" data-edit-product="${p.id}">
          <svg viewBox="0 0 24 24"><path d="M12 20h9M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4 12.5-12.5z"/></svg>
        </button>
        <button class="icon-btn danger" title="Excluir" data-del-product="${p.id}">
          <svg viewBox="0 0 24 24"><path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6"/></svg>
        </button>
      </div>
    </td>
  </tr>`).join('');
}

/* ------------------------------------------------------------
   RENDER: ESTOQUE
   ------------------------------------------------------------ */
function renderStock() {
  const q = state.stockSearch.toLowerCase();
  const rows = stockItems.filter(s => {
    const p = productById(s.productId);
    const hay = `${p ? p.nome : ''} ${s.lote}`.toLowerCase();
    return !q || hay.includes(q);
  });
  const tbody = document.querySelector('#stockTable tbody');

  if (!rows.length) {
    tbody.innerHTML = `<tr class="empty--row"><td colspan="7">${emptyState('layers',
      q ? 'Nenhum item encontrado' : 'Nenhum item de estoque',
      q ? 'Ajuste a busca e tente novamente.' : 'Adicione itens de estoque vinculados aos produtos.')}</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map(s => {
    const p = productById(s.productId); const st = statusOf(s);
    return `<tr>
      <td>
        <div class="prod-cell">
          ${productIconAvatar(p)}
          <div>
            <div class="cell-strong">${escapeHtml(p ? p.nome : '—')}</div>
            <div class="cell-sub">${p ? escapeHtml(p.sku) : ''}</div>
          </div>
        </div>
      </td>
      <td class="mono">${escapeHtml(s.lote)}</td>
      <td class="num mono">${s.quantidade} ${p ? p.unidade : ''}</td>
      <td class="num mono">${s.estoqueMinimo}</td>
      <td>${expiryCell(s.dataValidade)}</td>
      <td>${badge(st)}</td>
      <td class="actions-col">
        <div class="row-actions">
          <button class="icon-btn" title="Entrada" data-quick-entry="${s.id}">
            <svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
          </button>
          <button class="icon-btn" title="Saída" data-quick-exit="${s.id}">
            <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
          </button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

/* ------------------------------------------------------------
   RENDER: MOVIMENTAÇÕES
   ------------------------------------------------------------ */
function renderMovements() {
  populateStockSelects();

  const todayStr = new Date().toDateString();
  const entradasHoje = movements.filter(m => m.tipo === 'entrada' && new Date(m.data).toDateString() === todayStr).reduce((a, m) => a + m.quantidade, 0);
  const saidasHoje = movements.filter(m => m.tipo === 'saida' && new Date(m.data).toDateString() === todayStr).reduce((a, m) => a + m.quantidade, 0);
  const last = movements[0];

  document.getElementById('movementMetrics').innerHTML = [
    `<div class="mini-metric mini-metric--in">
      <div class="mini-metric__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div>
      <div><div class="mini-metric__label">Entradas Hoje</div><div class="mini-metric__value">${entradasHoje}</div></div>
    </div>`,
    `<div class="mini-metric mini-metric--out">
      <div class="mini-metric__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 5v14M5 12l7 7 7-7"/></svg></div>
      <div><div class="mini-metric__label">Saídas Hoje</div><div class="mini-metric__value">${saidasHoje}</div></div>
    </div>`,
    `<div class="mini-metric mini-metric--last">
      <div class="mini-metric__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
      <div><div class="mini-metric__label">Última Movimentação</div><div class="mini-metric__value">${last ? fmtRelative(last.data) : '—'}</div></div>
    </div>`,
  ].join('');

  const hist = document.getElementById('movementHistory');
  if (!movements.length) {
    hist.innerHTML = emptyState('history', 'Sem movimentações', 'As entradas e saídas aparecerão aqui.');
    return;
  }
  hist.innerHTML = '<div class="list">' + movements.slice(0, 12).map(m => {
    const item = stockItems.find(s => s.id === m.itemId);
    const p = item ? productById(item.productId) : null;
    const isIn = m.tipo === 'entrada';
    return `<div class="list-item">
      <div class="mv-icon mv-icon--${isIn ? 'in' : 'out'}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">${isIn ? '<path d="M12 19V5M5 12l7-7 7 7"/>' : '<path d="M12 5v14M5 12l7 7 7-7"/>'}</svg>
      </div>
      <div class="list-item__main">
        <div class="list-item__title">${escapeHtml(p ? p.nome : 'Item removido')}</div>
        <div class="list-item__sub">${isIn ? 'Entrada' : 'Saída'} · ${escapeHtml(m.motivo)}${item ? ' · Lote ' + escapeHtml(item.lote) : ''}</div>
      </div>
      <div class="list-item__right">
        <div class="mv-qty mv-qty--${isIn ? 'in' : 'out'}">${isIn ? '+' : '−'}${m.quantidade}</div>
        <div class="mv-time">${fmtRelative(m.data)}</div>
      </div>
    </div>`;
  }).join('') + '</div>';
}

/* ------------------------------------------------------------
   RENDER: ALERTAS
   ------------------------------------------------------------ */
function renderAlerts() {
  const low = stockItems.filter(s => ['low', 'out'].includes(statusOf(s).key))
    .sort((a, b) => severityRank(statusOf(b).key) - severityRank(statusOf(a).key));
  const exp = stockItems.filter(s => isExpiring(s.dataValidade) || isExpired(s.dataValidade))
    .sort((a, b) => daysUntil(a.dataValidade) - daysUntil(b.dataValidade));

  document.getElementById('lowStockCount').textContent = low.length;
  document.getElementById('expiringCount').textContent = exp.length;

  const lowEl = document.getElementById('lowStockAlerts');
  if (!low.length) {
    lowEl.innerHTML = emptyState('ok', 'Estoque saudável', 'Nenhum item abaixo do mínimo no momento.');
  } else {
    lowEl.style.padding = '0';
    lowEl.innerHTML = '<div class="list">' + low.map(s => {
      const p = productById(s.productId); const st = statusOf(s);
      const motivo = st.key === 'out' ? 'Sem estoque disponível' : `Abaixo do mínimo (${s.estoqueMinimo})`;
      return `<div class="list-item alert-item alert-item--${st.cls}" style="padding-left:24px">
        ${productIconAvatar(p)}
        <div class="list-item__main">
          <div class="list-item__title">${escapeHtml(p ? p.nome : '—')}</div>
          <div class="list-item__sub">Lote ${escapeHtml(s.lote)} · ${motivo}</div>
        </div>
        <div class="list-item__right">
          <div class="alert-badge-num" style="color:var(--${st.cls}-fg)">${s.quantidade} ${p ? p.unidade : ''}</div>
          <div class="cell-sub">${badge(st)}</div>
        </div>
      </div>`;
    }).join('') + '</div>';
  }

  const expEl = document.getElementById('expiringAlerts');
  if (!exp.length) {
    expEl.innerHTML = emptyState('ok', 'Nenhum vencimento próximo', `Nenhum item vence nos próximos ${CONFIG.EXPIRY_WINDOW_DAYS} dias.`);
  } else {
    expEl.style.padding = '0';
    expEl.innerHTML = '<div class="list">' + exp.map(s => {
      const p = productById(s.productId);
      const days = daysUntil(s.dataValidade);
      const vencido = days < 0;
      const motivo = vencido ? 'Produto vencido' : `Vence em ${days} dia${days === 1 ? '' : 's'}`;
      return `<div class="list-item alert-item alert-item--${vencido ? 'out' : 'exp'}" style="padding-left:24px">
        ${productIconAvatar(p)}
        <div class="list-item__main">
          <div class="list-item__title">${escapeHtml(p ? p.nome : '—')}</div>
          <div class="list-item__sub">Lote ${escapeHtml(s.lote)} · ${s.quantidade} ${p ? p.unidade : ''} · ${motivo}</div>
        </div>
        <div class="list-item__right">
          <div class="mono" style="font-weight:700;color:var(--${vencido ? 'out' : 'exp'}-fg)">${fmtDate(s.dataValidade)}</div>
        </div>
      </div>`;
    }).join('') + '</div>';
  }
}

/* ------------------------------------------------------------
   ALERT COUNT NA SIDEBAR
   ------------------------------------------------------------ */
function updateAlertBadge() {
  const count = stockItems.filter(s => statusOf(s).key !== 'ok').length;
  const el = document.getElementById('navAlertCount');
  el.textContent = count;
  el.dataset.empty = count === 0 ? 'true' : 'false';
}

function setApiStatus(online) {
  servicesOnline = online;
  const pill = document.getElementById('apiStatusPill');
  const text = document.getElementById('apiStatusText');
  pill.classList.toggle('is-offline', !online);
  text.textContent = online ? 'Serviços online' : 'Serviços indisponíveis';
}

async function checkServicesHealth() {
  await Promise.all([
    requestJson(`${CONFIG.PRODUCT_SERVICE_BASE}/health`),
    requestJson(`${CONFIG.INVENTORY_SERVICE_BASE}/health`),
  ]);
}

async function loadData() {
  try {
    const [, apiProducts, apiStockItems] = await Promise.all([
      checkServicesHealth().then(() => true),
      api.getProducts(),
      api.getStockItems(),
    ]);

    setApiStatus(true);
    products = apiProducts;
    stockItems = apiStockItems;
    if (!movements.length) movements = clone(fallbackMovements);
  } catch (error) {
    setApiStatus(false);
    products = products.length ? products : clone(fallbackProducts);
    stockItems = stockItems.length ? stockItems : clone(fallbackStockItems);
    movements = movements.length ? movements : clone(fallbackMovements);
  }
}

/* ------------------------------------------------------------
   SELECTS dinâmicos
   ------------------------------------------------------------ */
function populateStockSelects() {
  const opts = stockItems.map(s => {
    const p = productById(s.productId);
    return `<option value="${s.id}">${escapeHtml(p ? p.nome : 'Item')} · Lote ${escapeHtml(s.lote)} (${s.quantidade})</option>`;
  }).join('');
  document.querySelectorAll('[data-stock-select]').forEach(sel => {
    const prev = sel.value;
    sel.innerHTML = opts || '<option value="">Nenhum item disponível</option>';
    if (prev) sel.value = prev;
  });
}
function populateProductSelects() {
  const opts = products.map(p => `<option value="${p.id}">${escapeHtml(p.nome)} · ${escapeHtml(p.sku)}</option>`).join('');
  document.querySelectorAll('[data-product-select]').forEach(sel => {
    sel.innerHTML = opts || '<option value="">Cadastre um produto primeiro</option>';
  });
}

/* ------------------------------------------------------------
   EMPTY STATES + ÍCONES (inline SVG)
   ------------------------------------------------------------ */
const iconBox    = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 7l9-4 9 4v10l-9 4-9-4V7z"/><path d="M3 7l9 4 9-4M12 11v10"/></svg>';
const iconLayers = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/></svg>';
const iconAlert  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 3l9 16H3l9-16z"/><path d="M12 10v4M12 17v.5"/></svg>';
const iconClock  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>';

function emptyState(type, title, text) {
  const icons = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20 6L9 17l-5-5"/></svg>',
    box: iconBox,
    layers: iconLayers,
    history: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 12a9 9 0 109-9 9 9 0 00-7 3.3M3 4v4h4"/><path d="M12 8v4l3 2"/></svg>',
  };
  const okCls = type === 'ok' ? ' empty__icon--ok' : '';
  return `<div class="empty">
    <div class="empty__icon${okCls}">${icons[type] || iconBox}</div>
    <div class="empty__title">${title}</div>
    <div class="empty__text">${text}</div>
  </div>`;
}

/* ------------------------------------------------------------
   MODAIS
   ------------------------------------------------------------ */
function openModal(id) { document.getElementById(id).classList.add('is-open'); document.getElementById(id).setAttribute('aria-hidden', 'false'); }
function closeModal(el) { const m = el.closest('.modal'); m.classList.remove('is-open'); m.setAttribute('aria-hidden', 'true'); }

function openProductModal(product = null) {
  const form = document.getElementById('productForm');
  form.reset();
  state.editingProduct = product ? product.id : null;
  document.getElementById('productModalTitle').textContent = product ? 'Editar Produto' : 'Adicionar Produto';
  if (product) {
    form.id.value = product.id;
    form.nome.value = product.nome;
    form.sku.value = product.sku;
    form.unidade.value = product.unidade;
    form.estoqueMinimo.value = product.estoqueMinimo;
    form.categoria.value = product.categoria;
    form.descricao.value = product.descricao || '';
  }
  openModal('productModal');
}

function openStockModal() {
  document.getElementById('stockForm').reset();
  populateProductSelects();
  openModal('stockModal');
}

/* ------------------------------------------------------------
   TOAST
   ------------------------------------------------------------ */
let toastTimer;
function toast(msg) {
  const t = document.getElementById('toast');
  t.innerHTML = `<span class="toast__dot"></span>${msg}`;
  t.classList.add('is-show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('is-show'), 2600);
}

/* ------------------------------------------------------------
   REFRESH GERAL
   ------------------------------------------------------------ */
async function refreshAll() {
  await loadData();
  updateAlertBadge();
  renderRoute(state.route);
}

/* ------------------------------------------------------------
   EVENTOS
   ------------------------------------------------------------ */
function bindEvents() {
  // navegação (qualquer elemento com data-route)
  document.addEventListener('click', e => {
    const navEl = e.target.closest('[data-route]');
    if (navEl) { navigate(navEl.dataset.route); return; }

    // fechar modal
    if (e.target.closest('[data-close]')) { closeModal(e.target); return; }

    // editar / excluir produto
    const edit = e.target.closest('[data-edit-product]');
    if (edit) { openProductModal(productById(edit.dataset.editProduct)); return; }

    const del = e.target.closest('[data-del-product]');
    if (del) {
      const p = productById(del.dataset.delProduct);
      if (p && confirm(`Excluir o produto "${p.nome}"? Os itens de estoque vinculados também serão removidos.`)) {
        api.deleteProduct(p.id).then(async () => { toast('Produto excluído'); await refreshAll(); });
      }
      return;
    }

    // entrada / saída rápida a partir da tabela de estoque
    const qEntry = e.target.closest('[data-quick-entry]');
    if (qEntry) { quickMovement(Number(qEntry.dataset.quickEntry), 'entrada'); return; }
    const qExit = e.target.closest('[data-quick-exit]');
    if (qExit) { quickMovement(Number(qExit.dataset.quickExit), 'saida'); return; }
  });

  // busca produtos
  document.getElementById('productSearch').addEventListener('input', e => { state.productSearch = e.target.value; renderProducts(); });
  document.getElementById('stockSearch').addEventListener('input', e => { state.stockSearch = e.target.value; renderStock(); });

  // botões de adicionar
  document.getElementById('addProductBtn').addEventListener('click', () => openProductModal());
  document.getElementById('addStockBtn').addEventListener('click', () => openStockModal());
  document.getElementById('refreshBtn').addEventListener('click', async () => {
    const btn = document.getElementById('refreshBtn');
    btn.disabled = true;
    await refreshAll();
    btn.disabled = false;
    toast('Dados atualizados');
  });

  // form produto
  document.getElementById('productForm').addEventListener('submit', async e => {
    e.preventDefault();
    const f = e.target;
    const payload = {
      nome: f.nome.value.trim(), sku: f.sku.value.trim(), unidade: f.unidade.value,
      estoqueMinimo: Number(f.estoqueMinimo.value), categoria: f.categoria.value, descricao: f.descricao.value.trim(),
    };
    const done = async () => { closeModal(f); await refreshAll(); };
    if (state.editingProduct) {
      await api.updateProduct(state.editingProduct, payload);
      toast('Produto atualizado');
      await done();
    } else {
      await api.createProduct(payload);
      toast('Produto cadastrado');
      await done();
    }
  });

  // form item de estoque
  document.getElementById('stockForm').addEventListener('submit', async e => {
    e.preventDefault();
    const f = e.target;
    const payload = {
      productId: f.productId.value, quantidade: Number(f.quantidade.value),
      estoqueMinimo: Number(f.estoqueMinimo.value), dataValidade: f.dataValidade.value, lote: f.lote.value.trim(),
    };
    await api.createStockItem(payload);
    toast('Item de estoque adicionado');
    closeModal(f);
    await refreshAll();
  });

  // form entrada
  document.getElementById('entryForm').addEventListener('submit', async e => {
    e.preventDefault();
    const f = e.target;
    const itemId = f.itemId.value;
    if (!itemId) return;
    const movement = await api.registerEntry(itemId, { quantidade: Number(f.quantidade.value), motivo: f.motivo.value.trim() });
    if (movement) movements.unshift(movement);
    toast('Entrada registrada');
    f.reset();
    await refreshAll();
  });

  // form saída
  document.getElementById('exitForm').addEventListener('submit', async e => {
    e.preventDefault();
    const f = e.target;
    const itemId = f.itemId.value;
    if (!itemId) return;
    const item = stockItems.find(s => String(s.id) === String(itemId));
    const qtd = Number(f.quantidade.value);
    if (item && qtd > item.quantidade && !confirm(`Quantidade maior que o disponível (${item.quantidade}). O estoque ficará zerado. Continuar?`)) return;
    const movement = await api.registerExit(itemId, { quantidade: qtd, motivo: f.motivo.value.trim() });
    if (movement) movements.unshift(movement);
    toast('Saída registrada');
    f.reset();
    await refreshAll();
  });

  // fechar modal com ESC
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') document.querySelectorAll('.modal.is-open').forEach(m => { m.classList.remove('is-open'); m.setAttribute('aria-hidden', 'true'); });
  });
}

/* entrada/saída rápida via prompt simples */
async function quickMovement(itemId, tipo) {
  const item = stockItems.find(s => String(s.id) === String(itemId));
  if (!item) return;
  const p = productById(item.productId);
  const label = tipo === 'entrada' ? 'entrada' : 'saída';
  const val = prompt(`Registrar ${label} — ${p ? p.nome : 'item'} (Lote ${item.lote})\nQuantidade:`, '1');
  if (val === null) return;
  const qtd = Number(val);
  if (!qtd || qtd < 1) { toast('Quantidade inválida'); return; }
  const fn = tipo === 'entrada' ? api.registerEntry : api.registerExit;
  const movement = await fn(itemId, { quantidade: qtd, motivo: tipo === 'entrada' ? 'Reposição rápida' : 'Saída rápida' });
  if (movement) movements.unshift(movement);
  toast(`${tipo === 'entrada' ? 'Entrada' : 'Saída'} registrada`);
  await refreshAll();
}

/* ------------------------------------------------------------
   INICIALIZAÇÃO
   ------------------------------------------------------------ */
async function init() {
  window.history.scrollRestoration = 'manual';
  window.scrollTo(0, 0);

  // data atual no header
  document.getElementById('currentDate').textContent =
    new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' });

  bindEvents();
  await loadData();
  updateAlertBadge();
  navigate('dashboard');
}

document.addEventListener('DOMContentLoaded', init);
