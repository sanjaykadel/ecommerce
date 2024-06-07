document.addEventListener('DOMContentLoaded', function () {
    var productSelect = document.querySelector('.combo-products');
    var discountInput = document.querySelector('.combo-discount');
    var totalPriceInput = document.querySelector('.combo-total-price');

    function calculateTotalPrice() {
        var selectedProducts = Array.from(productSelect.selectedOptions);
        var total = selectedProducts.reduce(function (sum, option) {
            return sum + parseFloat(option.dataset.price);
        }, 0);

        var discount = parseFloat(discountInput.value) || 0;
        var discountedTotal = total - (total * discount / 100);

        totalPriceInput.value = discountedTotal.toFixed(2);
    }

    productSelect.addEventListener('change', calculateTotalPrice);
    discountInput.addEventListener('input', calculateTotalPrice);

    // Initial calculation
    calculateTotalPrice();
});
