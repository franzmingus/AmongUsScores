function sendRequest(url, method, data){
    var r = axios({
        method: method,
        url: url,
        data: data,
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {
            'X-Requested-with': 'XMLHttpRequest'
        }
    })

    return r
}

var app = new Vue({
    el: '#app',
    data: {
        name: "",
        players: [  ],
        winner: {name: "Unkown", score: -1},
        raw_data: [],
        checked_players: [],
        password: "",
    },
    created(){
        var vm = this;
        var r = sendRequest('','get')
            .then(function(response){
                vm.players = response.data.players;
                vm.raw_data = response.data.raw_data;
            })
    },
    methods: {
        createPlayer(){
            console.log("Adding Player");
            var vm = this;
            var formData = new FormData();

            if( vm.name != "" ){

                formData.append("name", vm.name);
                formData.append("action", "add_player");

                sendRequest('', 'post', formData)
                    .then(function(response){
                        vm.raw_data.push(response.data)
                        vm.name = "";
                    })
            }

        },
        removePlayer(){
            console.log("Removing Player");
            var vm = this;
            var formData = new FormData();

            var checked = vm.checked_players;
            console.log(checked);

            if( checked != [] ){

                formData.append("names", checked);
                formData.append("action", "remove_players");

                sendRequest('', 'post', formData)
                        .then(function(response){
                            vm.raw_data = response.data.raw_data
                            vm.checked_players = []
                        })

            }
            else{
                console.log("Checks missing on players");
            }

        },
        updateWinner(){
            console.log("Adding Winner");
            var vm = this;
            var formData = new FormData();

            var winners = vm.checked_players;
            console.log(winners);

            formData.append("winners", winners);
            formData.append("action", "update_winners");

            sendRequest('', 'post', formData)
                    .then(function(response){
                        vm.raw_data = response.data.raw_data
                        vm.checked_players = []
                    })

        },
        updateLooser(){
            console.log("Adding Looser");

            var vm = this;
            var formData = new FormData();

            var loosers = vm.checked_players;
            console.log(loosers);

            formData.append("loosers", loosers);
            formData.append("action", "update_loosers");

            sendRequest('', 'post', formData)
                    .then(function(response){
                        vm.raw_data = response.data.raw_data
                        vm.checked_players = []
                    })

        },
    }
})