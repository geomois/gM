app.controller('OverviewCtrl',['$scope','CookieService', function($scope, CookieService){
    $scope.team1 = CookieService.getCookies('team1');
    $scope.team2 = CookieService.getCookies('team2');
    var round = CookieService.getCookies('teamCount');
    $scope.round = (isEven(round))?round:round-1;
}]);

app.controller('TimerCtrl', ['$scope', '$timeout', 'CookieService', function($scope, $timeout, CookieService) {
    $scope.counter = 120;
    $scope.count = '';
    $scope.ready = 'none';
    var teams = CookieService.getCookies('teamCount');
    if (!isEven(teams)) {
        $scope.team = CookieService.getCookies('team1');
        var teamC = 'team1';
    } else {
        $scope.team = CookieService.getCookies('team2');
        var teamC = 'team2';
    }

    $scope.onTimeout = function() {
        if ($scope.counter < 118) {
            $timeout.cancel(mytimeout);
            $scope.count = 'none';
            $scope.ready = 'block';
        } else {
            $scope.counter--;
            mytimeout = $timeout($scope.onTimeout, 1000);
        }
    }

    var mytimeout = $timeout($scope.onTimeout, 1000);

    $scope.stop = function() {
        $timeout.cancel(mytimeout);
    }

    $scope.start = function() {
        mytimeout = $timeout($scope.onTimeout, 400);
    }
    $scope.paused = function(team) {
        CookieService.updateCookies(teamC);
        CookieService.updateCookiesTeams();
    }
    $scope.notPassed = function() {
        CookieService.updateCookiesTeams();
    }

}]);


app.controller('StartCtrl', ['$scope', 'CookieService', function($scope, CookieService) {

    $scope.team1 = '';
    $scope.team2 = '';
    $scope.save = function() {
        var team_2 = {
            name: $scope.team2,
            score: 0,
            movies: []
        };
        var team_1 = {
            name: $scope.team1,
            score: 0,
            movies: []
        };
        var teamCount = 0;
        CookieService.setCookies(team_1, team_2, teamCount);
        // CookieService.getCookies($cookies.team1);
    }

}]);

app.controller('GameCtrl', ['$timeout', '$scope', 'GetMovieData', 'CookieService', 'GameService',
    function($timeout, $scope, GetMovieData, CookieService, GameService) {

        var teams = CookieService.getCookies('teamCount');
        if (!isEven(teams)) {
            $scope.team = CookieService.getCookies('team1');
            var teamC = 'team1';
        } else {
            $scope.team = CookieService.getCookies('team2');
            var teamC = 'team2';
        }


        console.log($scope.team);
        GetMovieData.movieData(function(dataResponse) {
            $scope.movies = dataResponse;
            // console.log(movies);
            // console.log(team);
        });
        //x=GameService.game();
        $timeout(function() {
            $scope.movie = GameService.game($scope.team.movies, $scope.movies);
        }, 200);
console.log($scope.team.name);
        $scope.updateTeam = function(id) {
            CookieService.teamArray(teamC,id);

        }
    }
]);

function isEven(n) {
    return n % 2;
}