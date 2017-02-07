app.service('GetMovieData', ['$http','$q', function($http,$q) {
    this.movieData = function(callbackFunc) {
        $http.get('../movieData/data/data.cgi').
        success(function(data) {
            var data = angular.fromJson(data);
           
            // console.log(data); 
            return callbackFunc(data);
            // or depends what you need testArr[0] = data.images;
        }).
        error(function(data) {
            console.log('fffff'); // log error
        });
    }
}]);

app.service('CookieService', ['$cookies', function($cookies) {
    this.setCookies = function(team1, team2, teams) {
        $cookies.putObject('team1', team1);
        $cookies.putObject('team2', team2);
        $cookies.put('teamCount', teams);
        //$cookies.team1 = angular.toJson(team1);
        // $cookies.team2 = angular.toJson(team2);
    }
    this.getCookies = function(team) {
        return $cookies.getObject(team)
            //return angular.fromJson(t);
            // alert(mmmm.movies);
    }
    this.updateCookies = function(team) {
        var tCk = $cookies.getObject(team)
        tCk.score++;
        $cookies.putObject(team, tCk);
    }
    this.updateCookiesTeams = function() {
        var tC = $cookies.get('teamCount')
        $cookies.put('teamCount', ++tC)
    }
    this.teamArray = function(team, id) {
        var t = $cookies.getObject(team);       
        t.movies.push(id);
        $cookies.putObject(team, t);
    }

}]);

app.service('GameService', function() {

    function isEqual(ob, array) {
        var c = 0;
        for (var i = 0; i < array.length; i++) {
            if (array[i] == ob) {
                c++;
                break;
            }
        }
        if (c > 0) {
            return 1;
        } else {
            return 0;
        }
    }

    this.game = function(team, movies) {
        var movie = movies[Math.floor((Math.random() * movies.length) + 0)];
        var count = 0;
        if (team.length > 0 && team.length < movies.length) {
            do {


                count = isEqual(movie.id, team);
                movie = movies[Math.floor((Math.random() * movies.length) + 0)];

            } while (count != 0);
            return movie;
        } else {
            return movie;
            console.log(team.length);
        }
    }
});