var myApp = angular.module('myApp', ['ui.router'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});
// For Component users, it should look like this:
// var myApp = angular.module('myApp', [require('angular-ui-router')]);
myApp.config(function($stateProvider, $urlRouterProvider) {
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
        .state('state1', {
            url: "/",
            controller:'ProjectOverview',
            templateUrl: "/partials/read.html"
        });
});

myApp.controller('ProjectOverview', [ '$scope', '$http', function ($scope, $http) {

    //Hit API and get back response
    var url = "http://54.69.121.180:3000/show_activity";

    var req = {
        method: 'GET',
        url: url
    };

    $http(req).success(function (response) {

        response.features.forEach(function(activity) {
            activity.properties.time_created = format_date(activity.properties.time_created);
        });

        $scope.response = response;

    });

    var format_date = function(date) {
        var date_object = new Date(date);
        var month = date_object.getMonth();
        var day = date_object.getDay();
        var year = date_object.getFullYear();
        var date_object_formatted = month + "/" + day + "/" + year;

        return date_object_formatted;
    }

    var getDescription = function() {
        var description = $('#ckan-project-description').data().obj;
        return description;
    }

    var getTitle = function() {
        var title = $('#ckan-project-title').data().obj;
        return title;
    }

    var getName = function() {
        var name = $('#ckan-project-name').data().obj;
        return name;
    }

    $scope.projectDescription = getDescription();
    $scope.projectTitle = getTitle();
    $scope.projectName = getName();


}]);
