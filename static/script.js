// Cart state
let qtyMap = {};
let cart = {};

function updateCartCount() {
  const count = Object.values(cart).reduce((sum, item) => {
    if (typeof item === 'object' && item !== null && item.qty !== undefined) {
      return sum + item.qty;
    }
    return sum + (parseInt(item) || 0);
  }, 0);
  const cartCountEl = document.getElementById('cartCount');
  if (cartCountEl) cartCountEl.textContent = count;
}

function clearCart() {
  cart = {};
  qtyMap = {};
  localStorage.removeItem('homestyleCart');
  updateCartCount();
}

function addToCart(card) {
  const title = card.dataset.title;
  const price = parseFloat(card.dataset.price) || 300;
  const image = card.dataset.image || 'images/fantasy1.jpg';
  const qty = qtyMap[title] || 1;
  
  // Store with price and image information
  if (!cart[title]) {
    cart[title] = {qty: 0, price: price, image: image};
  }
  cart[title].qty += qty;
  cart[title].price = price; // Update price in case it changed
  cart[title].image = image; // Store the image path
  
  updateCartCount();
  saveCart();

  const message = card.querySelector('.added-message');
  if (message) {
    message.textContent = `Added ${qty}x ${title} to cart!`;
    message.style.display = 'block';
    setTimeout(() => message.style.display = 'none', 3000);
  }
}

function viewCart() {
  const cartContent = document.getElementById('cartContent');
  const totalEl = document.getElementById('cartTotal');
  if (!cartContent || Object.keys(cart).length === 0) {
    const modal = document.getElementById('cartModal');
    if (modal) {
      const content = modal.querySelector('.cart-empty') || modal.querySelector('#cartContent');
      content.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;"><p>Your cart is empty 😢</p><p>Add some items above!</p></div>';
    }
    if (totalEl) {
      totalEl.textContent = `Total: ₱0`;
    }
    document.getElementById('cartModal').style.display = 'block';
    return;
  }

  let cartHtml = '';
  let totalPrice = 0;

  Object.entries(cart).forEach(([title, item]) => {
    let qty = 1;
    let pricePer = 300;
    let imgSrc = 'images/fantasy1.jpg';
    
    // Handle both old format (number) and new format (object with qty, price, image)
    if (typeof item === 'object' && item !== null) {
      qty = item.qty || 1;
      pricePer = item.price || 300;
      imgSrc = item.image || 'images/fantasy1.jpg'; // Use stored image
    } else {
      qty = parseInt(item) || 1;
      // Try to find price from visible cards
      document.querySelectorAll('.card').forEach(card => {
        if (card.dataset.title === title) {
          pricePer = parseFloat(card.dataset.price) || 300;
          imgSrc = card.dataset.image || 'images/fantasy1.jpg';
        }
      });
    }
    
    const lineTotal = qty * pricePer;
    totalPrice += lineTotal;

    cartHtml += `
      <div style="display: flex; align-items: center; gap: 15px; padding: 20px; border: 1px solid #eee; margin-bottom: 15px; border-radius: 12px; background: #f9f9f9;">
        <img src="/static/${imgSrc}" style="width: 70px; height: 70px; object-fit: contain; border-radius: 8px;">
        <div style="flex: 1; min-width: 0;">
          <h4 style="margin: 0 0 5px 0; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${title}</h4>
          <p style="margin: 0; color: #666; font-size: 14px;">₱${pricePer.toLocaleString()} each</p>
        </div>
        <div style="text-align: right; min-width: 140px;">
          <input type="number" value="${qty}" min="0" max="99" onchange="updateCartQty('${title.replace(/'/g, "\\'" ).replace(/"/g, '\\\\"')}', this.value)" style="width: 65px; margin-bottom: 8px; padding: 6px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
          <div style="font-weight: bold; color: #e74c3c; font-size: 16px; margin-bottom: 10px;">
            ₱${lineTotal.toLocaleString()}
          </div>
          <button onclick="removeCartItem('${title.replace(/'/g, "\\'" ).replace(/"/g, '\\\\"')}')" style="background: #f44336; color: white; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; font-size: 13px; width: 100%;">Remove</button>
        </div>
      </div>
    `;
  });

  cartContent.innerHTML = cartHtml;
  totalEl.textContent = `Total: ₱${totalPrice.toLocaleString()}`;
  document.getElementById('cartModal').style.display = 'block';
}

function updateCartQty(title, qtyStr) {
  const qty = parseInt(qtyStr) || 0;
  if (qty === 0) {
    delete cart[title];
  } else {
    // Preserve price and image if they exist
    if (typeof cart[title] === 'object' && cart[title] !== null) {
      cart[title].qty = qty;
    } else {
      cart[title] = {qty: qty, price: 300, image: 'images/fantasy1.jpg'};
    }
  }
  updateCartCount();
  saveCart();
  viewCart();
}

function removeCartItem(title) {
  delete cart[title];
  updateCartCount();
  saveCart();
  viewCart();
}

function closeCartModal() {
  document.getElementById('cartModal').style.display = 'none';
}

function checkout() {
  if (Object.keys(cart).length === 0) return;
  const cartQuery = encodeURIComponent(JSON.stringify(cart));
  window.location.href = `/checkout?cart=${cartQuery}`;
}

function updateQty(title, qtyStr) {
  qtyMap[title] = parseInt(qtyStr) || 1;
}

function buyNow(card) {
  const title = card.dataset.title;
  const price = parseFloat(card.dataset.price) || 300;
  const image = card.dataset.image || 'images/fantasy1.jpg';
  const qty = qtyMap[title] || 1;
  
  // Store with price and image information
  if (!cart[title]) {
    cart[title] = {qty: 0, price: price, image: image};
  } else if (typeof cart[title] === 'number') {
    cart[title] = {qty: cart[title], price: price, image: image};
  }
  cart[title].qty += qty;
  cart[title].price = price;
  cart[title].image = image;
  
  updateCartCount();
  saveCart();
  checkout();
}

let selectedCategory = 'All';

function setCategoryFilter(category) {
  selectedCategory = category;
  document.querySelectorAll('.category-filter').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.category === category);
  });
  fetchFilteredItems();
}

function fetchFilteredItems(query = '') {
  const searchInput = document.getElementById('search');
  const booksDiv = document.getElementById('books');
  if (!booksDiv) return;
  const q = query || (searchInput ? searchInput.value.trim() : '');
  const category = selectedCategory === 'All' ? '' : selectedCategory;
  fetch(`/search?query=${encodeURIComponent(q)}&category=${encodeURIComponent(category)}`)
    .then(r => r.json())
    .then(items => {
      renderBooks(items);
    })
    .catch(() => {
      booksDiv.innerHTML = '<p style="text-align: center; color: #666; font-size: 18px;">Loading error</p>';
    });
}

function renderBooks(items) {
  const booksDiv = document.getElementById('books');
  if (!booksDiv) return;
  booksDiv.innerHTML = '';
  if (!items || items.length === 0) {
    booksDiv.innerHTML = '<p style="text-align: center; color: #666; font-size: 18px;">No items found</p>';
    return;
  }
  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.title = item.title;
    card.dataset.price = item.price;
    card.dataset.id = item.id || '';
    card.dataset.image = item.image;
    card.innerHTML = `
      <img src="/static/${item.image}" alt="${item.title}" class="card-image">
      <h3>${item.title}</h3>
      <div class="category-label">${item.category}</div>
      <div class="card-info">
        <div class="price">₱${item.price}</div>
        <div class="qty-section">
          <label>QTY:</label>
          <input type="number" class="qty-input" min="1" max="99" value="1" onchange="updateQty('${item.title.replace(/'/g, "\\'" ).replace(/"/g, '\\"')}', this.value)">
        </div>
      </div>
      <div class="btn-group">
        <button class="btn-cart" onclick="addToCart(this.parentElement.parentElement)">🛒</button>
        <button class="btn-buy" onclick="buyNow(this.parentElement.parentElement)">Buy Now</button>
      </div>
      <div class="added-message"></div>
    `;
    booksDiv.appendChild(card);
  });
}

function saveCart() {
  localStorage.setItem('homestyleCart', JSON.stringify(cart));
}

function loadCart() {
  const saved = localStorage.getItem('homestyleCart');
  if (saved) {
    try {
      cart = JSON.parse(saved);
      
      // Migrate old cart format (without image field) to new format
      Object.keys(cart).forEach(title => {
        const item = cart[title];
        // If it's just a number or missing image field, convert to new format
        if (typeof item === 'number') {
          cart[title] = {qty: item, price: 300, image: 'images/fantasy1.jpg'};
        } else if (typeof item === 'object' && item !== null && !item.image) {
          // Old object format without image - add the image field
          item.image = 'images/fantasy1.jpg';
        }
      });
    } catch(e) {
      console.log('Invalid cart data:', e);
      cart = {};
    }
  } else {
    cart = {};
  }
  updateCartCount();
}

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  loadCart();

  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-cart')) {
      saveCart();
    }
  });

  const searchInput = document.getElementById('search');
  const booksDiv = document.getElementById('books');
  const filterButtons = document.querySelectorAll('.category-filter');
  if (!searchInput || !booksDiv) return;

  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      setCategoryFilter(this.dataset.category);
    });
  });

  searchInput.addEventListener('input', function() {
    fetchFilteredItems(this.value.trim());
  });

  fetchFilteredItems();
});
