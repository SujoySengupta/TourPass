document.addEventListener('DOMContentLoaded', function() {
    // Update total price when quantity changes
    const quantityInput = document.getElementById('quantity');
    const priceElement = document.getElementById('total_price');
    const pricePerTicket = parseFloat(priceElement.textContent.replace('₹', ''));
  
    function updateTotalPrice() {
      const quantity = parseInt(quantityInput.value) || 1;
      const total = pricePerTicket * quantity;
      document.getElementById('total_price').textContent = '₹' + total.toFixed(2);
    }
  
    if (quantityInput) {
      quantityInput.addEventListener('input', updateTotalPrice);
    }
  });