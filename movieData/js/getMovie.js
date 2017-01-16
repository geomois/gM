app.service('GetMovieData', ['$http', function($http) {
    this.movieData =function(movie){
        $http.post('../data/movieData.json',movie).
            success(function(data) {
               console.log('succ'); 
                // or depends what you need testArr[0] = data.images;
            }).
            error(function(data) {
               console.log('fffff'); // log error
            });
    }

}]);

