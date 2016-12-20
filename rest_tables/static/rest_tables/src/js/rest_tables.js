// http://stackoverflow.com/questions/16539999/whats-the-recommended-way-to-extend-angularjs-controllers
var module = angular.module('restTables', ['ngTable']);

module.controller('restTableController', function($scope, NgTableParams, $http){
    var _this = this;
    // var initialParams = {}; // ng-init


    this.initialize = function() {
        _this.tableParams = new NgTableParams($scope.$parent.initialParams, {
            counts: [],
            getData: function(params) {
                // ajax request to api
                var urlParams = angular.copy($scope.$parent.urlParams);
                angular.extend(urlParams, {
                    'page': params._params.page,
                    'ordering': _this.getSorting(params).join(',')
                });
                if(params._params.filter){
                    urlParams = angular.extend(urlParams, params._params.filter);
                }
                return $http.get($scope.url, {params: urlParams}).then(function(data) {
                    params.total(data.data.count); // recal. page nav controls
                    return data.data.results;
                });
            }
        });
    };

    this.getSorting = function(params){
        var sorting = [];
        angular.forEach(params.sorting(), function(value, key){
            var sort = '';
            if(value == 'desc'){
                sort += '-';
            }
            sort += key;
            sorting.push(sort);
        });
        return sorting;
    };

    this.initialize();

});
