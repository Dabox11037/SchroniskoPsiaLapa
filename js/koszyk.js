// Koszyk Psiej Łapy – zapis w localStorage, wspólny dla wszystkich stron
(function () {
    const KEY = 'psialapa_koszyk';
    // Ścieżka do katalogu głównego strony (strony produktów leżą w /produkty/)
    const ROOT = document.currentScript && document.currentScript.dataset.root || '';

    function load() {
        try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
    }
    function save(items) {
        localStorage.setItem(KEY, JSON.stringify(items));
        updateBadge();
    }
    function count() {
        return load().reduce((n, i) => n + i.qty, 0);
    }
    function total() {
        return load().reduce((s, i) => s + i.qty * i.price, 0);
    }
    function add(item, qty) {
        qty = Math.max(1, parseInt(qty, 10) || 1);
        const items = load();
        const found = items.find(i => i.id === item.id);
        if (found) found.qty += qty; else items.push(Object.assign({}, item, { qty: qty }));
        save(items);
        toast('Dodano do koszyka: ' + item.name);
    }
    function setQty(id, qty) {
        let items = load();
        qty = parseInt(qty, 10) || 0;
        items = qty > 0 ? items.map(i => i.id === id ? Object.assign(i, { qty: qty }) : i) : items.filter(i => i.id !== id);
        save(items);
    }
    function clear() { save([]); }

    function updateBadge() {
        document.querySelectorAll('.cart-count').forEach(el => { el.textContent = count(); });
    }

    function toast(text) {
        let t = document.getElementById('cart-toast');
        if (!t) {
            t = document.createElement('div');
            t.id = 'cart-toast';
            t.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#333;color:#fff;' +
                'padding:0.8rem 1.4rem;border-radius:8px;z-index:1000;box-shadow:0 4px 12px rgba(0,0,0,0.3);transition:opacity 0.3s;';
            document.body.appendChild(t);
        }
        t.innerHTML = '🛒 ' + text + ' – <a href="' + ROOT + 'koszyk.html" style="color:#ffb74d;font-weight:bold">przejdź do koszyka</a>';
        t.style.opacity = '1';
        clearTimeout(t._timer);
        t._timer = setTimeout(() => { t.style.opacity = '0'; }, 3500);
    }

    window.Koszyk = { load, add, setQty, clear, count, total, root: ROOT };
    document.addEventListener('DOMContentLoaded', updateBadge);
    window.addEventListener('storage', updateBadge);
})();
