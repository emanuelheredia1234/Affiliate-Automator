async function generateProduct() {
  const prompt = document.getElementById('prompt').value;
  const res = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });
  const data = await res.json();
  if (data.content) {
    document.getElementById('output').textContent = data.content;
    document.getElementById('description').value = data.content;
  } else {
    document.getElementById('output').textContent = data.error || 'Error generating';
  }
}

async function saveProduct() {
  const name = document.getElementById('name').value;
  const description = document.getElementById('description').value;
  const res = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description })
  });
  const data = await res.json();
  if (data.id) {
    loadProducts();
  } else {
    alert(data.error || 'Failed to save product');
  }
}

async function loadProducts() {
  const res = await fetch('/api/products');
  const products = await res.json();
  const container = document.getElementById('products');
  container.innerHTML = '<h2>Products</h2>';
  products.forEach(p => {
    const div = document.createElement('div');
    div.className = 'product';
    div.innerHTML = `<h3>${p.name}</h3><p>${p.description}</p>`;
    container.appendChild(div);
  });
}

document.getElementById('generate').addEventListener('click', generateProduct);
document.getElementById('save').addEventListener('click', saveProduct);
loadProducts();
