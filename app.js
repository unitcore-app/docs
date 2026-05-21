(function () {
  const groupsEl = document.getElementById('groups');
  const searchEl = document.getElementById('search');
  const hintEl = document.getElementById('hint');

  let data = null;

  function codeToSlug(code) { return code.replace(/\./g, '/'); }

  function statusBadge(status) {
    return '<span class="badge badge-status-' + status + '">' + status + '</span>';
  }

  function render(filter) {
    if (!data) return;
    const q = (filter || '').trim().toLowerCase();
    let total = 0;
    const html = data.groups.map(function (g) {
      const codes = g.codes.filter(function (c) {
        if (!q) return true;
        return (
          c.code.toLowerCase().includes(q) ||
          c.title.toLowerCase().includes(q) ||
          c.summary.toLowerCase().includes(q) ||
          g.title.toLowerCase().includes(q)
        );
      });
      if (codes.length === 0) return '';
      total += codes.length;
      const cards = codes.map(function (c) {
        return (
          '<a class="code-card" href="/errors/' + codeToSlug(c.code) + '">' +
          '<span class="code">' + c.code + '</span>' +
          '<span class="title">' + c.title + '</span>' +
          '<span class="meta">' + statusBadge(c.status) + '</span>' +
          '</a>'
        );
      }).join('');
      return (
        '<div class="group">' +
        '<h2>' + g.title + '</h2>' +
        '<p class="group-desc">' + g.description + '</p>' +
        '<div class="codes">' + cards + '</div>' +
        '</div>'
      );
    }).join('');

    if (total === 0) {
      groupsEl.innerHTML = '<p class="no-results">No matching error codes.</p>';
    } else {
      groupsEl.innerHTML = html;
    }
    hintEl.textContent = total + ' code' + (total === 1 ? '' : 's') + (q ? ' match "' + q + '"' : ' total');
  }

  fetch('/errors.json').then(function (r) { return r.json(); }).then(function (j) {
    data = j;
    render('');
  });

  searchEl.addEventListener('input', function () { render(searchEl.value); });
})();
