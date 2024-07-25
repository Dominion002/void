document.getElementById('dashboard').addEventListener('click', function() {
    var subtext = document.getElementById('subtext');
    if (subtext.classList.contains('hidden')) {
        subtext.classList.remove('hidden');
    } else {
        subtext.classList.add('hidden');
    }
});

document.getElementById('settings').addEventListener('click', function() {
    var subtexts = document.getElementById('subtext2');
    if (subtexts.classList.contains('hidden')) {
        subtexts.classList.remove('hidden');
    } else {
        subtexts.classList.add('hidden');
    }
});

function toggleDropdown(event) {
    event.stopPropagation();
    const dropdown = event.currentTarget.nextElementSibling;
    dropdown.classList.toggle('hidden');
}

function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/delete_product/${productId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    return response.json().then(data => {
                        alert(data.message);
                    });
                }
            })
            .catch(error => {
                alert('Failed to delete product: ' + error.message);
            });
    }
}

document.addEventListener('click', function(event) {
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(dropdown => {
        if (!dropdown.contains(event.target) && !dropdown.previousElementSibling.contains(event.target)) {
            dropdown.classList.add('hidden');
        }
    });
});

document.getElementById('burger').addEventListener('click', function() {
    document.getElementById('menu').classList.toggle('hidden');
});

document.getElementById('load-more-button').addEventListener('click', function() {
    document.getElementById('hidden-content').classList.remove('hidden');
    this.classList.add('hidden');
    document.getElementById('show-less-button').classList.remove('hidden');
});

document.getElementById('show-less-button').addEventListener('click', function() {
    document.getElementById('hidden-content').classList.add('hidden');
    this.classList.add('hidden');
    document.getElementById('load-more-button').classList.remove('hidden');
});
