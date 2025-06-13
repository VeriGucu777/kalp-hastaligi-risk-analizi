document.addEventListener('DOMContentLoaded', function () {
    const avatar = document.querySelector('.avatar');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    // Avatar tıklanınca menüyü aç/kapat
    avatar.addEventListener('click', function () {
        avatar.classList.toggle('active');
    });

    // Dropdown dışında bir yere tıklanınca menüyü kapat
    document.addEventListener('click', function (e) {
        if (!avatar.contains(e.target)) {
            avatar.classList.remove('active');
        }
    });
});

// Çıkış yap fonksiyonu
function logout() {
    if (confirm('Çıkış yapmak istediğinize emin misiniz?')) {
        window.location.href = "{{ url_for('logout') }}";
    }
}
