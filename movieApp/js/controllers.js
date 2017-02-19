app.controller('TimerCtrl', ['$scope', '$timeout', 'CookieService',
    function ($scope, $timeout, CookieService) {
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

        $scope.onTimeout = function () {
            if ($scope.counter < 0.5) {
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

        $scope.stop = function () {
            $timeout.cancel(mytimeout);
        }

        $scope.start = function () {
            mytimeout = $timeout($scope.onTimeout, 400);
        }
        $scope.paused = function (team) {
            CookieService.updateCookies(teamC);
            CookieService.updateCookiesTeams();
        }
        $scope.notPassed = function () {
            CookieService.updateCookiesTeams();
        }

    }
]);


app.controller('StartCtrl', ['$scope', '$rootScope', 'CookieService', 'GetMovieData',
    function ($scope, $rootScope, CookieService, GetMovieData) {

        GetMovieData.movieData(function (dataResponse) {
            console.log(dataResponse)
            $rootScope.movies1 = dataResponse.slice(0, 20)
            $rootScope.movies2 = dataResponse.slice(20, dataResponse.length)
        });
        $rootScope.poster = {
            "horror": "scary.png",
            "action": "adventure.png",
            "family": "families.png",
            "fantasy": "fantasy.png",
            "history": "history.png",
            "music": "musical.png",
            "crimeDrama":"crime.png",
            "noirRomance":"romance.png",
            "sport":"sport.png"
        }

        $rootScope.genres = [
                "Thriller", "Horror",
                "Biography", "History",
                "Sci-Fi", "Fantasy",
                "Crime", "Drama", 
                "Musical", "Music",
                "Romance", "Film-Noir",
                "Mystery", "Action", "Adventure", "Western", "War",
                "Sport",
                "Family", "Animation", "Comedy"];
                

        $scope.team1 = '';
        $scope.team2 = '';
        $scope.save = function () {
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

app.controller('GameCtrl', ['$timeout', '$scope', '$rootScope', 'CookieService', 'GameService',
    function ($timeout, $scope, $rootScope, CookieService, GameService) {

        var teams = CookieService.getCookies('teamCount');
        if (isEven(teams)) {
            $scope.team = CookieService.getCookies('team1');
            $scope.teamC = 'team1';
            $scope.movie = GameService.game($scope.team.movies, $rootScope.movies1);
        } else {
            $scope.team = CookieService.getCookies('team2');
            $scope.teamC = 'team2';
            $scope.movie = GameService.game($scope.team.movies, $rootScope.movies2);
        }
        
        var genre = $scope.movie.Genre;
        switchGendre($rootScope.genres, genre, function (data) {
            $scope.src = switchRes(data, $rootScope.genres, $rootScope.poster);
        });



        $scope.updateTeam = function (id) {
            CookieService.teamArray($scope.teamC, id);
        }

    }
]);

app.controller('OverviewCrtl', ['$scope', '$cookies', 'CookieService', '$rootScope', 'GetMovieData', '$timeout',
    function ($scope, $cookies, CookieService, $rootScope, GetMovieData, $timeout) {
        $scope.team1 = CookieService.getCookies('team1');
        $scope.team2 = CookieService.getCookies('team2');
        
        $scope.displayRound = $scope.team2.movies.length+1 > 10 ? 'none' : null
        $scope.display = $scope.team2.movies.length+1 > 10 ? null : 'none'
        if ($scope.display===null){
            console.log($scope.team1.score,$scope.team2.score)
            if ($scope.team1.score == $scope.team2.score){
                $scope.winner = 'DrAw'
            }else{
                $scope.winner = $scope.team1.score > $scope.team2.score ? $scope.team1.name : $scope.team2.name
            }
        }
        if (!$rootScope.movies1 && !$rootScope.movies2) {
            GetMovieData.movieData(function (dataResponse) {
                //$scope.movies = dataResponse;
                $rootScope.movies1 = dataResponse.slice(0, 20)
                $rootScope.movies2 = dataResponse.slice(20, dataResponse.length)
                $rootScope.genres = [
                    "Thriller", "Horror",
                    "Biography", "History",
                    "Sci-Fi", "Fantasy",
                    "Crime", "Drama", /*POSTER*/
                    "Musical", "Music",
                    "Romance", "Film-Noir",/*POSTER*/
                    "Mystery", "Action", "Adventure", "Western", "War",
                    "Sport",/*POSTER*/
                    "Family", "Animation", "Comedy"];

                $rootScope.poster = {
                    "horror": "scary.png",
                    "action": "adventure.png",
                    "family": "families.png",
                    "fantasy": "fantasy.png",
                    "history": "history.png",
                    "music": "musical.png",
                    "crimeDrama":"crime.png",
                    "noirRomance":"romance.png",
                    "sport":"sport.png"
                }
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

function switchGendre(array, str, callbackFunc) {
    for (i in array) {
        if (str.search(array[i]) > -1) {
            var res = array[i];
            break;
        }
    }
    return callbackFunc(res);
}

function switchRes(res, array, posj) {
    var poster = 'dead-Oscar.png'
    switch (res) {
        case array[0]:
        case array[1]:
            poster = posj.horror
            break
        case array[2]:
        case array[3]:
            poster = posj.history
            break
        case array[4]:
        case array[5]:
            poster = posj.fantasy
            break
        case array[6]:
        case array[7]:
            poster = posj.crimeDrama
            break
        case array[8]:
        case array[9]:
            poster = posj.music
            break
        case array[10]:
        case array[11]:
            poster = posj.noirRomance
            break
        case array[12]:
        case array[13]:
        case array[14]:
        case array[15]:
        case array[16]:
            poster = posj.action
            break
        case array[17]:
            poster = posj.sport
            break
        case array[18]:
        case array[19]:
        case array[20]:
            poster = posj.family
            break
        default:
            poster 
    }
    return poster
}
