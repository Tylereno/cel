const data = window.CEL_DATA
const taxonomy = data.taxonomy
const codes = taxonomy.codes
const machines = data.machines

const state = {
  query: '',
  category: 'all',
  selectedCode: codes.find((code) => code.kind === 'leaf')?.code || codes[0]?.code,
  machineId: machines[0]?.id,
}

const $ = (selector) => document.querySelector(selector)

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function leafCodes() {
  return codes.filter((code) => code.kind === 'leaf')
}

function renderStats() {
  $('#incident-count').textContent = codes.length
  $('#leaf-count').textContent = leafCodes().length
  $('#machine-count').textContent = machines.length
  $('#spec-version').textContent = taxonomy.cel_spec
}

function renderCategories() {
  const categories = codes.filter((code) => code.kind === 'category')
  $('#category-list').innerHTML = [
    `<button class="filter-button ${state.category === 'all' ? 'active' : ''}" type="button" data-category="all">All</button>`,
    ...categories.map(
      (category) =>
        `<button class="filter-button ${state.category === category.code ? 'active' : ''}" type="button" data-category="${escapeHtml(category.code)}">${escapeHtml(category.label)}</button>`,
    ),
  ].join('')

  $('#category-list').querySelectorAll('[data-category]').forEach((button) => {
    button.addEventListener('click', () => {
      state.category = button.dataset.category
      renderCategories()
      renderIncidentList()
    })
  })
}

function matchesCategory(code) {
  return (
    state.category === 'all' ||
    code.code === state.category ||
    code.parent === state.category ||
    code.code.startsWith(`${state.category}.`)
  )
}

function renderIncidentList() {
  const query = state.query.trim().toLowerCase()
  const visible = codes.filter((code) => {
    const haystack = `${code.code} ${code.label} ${code.spoken} ${code.description || ''}`.toLowerCase()
    return matchesCategory(code) && (!query || haystack.includes(query))
  })

  $('#visible-count').textContent = `${visible.length} shown`
  $('#incident-list').innerHTML =
    visible.length > 0
      ? visible
          .map(
            (code) => `
              <button
                class="word-button ${state.selectedCode === code.code ? 'active' : ''}"
                type="button"
                role="option"
                aria-selected="${state.selectedCode === code.code}"
                data-code="${escapeHtml(code.code)}"
              >
                <span class="word-code">${escapeHtml(code.code)}</span>
                <span class="word-label">${escapeHtml(code.label)}</span>
                <span class="word-kind">${escapeHtml(code.kind)}</span>
              </button>
            `,
          )
          .join('')
      : '<p class="detail-copy">No incident words match this filter.</p>'

  $('#incident-list').querySelectorAll('[data-code]').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedCode = button.dataset.code
      renderIncidentList()
      renderIncidentDetail()
    })
  })
}

function renderIncidentDetail() {
  const code = codes.find((item) => item.code === state.selectedCode)
  if (!code) {
    $('#incident-detail').innerHTML = '<div class="detail-empty">Select an incident word.</div>'
    return
  }

  const profiles = Object.entries(code.profiles || {})
    .map(
      ([name, value]) => `
        <div class="meta-box">
          <dt>${escapeHtml(name.replaceAll('_', ' '))}</dt>
          <dd>${escapeHtml(value)}</dd>
        </div>
      `,
    )
    .join('')

  $('#incident-detail').innerHTML = `
    <div class="detail-code">${escapeHtml(code.code)}</div>
    <h2 class="detail-title">${escapeHtml(code.label)}</h2>
    <p class="detail-copy">${escapeHtml(code.description || 'Named CEL incident vocabulary.')}</p>
    <dl class="detail-meta">
      <div class="meta-box">
        <dt>Spoken</dt>
        <dd>${escapeHtml(code.spoken)}</dd>
      </div>
      <div class="meta-box">
        <dt>Kind</dt>
        <dd>${escapeHtml(code.kind)}</dd>
      </div>
      <div class="meta-box">
        <dt>Parent</dt>
        <dd>${escapeHtml(code.parent || '—')}</dd>
      </div>
      ${profiles}
    </dl>
  `
}

function renderMachineTabs() {
  $('#machine-tabs').innerHTML = machines
    .map(
      (machine) => `
        <button
          class="machine-tab ${state.machineId === machine.id ? 'active' : ''}"
          type="button"
          role="tab"
          aria-selected="${state.machineId === machine.id}"
          data-machine="${escapeHtml(machine.id)}"
        >
          ${escapeHtml(machine.title.replace(' response machine', ''))}
        </button>
      `,
    )
    .join('')

  $('#machine-tabs').querySelectorAll('[data-machine]').forEach((button) => {
    button.addEventListener('click', () => {
      state.machineId = button.dataset.machine
      renderMachineTabs()
      renderMachine()
    })
  })
}

function renderMachine() {
  const machine = machines.find((item) => item.id === state.machineId)
  if (!machine) {
    $('#machine-content').innerHTML = '<p class="detail-copy">No response machine selected.</p>'
    return
  }

  const states = machine.states
    .map(
      (item, index) => `
        ${index ? '<span class="state-arrow" aria-hidden="true">→</span>' : ''}
        <span class="state">${escapeHtml(item.id)}</span>
      `,
    )
    .join('')

  const transitions = machine.transitions
    .map(
      (transition) => `
        <article class="transition">
          <code>${escapeHtml(transition.event)}</code>
          <p><strong>${escapeHtml(transition.from)}</strong> → <strong>${escapeHtml(transition.to)}</strong></p>
          <p>${escapeHtml(transition.description)}</p>
        </article>
      `,
    )
    .join('')

  $('#machine-content').innerHTML = `
    <div class="machine-summary">
      <strong>${escapeHtml(machine.title)}</strong> · ${escapeHtml(machine.description)}
      <br />
      Applies to: ${machine.incident_types.map((item) => `<code>${escapeHtml(item)}</code>`).join(', ')}
    </div>
    <div class="state-path" aria-label="Response machine states">${states}</div>
    <div class="transition-list">${transitions}</div>
  `
}

$('#incident-search').addEventListener('input', (event) => {
  state.query = event.target.value
  renderIncidentList()
})

renderStats()
renderCategories()
renderIncidentList()
renderIncidentDetail()
renderMachineTabs()
renderMachine()
