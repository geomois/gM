app.controller('TimerCtrl', ['$scope', '$timeout', 'CookieService',
    function($scope, $timeout, CookieService) {
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

    }
]);


app.controller('StartCtrl', ['$timeout', '$scope', 'GetMovieData', 'CookieService',
    function($timeout, $scope, GetMovieData, CookieService) {
        GetMovieData.movieData(function(dataResponse) {
            $scope.movies = dataResponse;
        })


        $timeout(function() {
            $scope.a = Math.floor((Math.random() * ($scope.movies.length - 4)) + 0) // length-4
            $scope.b = Math.floor((Math.random() * ($scope.movies.length - 4)) + 0)
            console.log($scope.a,$scope.b)
        }, 200)

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
        GetMovieData.movieData(function(dataResponse) {
            $scope.movies = dataResponse;
        })


        var teams = CookieService.getCookies('teamCount');
        if (isEven(teams)) {
            $scope.team = CookieService.getCookies('team1');
            var teamC = 'team1';
            $timeout(function() {
                 $rootScope.movies1=arraySlice($scope.movies,$scope.team.slice)
                 $scope.movie = GameService.game($scope.team.movies, $rootScope.movies1);
            }, 200);    
        } else {
            $scope.team = CookieService.getCookies('team2');
            var teamC = 'team2';
            $timeout(function() {
                 $rootScope.movies2=arraySlice($scope.movies,$scope.team.slice)
                 $scope.movie = GameService.game($scope.team.movies, $rootScope.movies2);
            }, 200);
        }

        console.log($rootScope.movies1,$rootScope.movies2)
        $scope.updateTeam = function(id) {
            CookieService.teamArray(teamC, id);
        }
    }
]);

app.controller('OverviewCrtl', ['$scope', '$cookies', 'CookieService', '$rootScope', 'GetMovieData', '$timeout',
    function($scope, $cookies, CookieService, $rootScope, GetMovieData, $timeout) {
        $scope.team1 = CookieService.getCookies('team1');
        $scope.team2 = CookieService.getCookies('team2');
        console.log($scope.team1.slice,$scope.team2.slice)

        if ($rootScope.movies1 == undefined) {
            GetMovieData.movieData(function(dataResponse) {
                $scope.moviesResponce = dataResponse;
            })
            $timeout(function() {
                $rootScope.movies1 = arraySlice($scope.moviesResponce, $scope.team1.slice)
            }, 200)
        }
        if ($rootScope.movies2 == undefined) {
            GetMovieData.movieData(function(dataResponse) {
                $scope.moviesResponce = dataResponse;
            })
            $timeout(function() {
                $rootScope.movies2 = arraySlice($scope.moviesResponce, $scope.team2.slice)
            }, 200)
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
