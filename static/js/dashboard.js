// dashboard.js

new Vue({
    el: '#app',
    data: {
        options: [
            { text: 'User Login', url: '{{ url_for("auth.user_login") }}' },
            { text: 'Store Manager Login', url: '{{ url_for("auth.store_manager_login") }}' },
            { text: 'Admin Login', url: '{{ url_for("auth.admin_login") }}' },
            { text: 'User Signup', url: '{{ url_for("auth.user_signup") }}' },
            { text: 'Store Manager Signup', url: '{{ url_for("auth.store_manager_signup") }}' }
        ],
        selectedOption: null
    },
    methods: {
        selectOption(option) {
            this.selectedOption = option;
        }
    }
});