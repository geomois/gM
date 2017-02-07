app.controller('TimerCtrl', ['$scope', '$timeout', 'CookieService',
    function($scope, $timeout, CookieService) {
        $scope.bar = 100;
        $scope.counter = 120;
        $scope.count = '';
        $scope.ready = 'none';
        var teams = CookieService.getCookies('teamCount');
        if (isEven(teams)) {
            $scope.team = CookieService.getCookies('team1');
            var teamC = 'team1';
        } else {
            $scope.team = CookieService.getCookies('team2');
            var teamC = 'team2';
        }

        $scope.onTimeout = function() {
            if ($scope.counter < 80) {
                $timeout.cancel(mytimeout);
                $scope.count = 'none';
                $scope.ready = 'block';
            } else {
                $scope.counter--;
                $scope.bar = $scope.counter * 0.833333;
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

    }
]);


app.controller('StartCtrl', ['$scope', 'CookieService',
    function($scope, CookieService) {

        $scope.team1 = '';
        $scope.team2 = '';
        $scope.save = function() {
            var team_2 = {
                name: $scope.team2,
                score: 0,
                movies: [],
                slice: $scope.a
            };
            var team_1 = {
                name: $scope.team1,
                score: 0,
                movies: [],
                slice: $scope.b
            };
            var teamCount = 1;
            CookieService.setCookies(team_1, team_2, teamCount);
            // CookieService.getCookies($cookies.team1);
        }
    }
]);

app.controller('GameCtrl', ['$timeout', '$scope', '$rootScope', 'GetMovieData', 'CookieService', 'GameService',
    function($timeout, $scope, $rootScope, GetMovieData, CookieService, GameService) {

        var teams = CookieService.getCookies('teamCount');
        if (!$rootScope.movies1 && !$rootScope.movies2) {
            GetMovieData.movieData(function(dataResponse) {
                //$scope.movies = dataResponse;
                $rootScope.movies1 = dataResponse.slice(0, 20)
                $rootScope.movies2 = dataResponse.slice(20, dataResponse.length)


                if (isEven(teams)) {
                    $scope.team = CookieService.getCookies('team1');
                    $scope.teamC = 'team1';
                    $scope.movie = GameService.game($scope.team.movies, $rootScope.movies1);
                } else {
                    $scope.team = CookieService.getCookies('team2');
                    $scope.teamC = 'team2';
                    $scope.movie = GameService.game($scope.team.movies, $rootScope.movies2);
                }

                console.log($rootScope.movies1, $rootScope.movies2)
                
            });
        }else{
            if (isEven(teams)) {
                    $scope.team = CookieService.getCookies('team1');
                    $scope.teamC = 'team1';
                    $scope.movie = GameService.game($scope.team.movies, $rootScope.movies1);
                } else {
                    $scope.team = CookieService.getCookies('team2');
                    $scope.teamC = 'team2';
                    $scope.movie = GameService.game($scope.team.movies, $rootScope.movies2);
                }
        }
     $scope.updateTeam = function(id) {
                    CookieService.teamArray($scope.teamC, id);
            }

    }
]);

app.controller('OverviewCrtl', ['$scope', '$cookies', 'CookieService', '$rootScope', 'GetMovieData', '$timeout',
    function($scope, $cookies, CookieService, $rootScope, GetMovieData, $timeout) {
        $scope.team1 = CookieService.getCookies('team1');
        $scope.team2 = CookieService.getCookies('team2');

        if (!$rootScope.movies1 && !$rootScope.movies2) {
            GetMovieData.movieData(function(dataResponse) {
                //$scope.movies = dataResponse;
                $rootScope.movies1 = dataResponse.slice(0, 20)
                $rootScope.movies2 = dataResponse.slice(20, dataResponse.length)
            });

        }
    }
]);

function isEven(n) {
    return n % 2;
}
var test = 'fdfdfdf'


function arraySlice(arr, x) {
    return arr.slice(x, (x + 5));
}
