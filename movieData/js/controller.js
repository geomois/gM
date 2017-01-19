app.controller('MainCtrl', ['$scope', '$http','GetMovieData', function($scope, $http, GetMovieData) {
 
 $scope.find = function() {
        var title = document.getElementById("search").value;
        $http.get('http://www.omdbapi.com/?t=' + title +'&type=movie').success(function(data) {
            // The then function here is an opportunity to modify the response
            $scope.responce = angular.fromJson(data);
            // The return value gets picked up by the then in the controller.
        }).error(function(data) {
            $scope.responce = data;
        });} 
        // Return the promise to the controller

        /* movieService.async().success(function(data) {
             $scope.movieList = [];
             for (var i = 0; i < data.images.length; i++) {
                 $scope.movieList.push(data.images[i]);
             }
             return $scope.movieList
         }) 
         */
        
    
  $scope.save = function(){
           //  $http.post('../data/movieData.json',$scope.responce).success(function(data){
      // GetMovieData.movieData($scope.responce);          
           //  });
        //     $scope.msg = 'Data sent: '+ JSON.stringify($scope.responce);
// use $.param jQuery function to serialize data from JSON 
            var data =[ {
                title: $scope.responce.Title,
                director: $scope.responce.Director,
                actors: $scope.responce.Actors,
                description: $scope.responce.Plot,
            }];

$http.post('data/movieData.json', JSON.stringify(data))
            .success(function (data) {
                $scope.PostDataResponse = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header +
                    "<hr />config: " + config;
            });
        } 


}]);